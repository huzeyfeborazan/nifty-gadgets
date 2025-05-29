"""Feed downvote interaction views."""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import Product, Upvote, Downvote

@login_required
def feed_downvote_product_view(request, product_id):
    """View for downvoting a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        # Remove any existing upvote
        had_upvote = Upvote.objects.filter(product=product, user=user).exists()
        Upvote.objects.filter(product=product, user=user).delete()
        if had_upvote:
            product.product_upvote_count = max(0, product.product_upvote_count - 1)
            user.total_upvotes_by_user = max(0, user.total_upvotes_by_user - 1)
            product.author_user.total_upvotes_received_by_user = max(0, product.author_user.total_upvotes_received_by_user - 1)
            product.save(update_fields=['product_upvote_count'])
            user.save(update_fields=['total_upvotes_by_user'])
            product.author_user.save(update_fields=['total_upvotes_received_by_user'])

        # Check if user already downvoted this product
        existing_downvote = Downvote.objects.filter(product=product, user=user).first()

        if existing_downvote:
            # Remove the existing downvote (toggle off)
            existing_downvote.delete()
            downvoted = False
            # Decrease downvote count
            product.product_downvote_count = max(0, product.product_downvote_count - 1)
            user.total_downvotes_by_user = max(0, user.total_downvotes_by_user - 1)
            product.author_user.total_downvotes_received_by_user = max(0, product.author_user.total_downvotes_received_by_user - 1)
        else:
            # Add a new downvote
            Downvote.objects.create(product=product, user=user)
            downvoted = True
            # Increase downvote count
            product.product_downvote_count += 1
            user.total_downvotes_by_user += 1
            product.author_user.total_downvotes_received_by_user += 1

        # Save all changes
        product.save(update_fields=['product_downvote_count'])
        user.save(update_fields=['total_downvotes_by_user'])
        product.author_user.save(update_fields=['total_downvotes_received_by_user'])

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
            'downvoted': downvoted,
            'total_downvotes': product.product_downvote_count,
        })

    return JsonResponse({'error': 'POST request required'}, status=400)
