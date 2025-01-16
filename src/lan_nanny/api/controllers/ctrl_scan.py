"""
    Lan Nanny - Api
    Controller
    /scan

"""
import logging
import json

import arrow
from flask import Blueprint, jsonify, Response, request

# from lan_nanny.api.utils import api_util
from lan_nanny.api.models.device import Device
from lan_nanny.api.models.device_mac import DeviceMac
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.models.device_port import DevicePort
from lan_nanny.api.utils.handle_host_scan import HandleHostScan

from lan_nanny.api.utils import auth

ctrl_scan = Blueprint("scan", __name__, url_prefix="/scan")


@auth.auth_request
@ctrl_scan.route("/submit-host", methods=["POST"])
@ctrl_scan.route("/submit-host/", methods=["POST"])
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
@ctrl_scan.route("/submit-port/<device_mac_id>", methods=["POST"])
def submit_port_scan(device_mac_id: int) -> Response:
    """Scan Submit"""
    data = {
        "info": "Lan Nanny",
    }
    data["scan"] = {}
    request_data = json.loads(request.get_data().decode('utf-8'))
    device_mac = DeviceMac()
    device_mac.get_by_id(device_mac_id)
    logging.info("Handling port scan for %s" % device_mac)
    now = arrow.utcnow()
    logging.debug("Recieved data on %s ports for device" % len(request_data["ports"]))
    for port in request_data["ports"]:
        dp = DevicePort()
        if dp.get_by_scan_details(device_mac.id, port["port_id"], port["protocol"]):
            logging.info("Found Device Port existings already")
        else:
            logging.info("Did not find Device Port already")
            dp.port_id = port["port_id"]
            dp.device_mac_id = device_mac.id
            dp.first_seen = now
            dp.protocol = port["protocol"]

        dp.last_seen = now
        dp.current_state = "open"
        if device_mac.device_id:
            dp.device_id = device_mac.device_id
        if not dp.save():
            logging.error("Failed to save: %s" % dp)
        else:
            logging.info("Saved %s" % dp)
    device_mac.last_port_scan = now
    device_mac.save()
    if device_mac.device_id:
        device = Device()
        device.last_port_scan = now
        device.save()

    return jsonify(data), 201

# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
