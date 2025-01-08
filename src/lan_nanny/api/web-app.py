#!/usr/bin/env python
"""
    Bookmarky Api
    Web App
    Primary web app entrpoint

"""
import logging
import os
import traceback
import sys

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from lan_nanny.shared.utils.log_config import log_config
from lan_nanny.api.utils import db
from lan_nanny.api.utils import glow
# from cver.api.utils import glow
# from cver.api.utils import misc
from lan_nanny.api.controllers.models.ctrl_api_key import ctrl_api_key
from lan_nanny.api.controllers.collections.ctrl_api_keys import ctrl_api_keys
from lan_nanny.api.controllers.ctrl_index import ctrl_index
from lan_nanny.api.controllers.ctrl_inter_ops import ctrl_interops
# from cver.api.controllers.ctrl_collections.ctrl_migrations import ctrl_migrations
# from cver.api.controllers.ctrl_models.ctrl_role import ctrl_role
# from cver.api.controllers.ctrl_collections.ctrl_roles import ctrl_roles
# from cver.api.controllers.ctrl_models.ctrl_role_perm import ctrl_role_perm
# from cver.api.controllers.ctrl_collections.ctrl_role_perms import ctrl_role_perms
# from cver.api.controllers.ctrl_models.ctrl_perm import ctrl_perm
# from cver.api.controllers.ctrl_collections.ctrl_perms import ctrl_perms
from lan_nanny.api.controllers.models.ctrl_user import ctrl_user
from lan_nanny.api.controllers.collections.ctrl_users import ctrl_users
from lan_nanny.api.controllers.models.ctrl_option import ctrl_option
from lan_nanny.api.controllers.collections.ctrl_options import ctrl_options

from lan_nanny.api.controllers.models.ctrl_bookmark import ctrl_bookmark
from lan_nanny.api.controllers.collections.ctrl_bookmarks import ctrl_bookmarks

from lan_nanny.api.controllers.models.ctrl_bookmark_tag import ctrl_bookmark_tag
from lan_nanny.api.controllers.models.ctrl_auto_feature import ctrl_auto_feature
from lan_nanny.api.controllers.collections.ctrl_auto_features import ctrl_auto_features

from lan_nanny.api.controllers.models.ctrl_directory import ctrl_directory
from lan_nanny.api.controllers.collections.ctrl_directories import ctrl_directories
from lan_nanny.api.controllers.models.ctrl_tag import ctrl_tag
from lan_nanny.api.controllers.collections.ctrl_tags import ctrl_tags

from lan_nanny.api.controllers.ctrl_stats import ctrl_stats
from lan_nanny.api.controllers.ctrl_image import ctrl_image


logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True

app = Flask(__name__)
app.config.update(DEBUG=True)
app.debugger = False


def register_blueprints(app: Flask) -> bool:
    """Register controller blueprints to flask."""
    app.register_blueprint(ctrl_index)
    app.register_blueprint(ctrl_api_key)
    app.register_blueprint(ctrl_api_keys)
    app.register_blueprint(ctrl_user)
    app.register_blueprint(ctrl_users)
    app.register_blueprint(ctrl_option)
    app.register_blueprint(ctrl_options)

    app.register_blueprint(ctrl_bookmark)
    app.register_blueprint(ctrl_bookmarks)
    app.register_blueprint(ctrl_bookmark_tag)
    app.register_blueprint(ctrl_directory)
    app.register_blueprint(ctrl_directories)
    app.register_blueprint(ctrl_tag)
    app.register_blueprint(ctrl_tags)
    app.register_blueprint(ctrl_auto_feature)
    app.register_blueprint(ctrl_auto_features)

    app.register_blueprint(ctrl_interops)
    app.register_blueprint(ctrl_stats)
    app.register_blueprint(ctrl_image)

    return True


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch 500 errors, and pass through the exception
    @todo: Remove the exception for non prod environments.
    """
    data = {
        "message": "Server error",
        "request-id": glow.session["short_id"],
        "status": "error"
    }
    RESPONSE_CODE = 500
    # pass through HTTP errors
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    if isinstance(e, HTTPException):
        data["message"] = e.description
        return jsonify(data), RESPONSE_CODE

    traceback.print_exc(file=sys.stdout)
    logging.error(traceback)
    if glow.general["TEST"]:
        data["message"] = traceback
        return jsonify(data), 500
    else:
        return jsonify(data), RESPONSE_CODE


@app.before_request
def before_request():
    """Before we route the request log some info about the request."""
    url_requested = request.base_url[request.base_url.rfind("/"):]
    if url_requested == "/healthz":
        return
    glow.start_session()
    logging.info(
        "[Start Request] %s\tpath: %s | method: %s" % (
            glow.session["short_id"][:8],
            request.path,
            request.method))
    db.connect()
    return


@app.after_request
def after_request(response):
    url_requested = request.base_url[request.base_url.rfind("/"):]
    if url_requested == "/healthz":
        return response
    logging.info(
        "[End Request] %s\tpath: %s | method: %s | status: %s | size: %s",
        glow.session["short_id"],
        request.path,
        request.method,
        response.status,
        response.content_length
    )
    db.close()
    return response


register_blueprints(app)

# Development Runner
if __name__ == "__main__":
    logging.info("Starting develop webserver")
    app.run(host='0.0.0.0', port=80)


# Production Runner
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.debug")
    logging.info("Starting production webserver")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.config['DEBUG'] = False


# End File: politeauthority/bookmarky-api/src/bookmarky/api/app.py
