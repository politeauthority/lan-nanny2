"""
    Lan Nanny - Api
    Controller
    Scan Submit
    /scan-submit

"""
from flask import Blueprint, jsonify, Response, request
from lan_nanny.api.utils import api_util

from lan_nanny.api.utils import auth

ctrl_scan_submit = Blueprint("scan-submit", __name__, url_prefix="/scan-submit")


@auth.auth_request
@ctrl_scan_submit.route("", methods=["POST"])
@ctrl_scan_submit.route("/", methods=["POST"])
def scan_submit() -> Response:
    """Scan Submit
    """
    data = {
        "info": "Lan Nanny",
    }
    data["scan"] = {}
    print(request.form)
    import ipdb; ipdb.set_trace()
    return jsonify(data)


def _get_ids(rows) -> list:
    """Generate a list of Tag IDs from a result set."""
    ret_ids = []
    for row in rows:
        ret_ids.append(row[0])
    return ret_ids

# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
