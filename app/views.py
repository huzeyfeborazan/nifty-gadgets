""" This is the views.py file for the app"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Product, Review, Upvote, Downvote, Comment, Report
from .forms import ReviewForm

def home(request):
    """This is the home page view"""

    return render(request, 'app/home.html')

def register_view(request):
    """This is the register page view"""

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('app:dashboard')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    """This is the login page view"""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('app:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'app/login.html')

def logout_view(request):
    """This is the logout page view"""

    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('app:home')

@login_required
def dashboard_view(request):
    """This is the dashboard page view"""

    return render(request, 'app/dashboard.html', {'user': request.user})

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

def product_detail_view(request, product_id):
    """View for displaying product details and handling user interactions."""

    product = get_object_or_404(Product, id=product_id)

    # Calculate product statistics
    product.average_rating = Review.objects.filter(product=product).aggregate(
        Avg('review_score'))['review_score__avg'] or 0
    product.review_count = Review.objects.filter(product=product).count()
    product.upvote_count = Upvote.objects.filter(product=product).count()
    product.downvote_count = Downvote.objects.filter(product=product).count()
    product.comment_count = Comment.objects.filter(product=product).count()
    denominator = (product.upvote_count + product.downvote_count) * product.review_count
    product.score = (
        (product.upvote_count - product.downvote_count) * product.average_rating /
        denominator if denominator > 0 else 0
    )

    # Handle POST requests for user interactions
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to interact with products.')
            # display link to login/register page here
        else:
            action = request.POST.get('action')

            if action == 'upvote':
                # Toggle upvote
                upvote, created = Upvote.objects.get_or_create(
                    product=product,
                    user=request.user
                )
                if not created:
                    upvote.delete()

            elif action == 'downvote':
                # Toggle downvote
                downvote, created = Downvote.objects.get_or_create(
                    product=product,
                    user=request.user
                )
                if not created:
                    downvote.delete()
                messages.success(request, 'Downvote updated successfully.')

            elif action == 'comment':
                comment_text = request.POST.get('comment_text')
                if comment_text:
                    Comment.objects.create(
                        product=product,
                        user=request.user,
                        comment_text=comment_text
                    )
                    messages.success(request, 'Comment added successfully.')
                else:
                    messages.error(request, 'Comment cannot be empty.')

            elif action == 'report':
                Report.objects.create(
                    product=product,
                    user=request.user
                )
                messages.success(request, 'Product reported successfully.')

            elif action == 'review':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Review added successfully.')
                else:
                    messages.error(request, 'Please provide a valid review.')

            return redirect('app:product_detail', product_id=product.id)


    # Check if current user has interacted with the product
    user_has_upvoted = request.user.is_authenticated and Upvote.objects.filter(
        product=product, user=request.user).exists()
    user_has_downvoted = request.user.is_authenticated and Downvote.objects.filter(
        product=product, user=request.user).exists()
    user_has_commented = request.user.is_authenticated and Comment.objects.filter(
        product=product, user=request.user).exists()
    user_has_reviewed = request.user.is_authenticated and Review.objects.filter(
        product=product, user=request.user).exists()

    context = {
        'product': product,
        'user_has_upvoted': user_has_upvoted,
        'user_has_downvoted': user_has_downvoted,
        'user_has_commented': user_has_commented,
        'user_has_reviewed': user_has_reviewed,
        'review_form': ReviewForm(),
        'product_score': product.score,
        'product_average_rating': product.average_rating,
        'product_upvote_count': product.upvote_count,
        'product_downvote_count': product.downvote_count,
        'product_review_count': product.review_count,
        'product_comment_count': product.comment_count,
    }

    return render(request, 'app/product_detail.html', context)
