"""
    Bookmarky Api
    Controller Model
    Device Mac

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.device_mac import DeviceMac
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import api_util


ctrl_device_mac = Blueprint("device-mac", __name__, url_prefix="/device-mac")


@ctrl_device_mac.route("")
@ctrl_device_mac.route("/")
@ctrl_device_mac.route("/<device_mac_id>", methods=["GET"])
@auth.auth_request
def get_model(device_mac_id: int = None) -> Response:
    """GET operation for a Device.
    GET /device-mac
    """
    logging.info("GET - /device-mac")
    data = ctrl_base.get_model(DeviceMac, device_mac_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_device_mac.route("", methods=["POST"])
@ctrl_device_mac.route("/", methods=["POST"])
@ctrl_device_mac.route("/<device_mac_id>", methods=["POST"])
@ctrl_device_mac.route("/<device_mac_id>/", methods=["POST"])
@auth.auth_request
def post_model(device_mac_id: int = None):
    """POST operation for a Device model.
    POST /device-mac
    """
    data = {}
    logging.info("POST Devuce")
    if isinstance(device_mac_id, str):
        try:
            device_mac_id = int(device_mac_id)
        except ValueError:
            return {"status": "error"}, 400
    r_args = api_util.get_post_data()
    data.update(r_args)
    response, return_code = ctrl_base.post_model(DeviceMac, device_mac_id, data)
    if isinstance(response, Response):
        return response, return_code
    ret_data = response
    return jsonify(ret_data), return_code


# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/ctrl_models/ctrl_device_mac.py
