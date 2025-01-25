"""
    Lan Nanny - Api
    Controller Collection
    Scan Ports

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.scan_ports import ScanPorts
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth


ctrl_scan_ports = Blueprint("scan_ports", __name__, url_prefix="/scan-ports")


@ctrl_scan_ports.route("")
@ctrl_scan_ports.route("/")
@auth.auth_request
def index():
    """Get Device Scan Ports"""
    data = ctrl_collection_base.get(ScanPorts)
    return jsonify(data)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/collections/ctrl_scan_ports.py
