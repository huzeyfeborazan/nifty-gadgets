"""Feed-related views."""

from django.shortcuts import render
from app.models import Product

def feed_view(request):
    """This is the feed page view"""
    trending_products = Product.objects.filter(product_is_trending=True)
    new_products = Product.objects.filter(product_is_new=True)
    controversial_products = Product.objects.filter(product_is_controversial=True)
    popular_products = Product.objects.filter(product_is_popular=True)

    context = {
        'trending_products': trending_products,
        'new_products': new_products,
        'controversial_products': controversial_products,
        'popular_products': popular_products
    }
    return render(request, 'app/feed.html', context)
