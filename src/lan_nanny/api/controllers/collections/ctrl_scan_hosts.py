"""
    Lan Nanny - Api
    Controller Collection
    Scan Hosts

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.scan_hosts import ScanHosts
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth


ctrl_scan_hosts = Blueprint("scan_hosts", __name__, url_prefix="/scan-hosts")


@ctrl_scan_hosts.route("")
@ctrl_scan_hosts.route("/")
@auth.auth_request
def index():
    """Get Device Scan Hosts"""
    data = ctrl_collection_base.get(ScanHosts)
    return jsonify(data)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/collections/ctrl_scan_hosts.py
