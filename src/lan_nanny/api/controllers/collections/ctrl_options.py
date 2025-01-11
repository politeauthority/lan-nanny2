"""
    Cver Api - Controller Collection
    Options

"""

from flask import Blueprint, jsonify

from lan_nanny.api.collects.options import Options
from lan_nanny.api.controllers.collections import ctrl_collection_base
from lan_nanny.api.utils import auth

ctrl_options = Blueprint('options', __name__, url_prefix='/options')


@ctrl_options.route('')
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Options)
    return jsonify(data)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_collections/ctrl_options.py
