#!/usr/bin/env python
"""
    Lanny Nanny Web
    Modules - Glow
    Global variables for Lan Nanny Web.

"""
import os

from lan_nanny.api.version import version

# Collect General Details
global general
general = {
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    "ENV": os.environ.get("LAN_NANNY_ENV", "PROD"),
    "API_URL": "https://api.lan-nanny-%s.alix.lol" % (
        os.environ.get("LAN_NANNY_ENV", "PROD").lower()),
    "VERSION": version,
    # "VERSION_WEB": version.version
}
general["API_URL"] = "https://api.lan-nanny-dev.alix.lol"
if general["ENV"] == "prod":
    general["API_URL"] = "https://api.lan-nanny.alix.lol"


# End File: politeauthority/lan_nanny/src/lan_nanny/web/modules/glow.py
