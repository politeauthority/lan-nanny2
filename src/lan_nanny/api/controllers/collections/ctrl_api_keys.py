"""
    Bookmark Api
    Controller Collection
    Api Keys

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.api_keys import ApiKeys
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth

ctrl_api_keys = Blueprint("api_keys", __name__, url_prefix="/api-keys")


@ctrl_api_keys.route("")
@auth.auth_request
def index():
    """Get ApiKeys."""
    data = ctrl_collection_base.get(ApiKeys)
    return jsonify(data)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_collections/ctrl_api_keys.py
