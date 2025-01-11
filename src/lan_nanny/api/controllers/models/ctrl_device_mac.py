"""
    Bookmarky Api
    Controller Model
    Device Mac

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.device import Device
from lan_nanny.api.utils import auth


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
    data = ctrl_base.get_model(Device, device_mac_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/ctrl_models/ctrl_device_mac.py
