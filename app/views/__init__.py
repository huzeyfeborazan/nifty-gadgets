"""Views package initialization."""

from app.views.auth_views import register_view, login_view, logout_view
from app.views.core_views import home, dashboard_view, lists_view
from app.views.feed_views import feed_view
from app.views.feed_interaction_views import (
    feed_upvote_product_view,
    feed_downvote_product_view,
    feed_report_product_view,
    feed_comment_product_view
)
from app.views.product_views import product_detail_view, add_product_view

__all__ = [
    'register_view',
    'login_view',
    'logout_view',
    'home',
    'dashboard_view',
    'feed_view',
    'feed_upvote_product_view',
    'feed_downvote_product_view',
    'feed_report_product_view',
    'feed_comment_product_view',
    'product_detail_view',
    'add_product_view',
    'lists_view'
]
