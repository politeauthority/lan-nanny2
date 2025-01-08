"""
    Bookmarky Api
    Controller Model
    Bookmark

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.bookmark import Bookmark
from lan_nanny.api.models.bookmark_tag import BookmarkTag
from lan_nanny.api.models.bookmark_track import BookmarkTrack
from lan_nanny.api.collects.auto_features import AutoFeatures
from lan_nanny.api.collects.bookmark_tags import BookmarkTags
from lan_nanny.api.utils.auto_features import AutoFeatures as UtilAutoFeatures
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import api_util
from lan_nanny.api.utils import glow

ctrl_bookmark = Blueprint("bookmark", __name__, url_prefix="/bookmark")


@ctrl_bookmark.route("")
@ctrl_bookmark.route("/")
@ctrl_bookmark.route("/<bookmark_id>", methods=["GET"])
@auth.auth_request
def get_model(bookmark_id: int = None) -> Response:
    """GET operation for a bookmark.
    GET /user
    """
    logging.info("GET - /bookmark")
    data = ctrl_base.get_model(Bookmark, bookmark_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_bookmark.route("", methods=["POST"])
@ctrl_bookmark.route("/", methods=["POST"])
@ctrl_bookmark.route("/<bookmark_id>", methods=["POST"])
@ctrl_bookmark.route("/<bookmark_id>/", methods=["POST"])
@auth.auth_request
def post_model(bookmark_id: int = None):
    """POST operation for a Bookmark model.
    POST /bookmark
    @todo: This needs to be locked down to only allow users to delete their own Tag relationships
    """
    data = {
        "user_id": glow.user["user_id"]
    }
    logging.info("POST Bookmark")
    if isinstance(bookmark_id, str):
        try:
            bookmark_id = int(bookmark_id)
        except ValueError:
            return {"status": "error"}, 400
    r_args = api_util.get_post_data()
    if r_args and "tag_id" in r_args:
        BookmarkTag().create(bookmark_id, r_args["tag_id"])
    if r_args and "tag_id_remove" in r_args:
        BookmarkTag().remove(bookmark_id, r_args["tag_id_remove"])
    data.update(r_args)
    response, return_code = ctrl_base.post_model(Bookmark, bookmark_id, data)
    if isinstance(response, Response):
        return response, return_code
    ret_data = response
    if ret_data["status"] == "success":
        _handle_auto_features(ret_data)
    return jsonify(ret_data), return_code


@ctrl_bookmark.route("/<bookmark_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(bookmark_id: int = None):
    """DELETE operation for a Bookmark model.
    DELETE /bookmark
    Dont let a user delete a Bookmark they do not own, however we will send back a 404 in that
    event.
    @todo: Move BookmarkTag deletion logic down to the Tag model level, not the controller level so
    that it works outside of just API requests and is more encompassing
    """
    data = {
        "status": "Error",
        "message": "Could not find Bookmark ID: %s" % bookmark_id
    }
    logging.debug("DELETE Bookmark")
    bookmark = Bookmark()
    if not bookmark.get_by_id(bookmark_id):
        return jsonify(data), 404
    if bookmark.user_id != glow.user["user_id"]:
        logging.warning("User %s tried to delete Bookmark beloning to User: %s" % (
            glow.user["user_id"],
            bookmark.user_id
        ))
        return jsonify(data), 404
    bts_col = BookmarkTags()
    bts_col.delete_for_bookmark(bookmark.id)
    return ctrl_base.delete_model(Bookmark, bookmark.id)


@ctrl_bookmark.route("/click-track/<bookmark_id>", methods=["POST"])
@ctrl_bookmark.route("/click-track/<bookmark_id>/", methods=["POST"])
@auth.auth_request
def click_track(bookmark_id: int = None):
    """Operation for counting clicks on a link, adding them as a meta object to the Bookmark entity.
    POST /bookmark/click-track/355
    """
    data = {
        "status": "success",
        "message": "Updated Bookmark succesffuly"
    }
    bookmark = Bookmark()
    if not bookmark.get_by_id(bookmark_id):
        data["status"] = "error"
        data["message"] = "Bookmark not found"
        return jsonify(data), 404
    bookmark.load_meta()
    if "click-count" not in bookmark.metas:
        bookmark.metas["click-count"] = 1
    else:
        bookmark.metas["click-count"].value += 1
    bookmark.save()
    # Save the Bookmark Track record
    bookmark_track = BookmarkTrack()
    bookmark_track.bookmark_id = bookmark_id
    bookmark_track.user_id = glow.user["user_id"]
    bookmark_track.save()
    return bookmark.json()


def _handle_auto_features(data: dict) -> bool:
    """When we add a Bookmark, run through all the AutoFeatures and apply all of those which fit
    the Bookmark.
    """
    bookmark = Bookmark()
    bookmark.build_from_dict(data["object"])
    afs = AutoFeatures().get_by_user_id(glow.user["user_id"])
    if UtilAutoFeatures(glow.user["user_id"], afs).run(bookmark):
        logging.info("Auto Features ran successfully for %s" % bookmark)
        return True
    else:
        logging.error("Failed to run Auto Features for %s" % bookmark)
        return False

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_models/ctrl_bookmark.py
