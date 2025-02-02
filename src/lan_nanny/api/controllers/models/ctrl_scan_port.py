"""
    Bookmarky Api
    Controller Model
    Scan Port

"""
import logging

from flask import Blueprint, jsonify, Response

from lan_nanny.api.controllers.models import ctrl_base
from lan_nanny.api.models.scan_port import ScanPort
from lan_nanny.api.utils import auth


ctrl_scan_port = Blueprint("scan-port", __name__, url_prefix="/scan-port")


@ctrl_scan_port.route("")
@ctrl_scan_port.route("/")
@ctrl_scan_port.route("/<scan_port_id>", methods=["GET"])
@auth.auth_request
def get_model(scan_port_id: int = None) -> Response:
    """GET operation for a Scan Port ID.
    GET /scan-port
    """
    logging.info("GET - /scan-port")
    data = ctrl_base.get_model(ScanPort, scan_port_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/ctrl_models/ctrl_scan_port.py
