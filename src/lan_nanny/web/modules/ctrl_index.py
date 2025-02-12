"""
    Lan Nanny Web
    Controller - Index
    /

"""
import logging

from flask import Blueprint, jsonify, Response, render_template, request

from . import glow

ctrl_index = Blueprint("index", __name__, url_prefix="/")


@ctrl_index.route("")
@ctrl_index.route("/")
def index() -> Response:
    """Login page for unauthenticated users."""
    logging.info("Serving /")
    return render_template("page/login.jinja")


@ctrl_index.route("/info")
def info() -> Response:
    """Get information on Lan Nanny"""
    data = {
        "info": "Lan Nanny Web",
    }
    return jsonify(data)


@ctrl_index.route("/dashboard")
def dashboard() -> Response:
    """Lan Nanny Dashboard"""
    return render_template("page/dashboard.jinja")


@ctrl_index.route("/devices")
def devices() -> Response:
    """Lan Nanny Devices"""
    return render_template("page/devices.jinja")


@ctrl_index.route("/device/<device_id>")
def device(device_id) -> Response:
    """Device Mac"""
    return render_template("page/device.jinja")


@ctrl_index.route("/device-mac/<device_mac_id>")
def device_mac(device_mac_id) -> Response:
    """Device Mac"""
    return render_template("page/device_mac.jinja")


@ctrl_index.route("/scans")
def scans() -> Response:
    """Scans page"""
    return render_template("page/scans.jinja")


@ctrl_index.route("/scan-port/<scan_port_id>")
def scan_port(scan_port_id: int) -> Response:
    """Scan Port"""
    data = {
        "scan_id": scan_port_id
    }
    return render_template("page/scan-port.jinja", **data)


@ctrl_index.route("/search")
def search() -> Response:
    """Search results page"""
    data = {}
    if "query" in request.args:
        data["query"] = request.args
    return render_template("page/search-results.jinja", **data)


@ctrl_index.route("/settings")
def settings() -> Response:
    """Provide the User settings page."""
    logging.info("Serving /settings")
    return render_template("page/settings.jinja")


@ctrl_index.route("/debug")
def debug() -> Response:
    """A place to dump things"""
    logging.info("Serving /debug")
    data = {
        "ENV": glow.general["ENV"],
        "API_URL": glow.general["API_URL"],
        "VERSION": glow.general["VERSION"]
    }
    return render_template("page/debug.jinja", **data)


@ctrl_index.route("/config.js")
def config_js() -> Response:
    data = {
        "API_URL": glow.general["API_URL"],
        "VERSION": glow.general["VERSION"]
    }
    config_js = render_template("js_config.jinja", **data)
    return Response(config_js, mimetype="text/javascript")


@ctrl_index.route("/healthz")
def healthz() -> Response:
    data = {
        "status": "Success",
        "message": "Healthy"
    }
    # if glow.general["LOG_HEALTH_CHECKS"]:
    #     logging.info("Helath check, reporting healthy")
    return jsonify(data)


# End File: politeauthroity/lan_nanny/src/lan-nanny/web/modules/ctrl_index.py
