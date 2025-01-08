"""
    Bookmark Api
    Controller Collection
    Directories

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.directories import Directories
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth


ctrl_directories = Blueprint("directories", __name__, url_prefix="/directories")


@ctrl_directories.route("")
@auth.auth_request
def index():
    """Get Directories"""
    data = ctrl_collection_base.get(Directories)
    return jsonify(data)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/collections/
#           ctrl_bookmarks.py
