"""Feed comment interaction views."""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import Product, Comment

@login_required
def feed_comment_product_view(request, product_id):
    """View for commenting on a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        comment_text = request.POST.get('comment_text')

        if comment_text:
            # Create new comment
            Comment.objects.create(
                product=product,
                user=user,
                comment_text=comment_text
            )
            # Increase comment count
            product.product_comment_count += 1
            user.total_comments_by_user += 1
            product.author_user.total_comments_received_by_user += 1

            # Save all changes
            product.save(update_fields=['product_comment_count'])
            user.save(update_fields=['total_comments_by_user'])
            product.author_user.save(update_fields=['total_comments_received_by_user'])

            # Update total interaction counts
            product.product_interaction_count = (
                product.product_upvote_count +
                product.product_downvote_count +
                product.product_comment_count +
                product.product_report_count
            )
            product.save(update_fields=['product_interaction_count'])

            user.total_interaction_by_user = (
                user.total_upvotes_by_user +
                user.total_downvotes_by_user +
                user.total_comments_by_user +
                user.total_reviews_by_user +
                user.total_reports_by_user
            )
            user.save(update_fields=['total_interaction_by_user'])

            product.author_user.total_interactions_received_by_user = (
                product.author_user.total_upvotes_received_by_user +
                product.author_user.total_downvotes_received_by_user +
                product.author_user.total_comments_received_by_user +
                product.author_user.total_reports_received_by_user
            )
            product.author_user.save(update_fields=['total_interactions_received_by_user'])

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

    return JsonResponse({'error': 'POST request required'}, status=400)
