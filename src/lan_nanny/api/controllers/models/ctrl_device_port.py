"""
    Lan Nanny
    Controller Model
    Device Port

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.device_port import DevicePort
from lan_nanny.api.utils import auth


ctrl_device_port = Blueprint("device-port", __name__, url_prefix="/device-port")


@ctrl_device_port.route("")
@ctrl_device_port.route("/")
@ctrl_device_port.route("/<device_port_id>", methods=["GET"])
@auth.auth_request
def get_model(device_port_id: int = None) -> Response:
    """GET operation for a Device.
    GET /device-port
    """
    logging.info("GET - /device-mac")
    data = ctrl_base.get_model(DevicePort, device_port_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/ctrl_models/ctrl_device_port.py
