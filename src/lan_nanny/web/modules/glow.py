#!/usr/bin/env python
"""
    Lanny Nanny Web
    Modules - Glow
    Global variables for Lan Nanny Web.

"""
import os
# from . import version

# Collect General Details
global general
general = {
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    "ENV": os.environ.get("LAN_NANNY_ENV", "PROD"),
    "API_URL": "https://api.lan_nanny-%s.alix.lol" % (
        os.environ.get("BOOKMARKY_ENV", "PROD").lower()),
    "VERSION_WEB": "",
    # "VERSION_WEB": version.version
}
if general["ENV"] == "PROD":
    general["API_URL"] = "https://api.lan_nanny.alix.lol"


# End File: politeauthority/lan_nanny/src/lan_nanny/web/modules/glow.py
