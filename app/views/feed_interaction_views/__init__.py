"""Feed interaction views package initialization."""

from app.views.feed_interaction_views.upvotes_views import feed_upvote_product_view
from app.views.feed_interaction_views.downvotes_views import feed_downvote_product_view
from app.views.feed_interaction_views.reports_views import feed_report_product_view
from app.views.feed_interaction_views.comments_views import feed_comment_product_view

__all__ = [
    'feed_upvote_product_view',
    'feed_downvote_product_view',
    'feed_report_product_view',
    'feed_comment_product_view'
]
