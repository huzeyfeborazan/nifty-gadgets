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
    list_display = ('username', 'email', 'date_joined', 'user_is_trending')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_is_trending', 'user_is_featured', 'user_is_affiliate', 'is_staff', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = (
        'product_title',
        'product_category',
        'author_user',
        'product_price',
        'created_at',
        'trending',
        'popular',
        'controversial',
        'new'
    )
    search_fields = ('product_title', 'product_description')
    list_filter = ('product_category',)

    @admin.display(boolean=True, description='Trending')
    def trending(self, obj):
        return obj in Product.get_trending_products()

    @admin.display(boolean=True, description='Popular')
    def popular(self, obj):
        return obj in Product.get_popular_products()

    @admin.display(boolean=True, description='Controversial')
    def controversial(self, obj):
        return obj in Product.get_controversial_products()

    @admin.display(boolean=True, description='New')
    def new(self, obj):
        return obj in Product.get_new_products()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ('product', 'user', 'review_score', 'created_at')
    search_fields = ('review_title', 'review_content')
    list_filter = ('review_score',)


@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    """Admin configuration for Upvote model."""
    list_display = ('product', 'user', 'created_at')
    search_fields = ('product__product_title', 'user__username')


@admin.register(Downvote)
class DownvoteAdmin(admin.ModelAdmin):
    """Admin configuration for Downvote model."""
    list_display = ('product', 'user', 'created_at')
    search_fields = ('product__product_title', 'user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""
    list_display = ('product', 'user', 'created_at')
    search_fields = ('comment_content', 'product__product_title', 'user__username')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin configuration for Report model."""
    list_display = ('product', 'user', 'created_at')
    search_fields = ('product__product_title', 'user__username')
