"""
    Bookmarky Api
    Controller Model
    Vendor

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.vendor import Vendor
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import api_util
from lan_nanny.api.utils import glow

ctrl_vendor = Blueprint("vendor", __name__, url_prefix="/vendor")


@ctrl_vendor.route("")
@ctrl_vendor.route("/")
@ctrl_vendor.route("/<vendor_id>", methods=["GET"])
@auth.auth_request
def get_model(vendor_id: int = None) -> Response:
    """GET operation for a Device.
    GET /vendor
    """
    logging.info("GET - /vendor")
    data = ctrl_base.get_model(Vendor, vendor_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_vendor.route("", methods=["POST"])
@ctrl_vendor.route("/", methods=["POST"])
@ctrl_vendor.route("/<vendor_id>", methods=["POST"])
@ctrl_vendor.route("/<vendor_id>/", methods=["POST"])
@auth.auth_request
def post_model(vendor_id: int = None):
    """POST operation for a Device model.
    POST /vendor
    """
    data = {
        "user_id": glow.user["user_id"]
    }
    logging.info("POST Vendor")
    if isinstance(vendor_id, str):
        try:
            vendor_id = int(vendor_id)
        except ValueError:
            return {"status": "error"}, 400
    r_args = api_util.get_post_data()
    data.update(r_args)
    response, return_code = ctrl_base.post_model(Vendor, vendor_id, data)
    if isinstance(response, Response):
        return response, return_code
    ret_data = response
    return jsonify(ret_data), return_code


@ctrl_vendor.route("/<vendor_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(vendor_id: int = None):
    """DELETE operation for a Bookmark model.
    DELETE /vendor_id
    Dont let a user delete a Bookmark they do not own, however we will send back a 404 in that
    event.
    @todo: Move BookmarkTag deletion logic down to the Tag model level, not the controller level so
    that it works outside of just API requests and is more encompassing
    """
    data = {
        "status": "Error",
        "message": "Could not find Device ID: %s" % vendor_id
    }
    logging.debug("DELETE Bookmark")
    vendor = Vendor()
    if not vendor.get_by_id(vendor_id):
        return jsonify(data), 404
    return ctrl_base.delete_model(Vendor, vendor.id)


# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/ctrl_models/ctrl_vendor.py
