"""Product detail view."""

from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from app.models import Product, Review, Upvote, Downvote, Comment
from app.forms import ReviewForm

def product_detail_view(request, product_id):
    """View for displaying product details."""
    # Calculate product statistics
    product = get_object_or_404(
        Product.objects.annotate(
            annotated_average_rating=Avg('review__review_score'),
            annotated_review_count=Count('review'),
            annotated_upvote_count=Count('upvote'),
            annotated_downvote_count=Count('downvote'),
            annotated_comment_count=Count('comment')
        ),
        id=product_id
    )

    # Handle possible None value from Avg:
    product.annotated_average_rating = product.annotated_average_rating or 0

    # Calculate product score:
    denominator = (product.annotated_upvote_count +
                   product.annotated_downvote_count) * product.annotated_review_count
    product.score = (
        (product.annotated_upvote_count - product.annotated_downvote_count)
          * product.annotated_average_rating /
        denominator if denominator > 0 else 0
    )

    # Check if current user has interacted with the product
    if request.user.is_authenticated:
        user_has_upvoted = Upvote.objects.filter(product=product, user=request.user).exists()
        user_has_downvoted = Downvote.objects.filter(product=product, user=request.user).exists()
        user_has_commented = Comment.objects.filter(product=product, user=request.user).exists()
        user_has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
    else:
        user_has_upvoted = user_has_downvoted = user_has_commented = user_has_reviewed = False

    # Fetch reviews along with their authors and timestamps
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-timestamp')

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
