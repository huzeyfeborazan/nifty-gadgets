"""Product detail view."""
# Shows product details, reviews, and interactions after a user clicks on a product

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.http import JsonResponse
from app.models import Product, Review, Upvote, Downvote, Comment
from app.forms import ReviewForm
from app.views.product_views.product_interactions_view import (
    handle_review, handle_upvote, handle_downvote, handle_comment, handle_report
)
from app.views.product_views.calculate_product_score import calculate_product_score

def get_user_interactions(product, user):
    """Show previous interactions of user viewing the product."""
    user_has_upvoted = Upvote.objects.filter(product=product, user=user).exists()
    user_has_downvoted = Downvote.objects.filter(product=product, user=user).exists()
    user_has_commented = Comment.objects.filter(product=product, user=user).exists()
    user_has_reviewed = Review.objects.filter(product=product, user=user).exists()
    return user_has_upvoted, user_has_downvoted, user_has_commented, user_has_reviewed


def product_detail_view(request, product_id):
    """View for displaying product details."""

    # Calculate product statistics
    product = get_object_or_404(
        Product.objects.annotate(
            annotated_average_rating=Avg('reviews__review_score'),
            annotated_review_count=Count('reviews'),
            annotated_upvote_count=Count('upvotes'),
            annotated_downvote_count=Count('downvotes'),
            annotated_comment_count=Count('comments')
        ),
        id=product_id
    )

    # Handle possible None value from Avg:
    product.annotated_average_rating = product.annotated_average_rating or 0

    # Calculate product score (for internal use)
    product.score = calculate_product_score(product.id)

    # Check if current user has interacted with the product
    user = request.user
    if user.is_authenticated:
        user_has_upvoted, user_has_downvoted, user_has_commented, user_has_reviewed = get_user_interactions(product, user)
    else:
        user_has_upvoted = user_has_downvoted = user_has_commented = user_has_reviewed = False

    # Fetch reviews along with their authors and timestamps
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')

    if request.method == 'POST' and user.is_authenticated:
        action = request.POST.get('action')

        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if action == 'upvote':
                handle_upvote(request, product)
                return JsonResponse({
                    'success': True,
                    'upvoted': Upvote.objects.filter(product=product, user=user).exists(),
                    'total_upvotes': product.product_upvote_count
                })
            elif action == 'downvote':
                handle_downvote(request, product)
                return JsonResponse({
                    'success': True,
                    'downvoted': Downvote.objects.filter(product=product, user=user).exists(),
                    'total_downvotes': product.product_downvote_count
                })
            elif action == 'comment':
                comment_text = request.POST.get('comment_text')
                if comment_text:
                    handle_comment(request, product)
                    return JsonResponse({
                        'success': True,
                        'message': 'Comment added successfully.',
                        'total_comments': product.product_comment_count
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Comment cannot be empty.'
                    }, status=400)
            elif action == 'report':
                handle_report(request, product)
                return JsonResponse({
                    'success': True,
                    'message': 'Product reported successfully.',
                    'total_reports': product.product_report_count
                })
            elif action == 'review':
                handle_review(request, product)
                return JsonResponse({
                    'success': True,
                    'message': 'Review added successfully.'
                })

        # Handle regular POST requests (fallback)
        elif action == 'review':
            handle_review(request, product)
            return redirect('app:product_detail', product_id=product.id)

    # Prepare context for template
    context = {
        'product': product,
        'reviews': reviews,
        'user_has_upvoted': user_has_upvoted,
        'user_has_downvoted': user_has_downvoted,
        'user_has_commented': user_has_commented,
        'user_has_reviewed': user_has_reviewed,
        'review_form': ReviewForm(),
        'product_score': product.score,
        'product_average_rating': product.annotated_average_rating,
        'product_upvote_count': product.annotated_upvote_count,
        'product_downvote_count': product.annotated_downvote_count,
        'product_review_count': product.annotated_review_count,
        'product_comment_count': product.annotated_comment_count,
    }

    return render(request, 'app/product_detail.html', context)
