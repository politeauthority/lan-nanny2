"""
    Lan Nanny - Shared
    Logging Configs
    Hopefully a unified place to manage logging across all Lan Nanny Apps.. we'll see.

"""
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")


config_dev = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(module)s #%(lineno)d - %(message)s",
            "datefmt": "%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default"
        },
        'requests': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            "level": "ERROR"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["wsgi"]
    },
    "requests": {
        "level": "warning"
    }
}

configs_prod = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(module)s: %(message)s",
            "datefmt": "%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["wsgi"]
    },
    "requests": {
        "level": "warning"
    }
}

# End File: bookmarky/src/bookmarky/shared/utils/log_config_configs.py
