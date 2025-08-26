"""Admin configuration for the Nifty Gadgets application."""

from django.contrib import admin
from .models import (
    User,
    Product,
    Review,
    Upvote,
    Downvote,
    Comment,
    Report
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model."""
    list_display = ('username', 'user_email', 'created_at', 'user_is_trending')
    search_fields = ('username', 'user_email')
    list_filter = ('user_is_trending', 'user_is_featured', 'user_is_affiliate')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = (
        'product_title',
        'product_category',
        'author_user',
        'product_price',
        'created_at',
        'product_is_trending'
    )
    search_fields = ('product_title', 'product_description')
    list_filter = (
        'product_is_trending',
        'product_is_featured',
        'product_is_promoted',
        'product_is_controversial',
        'product_is_new'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ('product', 'user', 'review_score', 'timestamp')
    search_fields = ('review_title', 'review_content')
    list_filter = ('review_score',)


@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    """Admin configuration for Upvote model."""
    list_display = ('product', 'user', 'timestamp')
    search_fields = ('product__product_title', 'user__username')


@admin.register(Downvote)
class DownvoteAdmin(admin.ModelAdmin):
    """Admin configuration for Downvote model."""
    list_display = ('product', 'user', 'timestamp')
    search_fields = ('product__product_title', 'user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""
    list_display = ('product', 'user', 'timestamp')
    search_fields = ('comment_content', 'product__product_title', 'user__username')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin configuration for Report model."""
    list_display = ('product', 'user', 'timestamp')
    search_fields = ('product__product_title', 'user__username')
