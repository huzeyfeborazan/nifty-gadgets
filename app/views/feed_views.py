"""Feed-related views."""

from django.shortcuts import render
from app.models import Product

def feed_view(request):
    """This is the feed page view"""
    trending_products = Product.get_trending_products()
    new_products = Product.get_new_products()
    controversial_products = Product.get_controversial_products()
    popular_products = Product.get_popular_products()

    context = {
        'trending_products': trending_products,
        'new_products': new_products,
        'controversial_products': controversial_products,
        'popular_products': popular_products
    }
    return render(request, 'app/feed.html', context)
