"""Core views for the application."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Review, Product

def home(request):
    """This is the home page view"""
    return render(request, 'app/home.html')

@login_required
def dashboard_view(request):
    """This is the dashboard page view"""
    # Get user's reviews with related product data
    user_reviews = Review.objects.filter(user=request.user).select_related('product').order_by('-created_at')

    context = {
        'user': request.user,
        'user_reviews': user_reviews,
        'total_reviews': request.user.get_total_reviews(),
        'total_upvotes': request.user.get_total_upvotes_given(),
        'total_downvotes': request.user.get_total_downvotes_given(),
        'total_comments': request.user.get_total_comments(),
        'total_products': request.user.get_total_products(),
    }

    return render(request, 'app/dashboard.html', context)

def lists_view(request):
    """This is the lists page view showing recommended product collections"""

    # Best Productivity Tools
    best_productivity_tools = Product.objects.filter(
        product_category='productivity_tools'
    ).order_by('-product_score')[:7]

    # Essential Mobile Accessories
    essential_mobile_accessories = Product.objects.filter(
        product_category='mobile_accessories'
    ).order_by('-product_score')[:7]

    # Smart Home Essentials
    smart_home_essentials = Product.objects.filter(
        product_category='smart_home_essentials'
    ).order_by('-product_score')[:7]

    # Gaming Accessories
    gaming_accessories = Product.objects.filter(
        product_category='gaming_accessories'
    ).order_by('-product_score')[:7]

    # Audio Accessories
    audio_accessories = Product.objects.filter(
        product_category='audio_accessories'
    ).order_by('-product_score')[:7]

    # Camera Accessories
    camera_accessories = Product.objects.filter(
        product_category='camera_accessories'
    ).order_by('-product_score')[:7]

    # Office Essentials
    office_essentials = Product.objects.filter(
        product_category='office_essentials'
    ).order_by('-product_score')[:7]

    # Travel Essentials
    travel_essentials = Product.objects.filter(
        product_category='travel_essentials'
    ).order_by('-product_score')[:7]

    # Health and Fitness
    health_and_fitness = Product.objects.filter(
        product_category='health_and_fitness'
    ).order_by('-product_score')[:7]

    # Home and Garden
    home_and_garden = Product.objects.filter(
        product_category='home_and_garden'
    ).order_by('-product_score')[:7]

    # Other
    other = Product.objects.filter(
        product_category='other'
    ).order_by('-product_score')[:7]


    context = {
        'best_productivity_tools': best_productivity_tools,
        'essential_mobile_accessories': essential_mobile_accessories,
        'smart_home_essentials': smart_home_essentials,
        'gaming_accessories': gaming_accessories,
        'audio_accessories': audio_accessories,
        'camera_accessories': camera_accessories,
        'office_essentials': office_essentials,
        'travel_essentials': travel_essentials,
        'health_and_fitness': health_and_fitness,
        'home_and_garden': home_and_garden,
        'other': other,
    }

    return render(request, 'app/lists.html', context)
