"""URL configuration for the app."""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('feed/', views.feed_view, name='feed'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('product/<int:product_id>/upvote/', views.feed_upvote_product_view, name='feed_upvote_product'),
    path('product/<int:product_id>/downvote/', views.feed_downvote_product_view, name='feed_downvote_product'),
    path('product/<int:product_id>/report/', views.feed_report_product_view, name='feed_report_product'),
    path('product/<int:product_id>/comment/', views.feed_comment_product_view, name='feed_comment_product'),
    path('lists/', views.lists_view, name='lists'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
