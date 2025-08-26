"""Feed upvote interaction views."""

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Product
from app.views.product_views.product_interactions_view import handle_upvote
from app.views.product_views.calculate_product_score import calculate_product_score

@login_required
@transaction.atomic
def feed_upvote_product_view(request, product_id):
    """View for upvoting a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        # Use the existing handle_upvote function
        handle_upvote(request, product)

        # Refresh product data to get updated counts
        product.refresh_from_db()

        # Calculate product score and update it in the database
        calculate_product_score(product.id)

        # Check if user has upvoted after handling
        from app.models import Upvote
        upvoted = Upvote.objects.filter(product=product, user=request.user).exists()

        return JsonResponse({
            'upvoted': upvoted,
            'total_upvotes': product.product_upvote_count,
        })

    return JsonResponse({'error': 'POST request required'}, status=400)
