"""
    Bookmark Api
    Controller Collection
    Auto Features

"""
from flask import Blueprint, jsonify, Response

from lan_nanny.api.collects.auto_features import AutoFeatures
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import glow

ctrl_auto_features = Blueprint("auto-features", __name__, url_prefix="/auto-features")

PER_PAGE = 50


@ctrl_auto_features.route("")
@auth.auth_request
def index() -> Response:
    """Get Auto Features."""
    extra_args = {
        "fields": {
            "user_id": {
                "value": glow.user["user_id"],
                "op": "=",
                "overrideable": False
            }
        },
        "order_by": {},
        "limit": None
    }
    data = ctrl_collection_base.get(AutoFeatures, extra_args)
    return jsonify(data)


# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_collections/
#           ctrl_auto_features.py
