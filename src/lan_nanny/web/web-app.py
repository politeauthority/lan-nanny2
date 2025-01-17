"""
    Lan Nanny Web
    Web App

"""

import logging

from flask import Flask
from modules.ctrl_index import ctrl_index

app = Flask(__name__, static_url_path='/static')
app.config.update(DEBUG=True)
app.debugger = False


def register_blueprints(app: Flask) -> bool:
    """Register controller blueprints to flask."""
    app.register_blueprint(ctrl_index)
    return True


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


# End File: politeauthority/lan-nanny/src/lan_nanny/web/web-app.py
