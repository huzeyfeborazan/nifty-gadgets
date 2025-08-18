"""Product interaction views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect

from app.forms import ReviewForm
from app.models import Product, Upvote, Downvote, Comment, Report

@login_required
def handle_product_interaction(request, product_id):
    """Handle all product interactions (upvote, downvote, comment, review, report)."""
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')

    if action == 'upvote':
        handle_upvote(request, product)
    elif action == 'downvote':
        handle_downvote(request, product)
    elif action == 'comment':
        handle_comment(request, product)
    elif action == 'review':
        handle_review(request, product)
    elif action == 'report':
        handle_report(request, product)

    update_interaction_counts(product, request.user)
    return redirect('app:product_detail', product_id=product.id)

@transaction.atomic
def handle_upvote(request, product):
    """Handle product upvote."""
    # Remove any existing downvote
    downvote_qs = Downvote.objects.filter(product=product, user=request.user)
    if downvote_qs.exists():
        downvote_qs.delete()
        product.product_downvote_count = max(0, product.product_downvote_count - 1)
        product.save(update_fields=['product_downvote_count'])
        request.user.save(update_fields=['total_downvotes_by_user'])
        product.author_user.save(update_fields=['total_downvotes_received_by_user'])

    # Toggle upvote
    upvote, created = Upvote.objects.get_or_create(
        product=product,
        user=request.user
    )
    if created:
        # Increase upvote count
        product.product_upvote_count += 1
        request.user.total_upvotes_by_user += 1
        product.author_user.total_upvotes_received_by_user += 1

    elif not created:
        # Decrease upvote count
        upvote.delete()
        product.product_upvote_count = max(0, product.product_upvote_count - 1)
        request.user.total_upvotes_by_user = max(0, request.user.total_upvotes_by_user - 1)
        product.author_user.total_upvotes_received_by_user = max(0, product.author_user.total_upvotes_received_by_user - 1)

    product.save(update_fields=['product_upvote_count'])
    request.user.save(update_fields=['total_upvotes_by_user'])
    product.author_user.save(update_fields=['total_upvotes_received_by_user'])

@transaction.atomic
def handle_downvote(request, product):
    """Handle product downvote."""
    # Remove any existing upvote
    upvote_qs = Upvote.objects.filter(product=product, user=request.user)
    if upvote_qs.exists():
        upvote_qs.delete()
        product.product_upvote_count = max(0, product.product_upvote_count - 1)
        product.save(update_fields=['product_upvote_count'])
        request.user.save(update_fields=['total_upvotes_by_user'])
        product.author_user.save(update_fields=['total_upvotes_received_by_user'])

    # Toggle downvote
    downvote, created = Downvote.objects.get_or_create(
        product=product,
        user=request.user
    )
    if created:
        # Increase downvote count
        product.product_downvote_count += 1
        request.user.total_downvotes_by_user += 1
        product.author_user.total_downvotes_received_by_user += 1
    else:
        # Decrease downvote count
        downvote.delete()
        product.product_downvote_count = max(0, product.product_downvote_count - 1)
        request.user.total_downvotes_by_user = max(0, request.user.total_downvotes_by_user - 1)
        product.author_user.total_downvotes_received_by_user = max(0, product.author_user.total_downvotes_received_by_user - 1)

    product.save(update_fields=['product_downvote_count'])
    request.user.save(update_fields=['total_downvotes_by_user'])
    product.author_user.save(update_fields=['total_downvotes_received_by_user'])

@transaction.atomic
def handle_comment(request, product):
    """Handle product comment."""
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

@transaction.atomic
def handle_review(request, product):
    """Handle product review."""
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

@transaction.atomic
def handle_report(request, product):
    """Handle product report."""
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

def update_product_interaction_count(product):
    """Update total interaction counts for a product."""
    product.product_interaction_count = (
        product.product_upvote_count +
        product.product_downvote_count +
        product.product_comment_count +
        product.product_report_count
    )
    product.save(update_fields=['product_interaction_count'])

def update_user_interaction_count(user):
    """Update total interaction counts for a user."""
    user.total_interaction_by_user = (
        user.total_upvotes_by_user +
        user.total_downvotes_by_user +
        user.total_comments_by_user +
        user.total_reviews_by_user +
        user.total_reports_by_user
    )
    user.save(update_fields=['total_interaction_by_user'])

def update_author_received_interaction_count(author_user):
    """Update total interactions received by the author."""
    author_user.total_interactions_received_by_user = (
        author_user.total_upvotes_received_by_user +
        author_user.total_downvotes_received_by_user +
        author_user.total_comments_received_by_user +
        author_user.total_reports_received_by_user
    )
    author_user.save(update_fields=['total_interactions_received_by_user'])

def update_interaction_counts(product, user):
    """Wrapper function to update product, user, and author interaction counts."""
    update_product_interaction_count(product)
    update_user_interaction_count(user)
    update_author_received_interaction_count(product.author_user)
