"""
    Lan Nanny Web
    Controller - Index
    /

"""
import logging

from flask import Blueprint, jsonify, Response, render_template

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
    """Get information on Bookmark Web"""
    return render_template("page/dashboard.jinja")


@ctrl_index.route("/settings")
def settings() -> Response:
    """Provide the User settings page."""
    logging.info("Serving /settings")
    data = {
        "ENV": glow.general["ENV"]
    }
    return render_template("page/settings.jinja", **data)


@ctrl_index.route("/config.js")
def config_js() -> Response:
    data = {
        "API_URL": glow.general["API_URL"],
        "VERSION_WEB": glow.general["VERSION_WEB"]
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
