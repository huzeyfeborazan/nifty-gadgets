from django.contrib import admin
from .models import Product, ProductCategory, User, Review, Comment

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'product_price', 'product_upvote_total', 'product_is_trending', 'created_at')
    list_filter = ('product_is_trending', 'product_is_featured', 'product_is_promoted', 'created_at')
    search_fields = ('product_title', 'product_description')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product_category_title',)
    search_fields = ('product_category_title',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_name', 'user_lastname', 'user_email', 'created_at')
    list_filter = ('user_is_trending', 'user_is_featured', 'user_is_affiliate')
    search_fields = ('username', 'user_name', 'user_lastname', 'user_email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review_score', 'timestamp')
    list_filter = ('review_score',)
    search_fields = ('review_text',)
