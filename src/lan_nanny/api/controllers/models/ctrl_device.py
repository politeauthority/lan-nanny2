"""
    Bookmarky Api
    Controller Model
    Device

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.device import Device
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import api_util
from lan_nanny.api.utils import glow

ctrl_device = Blueprint("device", __name__, url_prefix="/device")


@ctrl_device.route("")
@ctrl_device.route("/")
@ctrl_device.route("/<device_id>", methods=["GET"])
@auth.auth_request
def get_model(device_id: int = None) -> Response:
    """GET operation for a Device.
    GET /device
    """
    logging.info("GET - /device")
    data = ctrl_base.get_model(Device, device_id)
    if "object" in data:
        dm_col = DeviceMacs()
        device_macs = dm_col.get_by_device_id(data["object"]["id"])
        device_macs_ret = []
        if device_macs:
            for dm in device_macs:
                # device_macs_ret.append(dm.id)
                device_macs_ret.append(dm.json())
        data["object"]["device_macs"] = device_macs_ret
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_device.route("", methods=["POST"])
@ctrl_device.route("/", methods=["POST"])
@ctrl_device.route("/<device_id>", methods=["POST"])
@ctrl_device.route("/<device_id>/", methods=["POST"])
@auth.auth_request
def post_model(device_id: int = None):
    """POST operation for a Device model.
    POST /device
    """
    data = {
        "user_id": glow.user["user_id"]
    }
    logging.info("POST Devuce")
    if isinstance(device_id, str):
        try:
            device_id = int(device_id)
        except ValueError:
            return {"status": "error"}, 400
    r_args = api_util.get_post_data()
    data.update(r_args)
    response, return_code = ctrl_base.post_model(Device, device_id, data)
    if isinstance(response, Response):
        return response, return_code
    ret_data = response
    return jsonify(ret_data), return_code


@ctrl_device.route("/<device_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(device_id: int = None):
    """DELETE operation for a Bookmark model.
    DELETE /device_id
    Dont let a user delete a Bookmark they do not own, however we will send back a 404 in that
    event.
    @todo: Move BookmarkTag deletion logic down to the Tag model level, not the controller level so
    that it works outside of just API requests and is more encompassing
    """
    data = {
        "status": "Error",
        "message": "Could not find Device ID: %s" % device_id
    }
    logging.debug("DELETE Bookmark")
    device = Device()
    if not device.get_by_id(device_id):
        return jsonify(data), 404
    if device.user_id != glow.user["user_id"]:
        logging.warning("User %s tried to delete Bookmark beloning to User: %s" % (
            glow.user["user_id"],
            device.user_id
        ))
        return jsonify(data), 404
    return ctrl_base.delete_model(Device, device.id)


# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/ctrl_models/ctrl_device.py
