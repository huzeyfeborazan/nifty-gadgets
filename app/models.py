''' Models for the Nifty Gadgets application. '''
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import F
from django.db.models import Count

class User(AbstractUser):
    """Model representing a user in the system."""

    # Custom fields that don't duplicate AbstractUser functionality
    user_age = models.IntegerField(default=0)
    user_security_email = models.EmailField(default='')
    user_phone_number = models.CharField(max_length=20, default='')
    user_bio = models.TextField(default='')

    # User status flags
    user_is_trending = models.BooleanField(default=False)
    user_is_featured = models.BooleanField(default=False)
    user_is_affiliate = models.BooleanField(default=False)

    # Override email to make it unique (AbstractUser's email is not unique by default)
    email = models.EmailField(unique=True)

    def get_total_products(self):
        """Get total products created by this user."""
        return self.products.count()

    def get_total_reviews(self):
        """Get total reviews written by this user."""
        return self.reviews.count()

    def get_total_upvotes_given(self):
        """Get total upvotes given by this user."""
        return self.upvotes.count()

    def get_total_downvotes_given(self):
        """Get total downvotes given by this user."""
        return self.downvotes.count()

    def get_total_comments(self):
        """Get total comments made by this user."""
        return self.comments.count()

    def get_total_reports(self):
        """Get total reports made by this user."""
        return self.reports.count()

    def get_total_upvotes_received(self):
        """Get total upvotes received on user's products."""
        return Upvote.objects.filter(product__author_user=self).count()

    def get_total_downvotes_received(self):
        """Get total downvotes received on user's products."""
        return Downvote.objects.filter(product__author_user=self).count()

    def get_total_comments_received(self):
        """Get total comments received on user's products."""
        return Comment.objects.filter(product__author_user=self).count()

    def get_total_reports_received(self):
        """Get total reports received on user's products."""
        return Report.objects.filter(product__author_user=self).count()

class Product(models.Model):
    """Model representing a product."""
    product_title = models.CharField(max_length=255)
    product_description = models.TextField(default='')

    CATEGORY_CHOICES = [
        ('productivity_tools', 'Productivity Tools'),
        ('mobile_accessories', 'Mobile Accessories'),
        ('smart_home_essentials', 'Smart Home Essentials'),
        ('gaming_accessories', 'Gaming Accessories'),
        ('audio_accessories', 'Audio Accessories'),
        ('camera_accessories', 'Camera Accessories'),
        ('office_essentials', 'Office Essentials'),
        ('travel_essentials', 'Travel Essentials'),
        ('health_and_fitness', 'Health and Fitness'),
        ('home_and_garden', 'Home and Garden'),
        ('other', 'Other'),
    ]
    product_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    product_link = models.URLField(max_length=500, blank=True, null=True, help_text="Link to purchase the product")
    author_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    product_upvote_count = models.IntegerField(default=0)
    product_downvote_count = models.IntegerField(default=0)
    product_comment_count = models.IntegerField(default=0)
    product_interaction_count = models.IntegerField(default=0)
    product_report_count = models.IntegerField(default=0)
    product_average_rating = models.FloatField(default=0)
    product_score = models.FloatField(default=0)

    @classmethod
    def get_trending_products(cls):
        """Get top 7 products by engagement (upvotes + comments)."""
        return cls.objects.annotate(
            trending_score=F('product_upvote_count') + F('product_comment_count')
        ).order_by('-trending_score')[:7]

    @classmethod
    def get_controversial_products(cls):
        """Get top 7 controversial products (with both upvotes and downvotes)."""
        from django.db.models import Case, When, Value, IntegerField

        return cls.objects.annotate(
            upvotes_count=Count('upvotes'),
            downvotes_count=Count('downvotes')
        ).filter(upvotes_count__gt=0, downvotes_count__gt=0).annotate(
            controversy_score=Case(
                When(upvotes_count__gte=F('downvotes_count'),
                     then=F('upvotes_count') + F('downvotes_count') - (F('upvotes_count') - F('downvotes_count'))),
                default=F('upvotes_count') + F('downvotes_count') - (F('downvotes_count') - F('upvotes_count')),
                output_field=IntegerField()
            )
        ).order_by('-controversy_score')[:7]

    @classmethod
    def get_new_products(cls):
        """Get products created within last 7 days."""
        return cls.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))

    @classmethod
    def get_popular_products(cls):
        """Get top 10 products by total interactions."""
        return cls.objects.annotate(
            total_interactions=F('product_upvote_count') + F('product_downvote_count') + F('product_comment_count')
        ).order_by('-total_interactions')[:10]


class Review(models.Model):
    """Model representing a product review."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    review_title = models.CharField(max_length=255, default='')
    review_content = models.TextField(default='')
    review_score = models.IntegerField(default=0)


class Upvote(models.Model):
    """Model representing a product upvote."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)


class Downvote(models.Model):
    """Model representing a product downvote."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='downvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='downvotes')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Model representing a product comment."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField(default='')


class Report(models.Model):
    """Model representing a product report."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
