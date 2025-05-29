""" This is the views.py file for the app"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from .models import Product, Review, Upvote, Downvote, Comment, Report, ProductCategory
from .forms import ReviewForm, ProductForm

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

@login_required
def feed_upvote_product_view(request, product_id):
    """View for upvoting a product in the feed."""

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        # Remove any existing downvote
        had_downvote = Downvote.objects.filter(product=product, user=user).exists()
        Downvote.objects.filter(product=product, user=user).delete()
        if had_downvote:
            product.product_downvote_count = max(0, product.product_downvote_count - 1)
            user.total_downvotes_by_user = max(0, user.total_downvotes_by_user - 1)
            product.author_user.total_downvotes_received_by_user = max(0, product.author_user.total_downvotes_received_by_user - 1)
            product.save(update_fields=['product_downvote_count'])
            user.save(update_fields=['total_downvotes_by_user'])
            product.author_user.save(update_fields=['total_downvotes_received_by_user'])

        # Check if user already upvoted this product
        existing_upvote = Upvote.objects.filter(product=product, user=user).first()

        if existing_upvote:
            # Remove the existing upvote (toggle off)
            existing_upvote.delete()
            upvoted = False
            # Decrease upvote count
            product.product_upvote_count = max(0, product.product_upvote_count - 1)
            user.total_upvotes_by_user = max(0, user.total_upvotes_by_user - 1)
            product.author_user.total_upvotes_received_by_user = max(0, product.author_user.total_upvotes_received_by_user - 1)
        else:
            # Add a new upvote
            Upvote.objects.create(product=product, user=user)
            upvoted = True
            # Increase upvote count
            product.product_upvote_count += 1
            user.total_upvotes_by_user += 1
            product.author_user.total_upvotes_received_by_user += 1

        # Save all changes
        product.save(update_fields=['product_upvote_count'])
        user.save(update_fields=['total_upvotes_by_user'])
        product.author_user.save(update_fields=['total_upvotes_received_by_user'])

        # Update total interaction counts
        product.product_interaction_count = (
            product.product_upvote_count +
            product.product_downvote_count +
            product.product_comment_count +
            product.product_report_count
        )
        product.save(update_fields=['product_interaction_count'])

        user.total_interaction_by_user = (
            user.total_upvotes_by_user +
            user.total_downvotes_by_user +
            user.total_comments_by_user +
            user.total_reviews_by_user +
            user.total_reports_by_user
        )
        user.save(update_fields=['total_interaction_by_user'])

        product.author_user.total_interactions_received_by_user = (
            product.author_user.total_upvotes_received_by_user +
            product.author_user.total_downvotes_received_by_user +
            product.author_user.total_comments_received_by_user +
            product.author_user.total_reports_received_by_user
        )
        product.author_user.save(update_fields=['total_interactions_received_by_user'])

        return JsonResponse({
            'upvoted': upvoted,
            'total_upvotes': product.product_upvote_count,
        })

    # If not a POST request, return error
    return JsonResponse({'error': 'POST request required'}, status=400)

@login_required
def feed_downvote_product_view(request, product_id):
    """View for downvoting a product in the feed."""

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        # Remove any existing upvote
        had_upvote = Upvote.objects.filter(product=product, user=user).exists()
        Upvote.objects.filter(product=product, user=user).delete()
        if had_upvote:
            product.product_upvote_count = max(0, product.product_upvote_count - 1)
            user.total_upvotes_by_user = max(0, user.total_upvotes_by_user - 1)
            product.author_user.total_upvotes_received_by_user = max(0, product.author_user.total_upvotes_received_by_user - 1)
            product.save(update_fields=['product_upvote_count'])
            user.save(update_fields=['total_upvotes_by_user'])
            product.author_user.save(update_fields=['total_upvotes_received_by_user'])

        # Check if user already downvoted this product
        existing_downvote = Downvote.objects.filter(product=product, user=user).first()

        if existing_downvote:
            # Remove the existing downvote (toggle off)
            existing_downvote.delete()
            downvoted = False
            # Decrease downvote count
            product.product_downvote_count = max(0, product.product_downvote_count - 1)
            user.total_downvotes_by_user = max(0, user.total_downvotes_by_user - 1)
            product.author_user.total_downvotes_received_by_user = max(0, product.author_user.total_downvotes_received_by_user - 1)
        else:
            # Add a new downvote
            Downvote.objects.create(product=product, user=user)
            downvoted = True
            # Increase downvote count
            product.product_downvote_count += 1
            user.total_downvotes_by_user += 1
            product.author_user.total_downvotes_received_by_user += 1

        # Save all changes
        product.save(update_fields=['product_downvote_count'])
        user.save(update_fields=['total_downvotes_by_user'])
        product.author_user.save(update_fields=['total_downvotes_received_by_user'])

        # Update total interaction counts
        product.product_interaction_count = (
            product.product_upvote_count +
            product.product_downvote_count +
            product.product_comment_count +
            product.product_report_count
        )
        product.save(update_fields=['product_interaction_count'])

        user.total_interaction_by_user = (
            user.total_upvotes_by_user +
            user.total_downvotes_by_user +
            user.total_comments_by_user +
            user.total_reviews_by_user +
            user.total_reports_by_user
        )
        user.save(update_fields=['total_interaction_by_user'])

        product.author_user.total_interactions_received_by_user = (
            product.author_user.total_upvotes_received_by_user +
            product.author_user.total_downvotes_received_by_user +
            product.author_user.total_comments_received_by_user +
            product.author_user.total_reports_received_by_user
        )
        product.author_user.save(update_fields=['total_interactions_received_by_user'])

        return JsonResponse({
            'downvoted': downvoted,
            'total_downvotes': product.product_downvote_count,
        })

    # If not a POST request, return error
    return JsonResponse({'error': 'POST request required'}, status=400)

@login_required
def feed_report_product_view(request, product_id):
    """View for reporting a product in the feed."""

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        # Check if user has already reported this product
        existing_report = Report.objects.filter(product=product, user=user).first()

        if existing_report:
            # User has already reported this product
            return JsonResponse({
                'reported': True,
                'message': 'You have already reported this product.',
                'total_reports': product.product_report_count
            })
        else:
            # Create new report
            Report.objects.create(product=product, user=user)
            # Increase report count
            product.product_report_count += 1
            user.total_reports_by_user += 1
            product.author_user.total_reports_received_by_user += 1

            # Save all changes
            product.save(update_fields=['product_report_count'])
            user.save(update_fields=['total_reports_by_user'])
            product.author_user.save(update_fields=['total_reports_received_by_user'])

            # Update total interaction counts
            product.product_interaction_count = (
                product.product_upvote_count +
                product.product_downvote_count +
                product.product_comment_count +
                product.product_report_count
            )
            product.save(update_fields=['product_interaction_count'])

            user.total_interaction_by_user = (
                user.total_upvotes_by_user +
                user.total_downvotes_by_user +
                user.total_comments_by_user +
                user.total_reviews_by_user +
                user.total_reports_by_user
            )
            user.save(update_fields=['total_interaction_by_user'])

            product.author_user.total_interactions_received_by_user = (
                product.author_user.total_upvotes_received_by_user +
                product.author_user.total_downvotes_received_by_user +
                product.author_user.total_comments_received_by_user +
                product.author_user.total_reports_received_by_user
            )
            product.author_user.save(update_fields=['total_interactions_received_by_user'])

            return JsonResponse({
                'reported': True,
                'message': 'Product reported successfully.',
                'total_reports': product.product_report_count
            })

    # If not a POST request, return error
    return JsonResponse({'error': 'POST request required'}, status=400)

@login_required
def feed_comment_product_view(request, product_id):
    """View for commenting on a product in the feed."""

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        comment_text = request.POST.get('comment_text')

        if comment_text:
            # Create new comment
            Comment.objects.create(
                product=product,
                user=user,
                comment_text=comment_text
            )
            # Increase comment count
            product.product_comment_count += 1
            user.total_comments_by_user += 1
            product.author_user.total_comments_received_by_user += 1

            # Save all changes
            product.save(update_fields=['product_comment_count'])
            user.save(update_fields=['total_comments_by_user'])
            product.author_user.save(update_fields=['total_comments_received_by_user'])

            # Update total interaction counts
            product.product_interaction_count = (
                product.product_upvote_count +
                product.product_downvote_count +
                product.product_comment_count +
                product.product_report_count
            )
            product.save(update_fields=['product_interaction_count'])

            user.total_interaction_by_user = (
                user.total_upvotes_by_user +
                user.total_downvotes_by_user +
                user.total_comments_by_user +
                user.total_reviews_by_user +
                user.total_reports_by_user
            )
            user.save(update_fields=['total_interaction_by_user'])

            product.author_user.total_interactions_received_by_user = (
                product.author_user.total_upvotes_received_by_user +
                product.author_user.total_downvotes_received_by_user +
                product.author_user.total_comments_received_by_user +
                product.author_user.total_reports_received_by_user
            )
            product.author_user.save(update_fields=['total_interactions_received_by_user'])

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

    # If not a POST request, return error
    return JsonResponse({'error': 'POST request required'}, status=400)


def product_detail_view(request, product_id):
    """View for displaying product details and handling user interactions."""

    # Calculate product statistics
    product = get_object_or_404(
        Product.objects.annotate(
            annotated_average_rating=Avg('review__review_score'),
            annotated_review_count=Count('review'),
            annotated_upvote_count=Count('upvote'),
            annotated_downvote_count=Count('downvote'),
            annotated_comment_count=Count('comment')
        ),
        id=product_id
    )

    # Handle possible None value from Avg:
    product.annotated_average_rating = product.annotated_average_rating or 0

    # Calculate product score:
    denominator = (product.annotated_upvote_count +
                   product.annotated_downvote_count) * product.annotated_review_count
    product.score = (
        (product.annotated_upvote_count - product.annotated_downvote_count)
          * product.annotated_average_rating /
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
                # Remove any existing downvote
                had_downvote = Downvote.objects.filter(product=product, user=request.user).exists()
                Downvote.objects.filter(product=product, user=request.user).delete()
                if had_downvote:
                    product.product_downvote_count = max(0, product.product_downvote_count - 1)
                    product.save(update_fields=['product_downvote_count'])

                # Toggle upvote
                upvote, created = Upvote.objects.get_or_create(
                    product=product,
                    user=request.user
                )
                if not created:
                    upvote.delete()
                    # Decrease upvote count
                    product.product_upvote_count = max(0, product.product_upvote_count - 1)
                    request.user.total_upvotes_by_user = max(0, request.user.total_upvotes_by_user - 1)
                    product.author_user.total_upvotes_received_by_user = max(0, product.author_user.total_upvotes_received_by_user - 1)
                    messages.success(request, 'Upvote removed.')
                else:
                    # Increase upvote count
                    product.product_upvote_count += 1
                    request.user.total_upvotes_by_user += 1
                    product.author_user.total_upvotes_received_by_user += 1
                    messages.success(request, 'Upvote added successfully.')
                product.save(update_fields=['product_upvote_count'])
                request.user.save(update_fields=['total_upvotes_by_user'])
                product.author_user.save(update_fields=['total_upvotes_received_by_user'])

            elif action == 'downvote':
                # Remove any existing upvote
                had_upvote = Upvote.objects.filter(product=product, user=request.user).exists()
                Upvote.objects.filter(product=product, user=request.user).delete()
                if had_upvote:
                    product.product_upvote_count = max(0, product.product_upvote_count - 1)
                    request.user.total_upvotes_by_user = max(0, request.user.total_upvotes_by_user - 1)
                    product.author_user.total_upvotes_received_by_user = max(0, product.author_user.total_upvotes_received_by_user - 1)
                    product.save(update_fields=['product_upvote_count'])
                    request.user.save(update_fields=['total_upvotes_by_user'])
                    product.author_user.save(update_fields=['total_upvotes_received_by_user'])

                # Toggle downvote
                downvote, created = Downvote.objects.get_or_create(
                    product=product,
                    user=request.user
                )
                if not created:
                    downvote.delete()
                    # Decrease downvote count
                    product.product_downvote_count = max(0, product.product_downvote_count - 1)
                    request.user.total_downvotes_by_user = max(0, request.user.total_downvotes_by_user - 1)
                    product.author_user.total_downvotes_received_by_user = max(0, product.author_user.total_downvotes_received_by_user - 1)
                    messages.success(request, 'Downvote removed.')
                else:
                    # Increase downvote count
                    product.product_downvote_count += 1
                    request.user.total_downvotes_by_user += 1
                    product.author_user.total_downvotes_received_by_user += 1
                    messages.success(request, 'Downvote added successfully.')
                product.save(update_fields=['product_downvote_count'])
                request.user.save(update_fields=['total_downvotes_by_user'])
                product.author_user.save(update_fields=['total_downvotes_received_by_user'])

            elif action == 'comment':
                comment_text = request.POST.get('comment_text')
                if comment_text:
                    Comment.objects.create(
                        product=product,
                        user=request.user,
                        comment_text=comment_text
                    )
                    # Increase comment count
                    product.product_comment_count += 1
                    request.user.total_comments_by_user += 1
                    product.author_user.total_comments_received_by_user += 1
                    product.save(update_fields=['product_comment_count'])
                    request.user.save(update_fields=['total_comments_by_user'])
                    product.author_user.save(update_fields=['total_comments_received_by_user'])
                    messages.success(request, 'Comment added successfully.')
                else:
                    messages.error(request, 'Comment cannot be empty.')

            elif action == 'review':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    # Increase review count
                    request.user.total_reviews_by_user += 1
                    request.user.save(update_fields=['total_reviews_by_user'])
                    messages.success(request, 'Review added successfully.')
                else:
                    messages.error(request, 'Please provide a valid review.')

            elif action == 'report':
                # Check if user has already reported
                if not Report.objects.filter(product=product, user=request.user).exists():
                    Report.objects.create(
                        product=product,
                        user=request.user
                    )
                    # Increase report count
                    product.product_report_count += 1
                    request.user.total_reports_by_user += 1
                    product.author_user.total_reports_received_by_user += 1
                    product.save(update_fields=['product_report_count'])
                    request.user.save(update_fields=['total_reports_by_user'])
                    product.author_user.save(update_fields=['total_reports_received_by_user'])
                    messages.success(request, 'Product reported successfully.')
                else:
                    messages.warning(request, 'You have already reported this product.')

            # Update total interaction counts for product
            product.product_interaction_count = (
                product.product_upvote_count +
                product.product_downvote_count +
                product.product_comment_count +
                product.product_report_count
            )
            product.save(update_fields=['product_interaction_count'])

            # Update user's total interactions
            request.user.total_interaction_by_user = (
                request.user.total_upvotes_by_user +
                request.user.total_downvotes_by_user +
                request.user.total_comments_by_user +
                request.user.total_reviews_by_user +
                request.user.total_reports_by_user
            )
            request.user.save(update_fields=['total_interaction_by_user'])

            # Update author's total received interactions
            product.author_user.total_interactions_received_by_user = (
                product.author_user.total_upvotes_received_by_user +
                product.author_user.total_downvotes_received_by_user +
                product.author_user.total_comments_received_by_user +
                product.author_user.total_reports_received_by_user
            )
            product.author_user.save(update_fields=['total_interactions_received_by_user'])

            return redirect('app:product_detail', product_id=product.id)

    # Check if current user has interacted with the product
    if request.user.is_authenticated:
        user_has_upvoted = Upvote.objects.filter(product=product, user=request.user).exists()
        user_has_downvoted = Downvote.objects.filter(product=product, user=request.user).exists()
        user_has_commented = Comment.objects.filter(product=product, user=request.user).exists()
        user_has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
    else:
        user_has_upvoted = user_has_downvoted = user_has_commented = user_has_reviewed = False

    # Fetch reviews along with their authors and timestamps
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-timestamp')

    context = {
        'product': product,
        'reviews': reviews,
        'user_has_upvoted': user_has_upvoted,
        'user_has_downvoted': user_has_downvoted,
        'user_has_commented': user_has_commented,
        'user_has_reviewed': user_has_reviewed,
        'review_form': ReviewForm(),
        'product_score': product.score,
        'product_average_rating': product.annotated_average_rating,
        'product_upvote_count': product.annotated_upvote_count,
        'product_downvote_count': product.annotated_downvote_count,
        'product_review_count': product.annotated_review_count,
        'product_comment_count': product.annotated_comment_count,
    }

    return render(request, 'app/product_detail.html', context)

@login_required
def add_product_view(request):
    """View for adding a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author_user = request.user
            product.save()

            # Update user's total entries
            request.user.total_entries_by_user += 1
            request.user.save(update_fields=['total_entries_by_user'])

            messages.success(request, 'Product added successfully!')
            return redirect('app:product_detail', product_id=product.product_id)
    else:
        form = ProductForm()

    context = {
        'form': form,
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'app/add_product.html', context)
