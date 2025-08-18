"""Feed downvote interaction views."""

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Product
from app.views.product_views.product_interactions_view import handle_downvote

@login_required
@transaction.atomic
def feed_downvote_product_view(request, product_id):
    """View for downvoting a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        # Use the existing handle_downvote function
        handle_downvote(request, product)

        # Check if user has downvoted after handling
        from app.models import Downvote
        downvoted = Downvote.objects.filter(product=product, user=request.user).exists()

        return JsonResponse({
            'downvoted': downvoted,
            'total_downvotes': product.product_downvote_count,
        })

    return JsonResponse({'error': 'POST request required'}, status=400)
