"""
    Lan Nanny - Api
    Controller
    Scan Submit
    /scan-submit

"""
import logging
import json

from flask import Blueprint, jsonify, Response, request
# from lan_nanny.api.utils import api_util
from lan_nanny.api.utils.handle_scan import HandleScan

from lan_nanny.api.utils import auth

ctrl_scan_submit = Blueprint("scan-submit", __name__, url_prefix="/scan-submit")


@auth.auth_request
@ctrl_scan_submit.route("", methods=["POST"])
@ctrl_scan_submit.route("/", methods=["POST"])
def scan_submit() -> Response:
    """Scan Submit"""
    data = {
        "info": "Lan Nanny",
    }
    data["scan"] = {}
    request_data = json.loads(request.get_data().decode('utf-8'))
    logging.info("Recieved Scan from: %s" "User-Agent")
    # logging.info("Got Scan Data:\n%s" % request_data)
    if "scan" not in request_data:
        data["status"] = "Error"
        return jsonify(data, 400)
    scan_data = request_data["scan"]
    scan_handled = HandleScan().run(scan_data)
    logging.info(f"Scan Handled: {scan_handled}")
    return jsonify(data), 201


# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
