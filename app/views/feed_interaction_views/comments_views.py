"""Feed comment interaction views."""

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Product
from app.views.product_views.product_interactions_view import handle_comment

@login_required
@transaction.atomic
def feed_comment_product_view(request, product_id):
    """View for commenting on a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        comment_text = request.POST.get('comment_text')

        if comment_text:
            # Use the existing handle_comment function
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

    return JsonResponse({'error': 'POST request required'}, status=400)
