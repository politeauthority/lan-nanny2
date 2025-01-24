"""
    Lan Nanny - Api
    Controller Collection
    Device Ports

"""

from flask import Blueprint, jsonify

from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.collects.device_ports import DevicePorts
from lan_nanny.api.utils import auth


ctrl_device_ports = Blueprint("device_ports", __name__, url_prefix="/device-ports")


@ctrl_device_ports.route("")
@ctrl_device_ports.route("/")
@auth.auth_request
def index():
    """Get Device Macs"""
    data = ctrl_collection_base.get(DevicePorts)
    return jsonify(data)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/collections/ctrl_device_ports.py
