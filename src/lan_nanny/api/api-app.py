#!/usr/bin/env python
"""
    Lan Nanny - Api
    Web App
    Primary web app entrpoint

"""
import logging
import os
import traceback
import sys

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from lan_nanny.shared.utils import log_configs
from lan_nanny.api.utils import db
from lan_nanny.api.utils import glow
# from cver.api.utils import glow
# from cver.api.utils import misc
from lan_nanny.api.controllers.models.ctrl_api_key import ctrl_api_key
from lan_nanny.api.controllers.collections.ctrl_api_keys import ctrl_api_keys
from lan_nanny.api.controllers.ctrl_index import ctrl_index
# from lan_nanny.api.controllers.ctrl_inter_ops import ctrl_interops
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

from lan_nanny.api.controllers.models.ctrl_device import ctrl_device
from lan_nanny.api.controllers.collections.ctrl_devices import ctrl_devices
from lan_nanny.api.controllers.models.ctrl_device_mac import ctrl_device_mac
from lan_nanny.api.controllers.collections.ctrl_device_macs import ctrl_device_macs
from lan_nanny.api.controllers.models.ctrl_device_port import ctrl_device_port
from lan_nanny.api.controllers.collections.ctrl_device_ports import ctrl_device_ports
from lan_nanny.api.controllers.collections.ctrl_scan_hosts import ctrl_scan_hosts
from lan_nanny.api.controllers.collections.ctrl_scan_ports import ctrl_scan_ports
from lan_nanny.api.controllers.models.ctrl_vendor import ctrl_vendor
from lan_nanny.api.controllers.collections.ctrl_vendors import ctrl_vendors
from lan_nanny.api.controllers.ctrl_scan import ctrl_scan
from lan_nanny.api.controllers.ctrl_stats import ctrl_stats

if glow.general["ENV"].lower() == "dev":
    logging.config.dictConfig(log_configs.config_dev)
else:
    logging.config.dictConfig(log_configs.configs_prod)
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

    app.register_blueprint(ctrl_device)
    app.register_blueprint(ctrl_devices)
    app.register_blueprint(ctrl_device_mac)
    app.register_blueprint(ctrl_device_macs)
    app.register_blueprint(ctrl_device_port)
    app.register_blueprint(ctrl_device_ports)
    app.register_blueprint(ctrl_scan_hosts)
    app.register_blueprint(ctrl_scan_ports)
    app.register_blueprint(ctrl_vendor)
    app.register_blueprint(ctrl_vendors)

    app.register_blueprint(ctrl_scan)
    app.register_blueprint(ctrl_stats)

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
    if db:
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
