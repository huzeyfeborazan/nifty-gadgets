''' Models for the Nifty Gadgets application. '''
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Model representing a user in the system."""
    user_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_name = models.TextField(default='')
    user_lastname = models.TextField(default='')
    user_date_of_birth = models.DateField(null=True, blank=True)
    user_age = models.IntegerField(default=0)
    user_email = models.EmailField(unique=True)
    user_security_email = models.EmailField(default='')
    user_phone_number = models.CharField(max_length=20, default='')
    user_bio = models.TextField(default='')
    total_entries_by_user = models.IntegerField(default=0)
    total_upvotes_by_user = models.IntegerField(default=0)
    total_downvotes_by_user = models.IntegerField(default=0)
    total_reviews_by_user = models.IntegerField(default=0)
    total_comments_by_user = models.IntegerField(default=0)
    total_reports_by_user = models.IntegerField(default=0)
    total_interaction_by_user = models.IntegerField(default=0)
    total_upvotes_received_by_user = models.IntegerField(default=0)
    total_downvotes_received_by_user = models.IntegerField(default=0)
    total_comments_received_by_user = models.IntegerField(default=0)
    total_reports_received_by_user = models.IntegerField(default=0)
    total_interactions_received_by_user = models.IntegerField(default=0)
    user_score = models.FloatField(default=0)
    user_is_trending = models.BooleanField(default=False)
    user_is_featured = models.BooleanField(default=False)
    user_is_affiliate = models.BooleanField(default=False)


class ProductCategory(models.Model):
    """Model representing a product category."""
    product_category_id = models.AutoField(primary_key=True)
    product_category_title = models.CharField(max_length=255, unique=True)


class Product(models.Model):
    """Model representing a product."""
    product_id = models.AutoField(primary_key=True)
    product_title = models.CharField(max_length=255)
    product_description = models.TextField(default='')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                         related_name='products')
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    product_upvote_count = models.IntegerField(default=0)
    product_downvote_count = models.IntegerField(default=0)
    product_comment_count = models.IntegerField(default=0)
    product_interaction_count = models.IntegerField(default=0)
    product_report_count = models.IntegerField(default=0)
    product_average_rating = models.FloatField(default=0)
    product_total_score = models.FloatField()
    product_is_trending = models.BooleanField(default=False)
    product_is_featured = models.BooleanField(default=False)
    product_is_promoted = models.BooleanField(default=False)
    product_is_controversial = models.BooleanField(default=False)
    product_is_new = models.BooleanField(default=False)

    def update_trending_status(self):
        """Update the trending flag."""
        if self.product_upvote_count > 50 or self.product_comment_count > 50:
            self.product_is_trending = True
            self.save(update_fields=['product_is_trending'])

    def update_controversial_status(self):
        """Update the controversial flag."""
        if self.product_upvote_count > 50 and self.product_downvote_count > 50:
            self.product_is_controversial = True
            self.save(update_fields=['product_is_controversial'])

    def update_featured_status(self):
        """Update the featured flag."""


    def update_new_status(self):
        """Update the new flag (within 5 days)."""
        if self.created_at >= timezone.now() - timedelta(days=5):
            self.product_is_new = True
            self.save(update_fields=['product_is_new'])

class Review(models.Model):
    """Model representing a product review."""
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews')
    timestamp = models.DateTimeField(auto_now_add=True)
    review_title = models.CharField(max_length=255, default='')
    review_content = models.TextField(default='')
    review_score = models.IntegerField(default=0)


class Upvote(models.Model):
    """Model representing a product upvote."""
    upvote_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='upvotes')
    timestamp = models.DateTimeField(auto_now_add=True)


class Downvote(models.Model):
    """Model representing a product downvote."""
    downvote_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='downvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='downvotes')
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Model representing a product comment."""
    comment_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField(default='')


class Report(models.Model):
    """Model representing a product report."""
    report_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reports')
    timestamp = models.DateTimeField(auto_now_add=True)
