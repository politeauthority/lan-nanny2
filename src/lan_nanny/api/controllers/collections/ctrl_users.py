"""
    Bookmarky Api
    Controller Collection - Users

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.users import Users
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth

ctrl_users = Blueprint("users", __name__, url_prefix="/users")


@ctrl_users.route("")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Users)
    return jsonify(data)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_collections/ctrl_users.py
