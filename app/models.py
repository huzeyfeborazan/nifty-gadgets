from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    safety_question = models.CharField(max_length=255)
    safety_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user_name = models.TextField()
    user_lastname = models.TextField()
    user_date_of_birth = models.DateField()
    user_age = models.IntegerField()
    user_email = models.EmailField(unique=True)
    user_security_email = models.EmailField()
    user_phone_number = models.CharField(max_length=20)
    user_bio = models.TextField()
    total_entries_by_user = models.IntegerField(default=0)
    total_likes_by_user = models.IntegerField(default=0)
    total_comments_by_user = models.IntegerField(default=0)
    total_interaction_by_user = models.IntegerField(default=0)
    total_likes_received_by_user = models.IntegerField(default=0)
    total_comments_received_by_user = models.IntegerField(default=0)
    total_interactions_received_by_user = models.IntegerField(default=0)
    user_score = models.FloatField()
    user_is_trending = models.BooleanField(default=False)
    user_is_featured = models.BooleanField(default=False)
    user_is_affiliate = models.BooleanField(default=False)


class ProductCategory(models.Model):
    product_category_id = models.AutoField(primary_key=True)
    product_category_title = models.CharField(max_length=255, unique=True)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_title = models.CharField(max_length=255)
    product_description = models.TextField()
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    review_title = models.CharField(max_length=255)
    review_content = models.TextField()
    review_score = models.IntegerField()


class Upvote(models.Model):
    upvote_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Downvote(models.Model):
    downvote_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
