#!/usr/bin/env python
"""
    Lan Nanny - Scanner
    Utils
    Glow
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
    "ENV": os.environ.get("LAN_NANNY_ENV"),
    "TEST": os.environ.get("TEST", False),
    "DEPLOYED_AT": os.environ.get("DEPLOYED_AT", None),
}
if general["BUILD"]:
    general["BUILD_SHORT"] = general["BUILD"][:12]
if general["TEST"] == "true":
    general["TEST"] = True
else:
    general["TEST"] = False

global api
api = {
    "API_URL": os.environ.get("LAN_NANNY_API_URL"),
    "API_CLIENT_ID": os.environ.get("LAN_NANNY_API_CLIENT_ID"),
    "API_KEY": os.environ.get("LAN_NANNY_API_KEY"),
}

# End File: politeauthority/lan-nanny/src/scanner/lan_nanny/scanner/utils/glow.py
