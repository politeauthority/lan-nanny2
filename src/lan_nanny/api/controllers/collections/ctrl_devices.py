"""
    Lan Nanny - Api
    Controller Collection
    Devices

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth


ctrl_devices = Blueprint("devices", __name__, url_prefix="/devices")


@ctrl_devices.route("")
@ctrl_devices.route("/")
@auth.auth_request
def index():
    """Get Devices"""
    data = ctrl_collection_base.get(Devices)
    return jsonify(data)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/collections/ctrl_devices.py
