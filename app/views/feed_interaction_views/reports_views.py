"""Feed report interaction views."""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import Product, Report

@login_required
def feed_report_product_view(request, product_id):
    """View for reporting a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        # Check if user has already reported this product
        existing_report = Report.objects.filter(product=product, user=user).first()

        if existing_report:
            return JsonResponse({
                'reported': True,
                'message': 'You have already reported this product.',
                'total_reports': product.product_report_count
            })
        else:
            # Create new report
            Report.objects.create(product=product, user=user)
            # Increase report count
            product.product_report_count += 1
            user.total_reports_by_user += 1
            product.author_user.total_reports_received_by_user += 1

            # Save all changes
            product.save(update_fields=['product_report_count'])
            user.save(update_fields=['total_reports_by_user'])
            product.author_user.save(update_fields=['total_reports_received_by_user'])

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
                'reported': True,
                'message': 'Product reported successfully.',
                'total_reports': product.product_report_count
            })

    return JsonResponse({'error': 'POST request required'}, status=400)
