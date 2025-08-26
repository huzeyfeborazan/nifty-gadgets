"""Calculate product score."""

from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from app.models import Product


def calculate_product_score(pk, minimum_reviews=5):
    """Calculate the ranking score for a product on the platform, update it in the database"""

    # Get product and annotate with review count and average rating
    product = get_object_or_404(Product.objects.annotate(
        annotated_review_count=Count('reviews'),
        annotated_average_rating=Avg('reviews__review_score')
    ), pk=pk)

    # Calculate global average rating across all products
    global_average_rating = Product.objects.aggregate(
        Avg('reviews__review_score')
    )['reviews__review_score__avg'] or 3.0

    # Get average rating for the product
    average_rating = product.annotated_average_rating or 0

    # Get review count for the product
    review_count = product.annotated_review_count or 0

    # Compute denominator for Bayesian formula
    denominator = product.annotated_review_count + minimum_reviews

    # Bayesian formula
    product.product_score = (
        (review_count * average_rating + minimum_reviews * global_average_rating)
        / denominator
    )

    # Update the product in the database
    product.save(update_fields=['product_score'])

    return product.product_score
