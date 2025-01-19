"""
    Lan Nanny - Api
    Controller
    /scan

"""
import logging
import json

from flask import Blueprint, jsonify, Response, request

# from lan_nanny.api.utils import api_util
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.utils.handle_host_scan import HandleHostScan
from lan_nanny.api.utils.handle_port_scan import HandlePortScan

from lan_nanny.api.utils import auth

ctrl_scan = Blueprint("scan", __name__, url_prefix="/scan")


@auth.auth_request
@ctrl_scan.route("/submit-host", methods=["POST"])
@ctrl_scan.route("/submit-host/", methods=["POST"])
def scan_submit_host() -> Response:
    """Scan Submit Host"""
    data = {
        "info": "Lan Nanny",
    }
    data["scan"] = {}
    request_data = json.loads(request.get_data().decode('utf-8'))
    logging.info("Recieved Host Scan from: %s" "User-Agent")
    # logging.info("Got Scan Data:\n%s" % request_data)
    if "scan" not in request_data:
        data["status"] = "Error"
        return jsonify(data, 400)
    if "scan" not in request_data:
        logging.error("Scan request missing data")
        return jsonify(data), 400
    if "meta" not in request_data:
        logging.error("Scan request missing data")
        return jsonify(data), 400
    scan_meta = request_data["meta"]
    scan_data = request_data["scan"]
    scan_handled = HandleHostScan().run(scan_data, scan_meta)
    logging.info(f"Scan Handled: {scan_handled}")
    return jsonify(data), 201


@auth.auth_request
@ctrl_scan.route("/port-scan-order", methods=["GET"])
@ctrl_scan.route("/port-scan-order/", methods=["GET"])
def take_port_scan() -> Response:
    """Route for a Scanner Agent to recieve a prescription for a port scanning operation on a single
    host.
    """
    data = {
        "info": "Lan Nanny",
        "scan_targets": [],
        "command": "nmap {host}"
    }
    logging.info("Looking for Port Scan targets for Scan Agent")
    device_to_scan = DeviceMacs().ready_for_port_scan()
    for device_mac in device_to_scan:
        data["scan_targets"].append(device_mac.json())
    # logging.info("Got Scan Data:\n%s" % request_data)
    return jsonify(data), 201


@auth.auth_request
@ctrl_scan.route("/submit-port/<mac_address>", methods=["POST"])
def submit_port_scan(mac_address: int) -> Response:
    """Port Scan Submit.
    """
    data = {
        "info": "Lan Nanny",
    }
    data["scan"] = {}
    request_data = json.loads(request.get_data().decode('utf-8'))
    handle_scan = HandlePortScan().run(mac_address, request_data["meta"], request_data["scan"])
    print(handle_scan)
    return jsonify(data), 201


@auth.auth_request
@ctrl_scan.route("/submit-port-error/<mac_address>", methods=["POST"])
def submit_port_scan_error(mac_address: int) -> Response:
    """Port Scan Submit error."""
    data = {
        "info": "Lan Nanny",
    }
    data["scan"] = {}
    request_data = json.loads(request.get_data().decode('utf-8'))
    handle_scan = HandlePortScan().run_error(mac_address, request_data["meta"])
    print(handle_scan)
    data["scan"] = {}
    return jsonify(data), 201


# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
