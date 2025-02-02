"""
    Lan Nanny - Api
    Controller
    /search

"""
# import logging
# import json

from flask import Blueprint, jsonify, Response, request

# from lan_nanny.api.utils import api_util
# from lan_nanny.api.collects.device_macs import DeviceMacs
# from lan_nanny.api.utils.handle_host_scan import HandleHostScan
# from lan_nanny.api.utils.handle_port_scan import HandlePortScan
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.utils import auth

ctrl_search = Blueprint("search", __name__, url_prefix="/search")


@auth.auth_request
@ctrl_search.route("")
@ctrl_search.route("/")
def search() -> Response:
    """General search"""
    if "query" not in request.args:
        return jsonify({"error": "Error"}), 400
    query = request.args["query"]
    dm_col = DeviceMacs()
    device_macs = dm_col.search(query)
    device_macs = dm_col.make_json(device_macs)
    data = {
        "info": {
            "device_macs": len(device_macs),
        },
        "results": {
            "device_macs": device_macs
        }
    }
    return jsonify(data), 201


# End File: politeauthroity/lan-nanny/src/lan-nanny/api/controllers/ctrl_search.py
