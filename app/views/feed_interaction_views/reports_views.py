"""Feed report interaction views."""

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Product
from app.views.product_views.product_interactions_view import handle_report

@login_required
@transaction.atomic
def feed_report_product_view(request, product_id):
    """View for reporting a product in the feed."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        # Check if user has already reported this product
        from app.models import Report
        existing_report = Report.objects.filter(product=product, user=request.user).first()

        if existing_report:
            return JsonResponse({
                'reported': True,
                'message': 'You have already reported this product.',
                'total_reports': product.product_report_count
            })
        else:
            # Use the existing handle_report function
            handle_report(request, product)

            return JsonResponse({
                'reported': True,
                'message': 'Product reported successfully.',
                'total_reports': product.product_report_count
            })

    return JsonResponse({'error': 'POST request required'}, status=400)
