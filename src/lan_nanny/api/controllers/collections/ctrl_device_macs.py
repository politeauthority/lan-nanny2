"""
    Lan Nanny - Api
    Controller Collection
    Device Macs

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth


ctrl_device_macs = Blueprint("device_macs", __name__, url_prefix="/device-macs")


@ctrl_device_macs.route("")
@ctrl_device_macs.route("/")
@auth.auth_request
def index():
    """Get Device Macs"""
    data = ctrl_collection_base.get(Devices)
    return jsonify(data)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/collections/ctrl_device_macs.py
