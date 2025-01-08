"""
    Bookmark Api
    Controller Collection
    Bookmarks

"""
import logging

from flask import Blueprint, jsonify, request, Response

from lan_nanny.api.collects.devices import Bookmarks
from lan_nanny.api.collects.tags import Tags
from lan_nanny.api.collects.bookmark_tracks import BookmarkTracks
from lan_nanny.api.models.tag import Tag
from lan_nanny.api.models.directory import Directory
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import glow

ctrl_bookmarks = Blueprint("bookmarks", __name__, url_prefix="/bookmarks")

PER_PAGE = 20


@ctrl_bookmarks.route("")
@ctrl_bookmarks.route("/")
@auth.auth_request
def index() -> Response:
    """Get Bookmarks, along with associated Tags where they exist."""
    logging.info("\n\nStart Bookmarks Collection")
    extra_args = {
        "fields": {
            "user_id": {
                "value": glow.user["user_id"],
                "op": "=",
                "overrideable": False
            }
        },
        "order_by": {},
        "limit": None
    }
    user_display_hidden_search = _get_user_display_hidden()
    if user_display_hidden_search:
        extra_args["fields"].update(user_display_hidden_search)
        logging.debug("\n\nEXTRA ARGS %s\n\n" % extra_args["fields"])
    data = ctrl_collection_base.get(Bookmarks, extra_args)
    data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])
    logging.info("END Bookmarks Collection\n\n")
    return jsonify(data)


@ctrl_bookmarks.route("/search")
@auth.auth_request
def search() -> Response:
    """Search through Bookmarks from a wide variety of input."""
    data = {
        "objects": [],
        "object_type": "bookmark",
        "message": "No search criteria",
        "status": "Error",
        "info": {
            "current_page": 1,
            "last_page": None,
            "per_page": PER_PAGE,
            "total_objects": 0,
        }
    }
    search_args = request.args
    if "query" not in search_args:
        logging.warning("No search criteria for search")
        return jsonify(data)
    if "page" in search_args:
        if search_args["page"] and search_args["page"].isdigit():
            current_page = int(search_args["page"])
    else:
        current_page = 1
    search_phrase = f"%{search_args['query']}%"
    query = _gen_search_query(search_phrase, current_page)
    logging.debug(f"\n\nSEARCHING\n{search_args}\n\n")
    bookmarks_col = Bookmarks()
    # Get the Bookmarks
    data["objects"] = bookmarks_col.get_query(query["sql"], query["params"])
    data["objects"] = bookmarks_col.make_json(data["objects"])
    if data["objects"]:
        data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])

    # Get the pagination info
    data["info"] = bookmarks_col.get_pagination_info(query, current_page, PER_PAGE)

    data["message"] = "Search successful"
    data["status"] = "Success"

    return jsonify(data)


@ctrl_bookmarks.route("/by-tag")
@auth.auth_request
def by_tag() -> Response:
    """Get Bookmarks by a Tag.
    @todo: This feels lazy, this should be done better probably.
        - If tag slug can't be found return a 404
    """
    data = {
        "info": {
            "current_page": 1,
        },
        "objects": []
    }
    search_args = request.args
    tag = Tag()
    tag.get_by_slug(search_args["tag_slug"])
    bookmarks_col = Bookmarks()
    bookmarks = bookmarks_col.get_by_tag_id(tag.id)
    bookmarks_json = bookmarks_col.make_json(bookmarks)
    data["objects"] = Tags().get_tags_for_bookmarks(bookmarks_json)
    data["info"]["total_objects"] = len(data["objects"])
    data["info"]["tag"] = tag.json()
    return jsonify(data)


@ctrl_bookmarks.route("/by-dir")
@auth.auth_request
def by_dir() -> Response:
    """Get Bookmarks by a Directory.
    @todo: This feels lazy, this should be done better probably.
        - If dir slug can't be found return a 404
    """
    data = {
        "info": {
            "current_page": 1,
        },
        "objects": []
    }
    search_args = request.args
    directory = Directory()
    directory.get_by_slug(search_args["dir_slug"])
    bookmarks_col = Bookmarks()
    bookmarks = bookmarks_col.get_by_dir_id(directory.id)
    bookmarks_json = bookmarks_col.make_json(bookmarks)
    data["objects"] = Tags().get_tags_for_bookmarks(bookmarks_json)
    data["info"]["total_objects"] = len(data["objects"])
    data["info"]["dir"] = directory.json()
    return jsonify(data)


@ctrl_bookmarks.route("/popular")
@ctrl_bookmarks.route("/popular/")
@auth.auth_request
def get_most_clicked() -> Response:
    """Get the most clicked Bookmarks for a logged in User.
    @todo: Support date range feature, getting popular Bookmarks _since_ a given UTC datetime.
    """
    logging.info("Running Popular Search")
    bookmark_ids = BookmarkTracks().get_popular_bookmarks(glow.user["user_id"])
    bookmark_ids_search = []
    for b_id in bookmark_ids:
        bookmark_ids_search.append(b_id[0])
    bookmarks_collected = Bookmarks().get_by_ids(bookmark_ids_search)
    bookmarks = []
    for b in bookmarks_collected:
        bookmarks.append(b.json())
    data = {
        "objects": bookmarks,
        "info": {
            "total_objects": len(bookmarks)
        }
    }
    return jsonify(data)


def _gen_search_query(search_phrase: str, page: int) -> dict:
    """Generate the search query SQL. Helper function for search function."""
    if page == 1:
        offset = 0
    else:
        offset = (page * PER_PAGE) - PER_PAGE

    query = {
        "sql": None,
        "params": ()
    }
    query["sql"] = f"""
        SELECT *
        FROM bookmarks
        WHERE
            user_id = %s AND
            (
                url ILIKE %s OR
                title ILIKE %s OR
                notes ILIKE %s
            )
        ORDER BY created_ts DESC
        LIMIT 20 OFFSET {offset};
    """
    query["params"] = (glow.user["user_id"], search_phrase, search_phrase, search_phrase)
    return query


def _get_user_display_hidden() -> dict:
    """Get the argument for whether or not we display hidden bookmarks."""
    user = glow.user["obj"]
    if "display_hidden" not in user.metas:
        return {}

    if user.metas["display_hidden"].value == True:
        return {}
    else:
        ret = {
            "hidden": {
                "value": False,
                "op": "=",
                "overrideable": False
            }
        }
        logging.warning("Will display hidden Bookmarks with this query!")
        return ret

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/collections/
#           ctrl_bookmarks.py
