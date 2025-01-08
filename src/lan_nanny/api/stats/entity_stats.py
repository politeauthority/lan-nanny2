"""
"""

from lan_nanny.api.collects.devices import Bookmarks
from lan_nanny.api.collects.bookmark_tags import BookmarkTags
from lan_nanny.api.collects.users import Users
from lan_nanny.api.collects.tags import Tags


def get_all_entity_counts() -> dict:
    """Get the totals for all entities that we want to track."""
    data = {}
    data["bookmarks"] = Bookmarks().get_count_all()
    data["bookmark_tags"] = BookmarkTags().get_count_all()
    data["users"] = Users().get_count_all()
    data["tags"] = Tags().get_count_all()
    return data

# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/stats/entity_stats.py
