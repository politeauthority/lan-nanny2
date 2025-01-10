#!/usr/bin/env python
"""
    Lan Nanny - Scanner
    Modules - Glow
    Global variables for the Scanner

"""
import os

from lan_nanny.api.version import version


# Collect General Details
global general
general = {
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    "VERSION": version,
    "BUILD": os.environ.get("BUILD"),
    "BUILD_SHORT": "",
    "ENV": os.environ.get("BOOKMARKY_ENV"),
    "JWT_EXPIRE_MINUTES": os.environ.get("JWT_EXPIRE_MINUTES", 60),
    "SECRET_KEY": os.environ.get("SECRET_KEY", "hello-world123"),
    "TEST": os.environ.get("TEST", False),
    "LOG_HEALTH_CHECKS": os.environ.get("LOG_HEALTH_CHECKS", True),
    "DEPLOYED_AT": os.environ.get("DEPLOYED_AT", None),
    "IMAGE_DIR": os.environ.get("PUBLIC_IMAGES", "/images"),
    # "IMAGE_DIR": "/work/src/bookmarky/public/images",
}
if general["BUILD"]:
    general["BUILD_SHORT"] = general["BUILD"][:12]
if general["TEST"] == "true":
    general["TEST"] = True
else:
    general["TEST"] = False
if general["LOG_HEALTH_CHECKS"] == "true":
    general["LOG_HEALTH_CHECKS"] = True
else:
    general["LOG_HEALTH_CHECKS"] = False

global api
api = {
    "API_URL": os.environ.get("LAN_NANNY_API_URL"),
    "API_CLIENT_ID": os.environ.get("LAN_NANNY_CLIENT_ID"),
    "API_KEY": os.environ.get("LAN_NANNY_API_KEY"),
}


# End File: politeauthority/lan-nanny/src/scanner/lan-nanny/api/utils/glow.py
