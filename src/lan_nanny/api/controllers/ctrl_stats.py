"""
    Lan Nanny - Api
    Controller
    /stats

"""
# import logging
# import json

from flask import Blueprint, jsonify, Response

# from lan_nanny.api.utils import api_util
# from lan_nanny.api.collects.device_macs import DeviceMacs
# from lan_nanny.api.utils.handle_host_scan import HandleHostScan
# from lan_nanny.api.utils.handle_port_scan import HandlePortScan
from lan_nanny.api.stats import entity_stats

from lan_nanny.api.utils import auth

ctrl_stats = Blueprint("stats", __name__, url_prefix="/stats")


@auth.auth_request
@ctrl_stats.route("/dashboard")
def dashboard() -> Response:
    """Stats Dashboard"""
    data = {
        "info": "Lan Nanny",
        "stats": {
            "online": entity_stats.get_online_now()
        }
    }
    return jsonify(data), 201


# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
