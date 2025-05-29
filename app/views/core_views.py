"""Core views for the application."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Review

def home(request):
    """This is the home page view"""
    return render(request, 'app/home.html')

@login_required
def dashboard_view(request):
    """This is the dashboard page view"""
    # Get user's reviews with related product data
    user_reviews = Review.objects.filter(user=request.user).select_related('product').order_by('-timestamp')

    context = {
        'user': request.user,
        'user_reviews': user_reviews,
        'total_reviews': request.user.total_reviews_by_user,
        'total_upvotes': request.user.total_upvotes_by_user,
        'total_downvotes': request.user.total_downvotes_by_user,
        'total_comments': request.user.total_comments_by_user,
        'total_interactions': request.user.total_interaction_by_user,
    }

    return render(request, 'app/dashboard.html', context)
