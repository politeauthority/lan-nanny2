"""
    Lan Nanny - Api
    Controller Collection
    Vendors

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.vendors import Vendors
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth


ctrl_vendors = Blueprint("vendors", __name__, url_prefix="/vendors")


@ctrl_vendors.route("")
@ctrl_vendors.route("/")
@auth.auth_request
def index():
    """Get Vendors"""
    data = ctrl_collection_base.get(Vendors)
    return jsonify(data)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/controllers/collections/ctrl_vendors.py
