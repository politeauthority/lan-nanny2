"""
    Lan Nanny - Scanner

"""
import logging
from logging.config import dictConfig
import requests

from lan_nanny.scanner.modules.nmap_scan import NmapScan

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})


class Scanner:

    def __init__(self):
        self.scan_data = {}
        self.api_url = "https://api.lan-nanny-dev.alix.lol"
        self.api_client_id = ""
        self.api_key = ""

    def run(self):
        """Primary entrypot for Scan"""
        print("Running Scanner")
        self.api_login()
        self.run_nmap()
        self.scan_submit()

    def run_nmap(self):
        logging.info("Starting NMap scan")
        nmap = NmapScan()
        self.scan_data = nmap.run_scan()

    def scan_submit(self):
        """Submit a Scan to the 
        """
        self.api_login()
    
    def api_login(self) -> bool:
        headers = {
            "X-Api-Key": self.api_key,
            "Client-Id": self.api_client_id,
            "Content-Type": "application/json"
        }
        requests = requests.get(self.api_login, headers)
        import ipdb; ipdb.set_trace()

if __name__ == "__main__":
    Scanner().run()

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/scan.py
