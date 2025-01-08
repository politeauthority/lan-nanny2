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
        self.api_client_id = "cnw5cas65q"
        self.api_key = "0f7h-5muw-orfn-8g6h"
        self.token = ""

    def run(self):
        """Primary entrypot for Scan"""
        print("Running Scanner")
        self.api_login()
        self.run_nmap()
        self.scan_submit()

    def run_nmap(self) -> bool:
        """Runs an Nmap Scan and saves the parsed data to self.scan_sdata"""
        logging.info("Starting NMap scan")
        nmap = NmapScan()
        if not nmap.run_scan():
            logging.error("Nmap Scan failed")
            logging.critical("Exiting")
            exit(1)
        self.scan_data = nmap.data
        return True

    def scan_submit(self) -> bool:
        """Submit a Scan to the Lan Nanny Api"""
        logging.info("Starting to submit the Scan")
        if not self.token:
            logging.error("No Lan Nanny Api token found, cant continue")
            logging.critical("Exiting")
            exit(1)
        if not self.scan_data:
            logging.error("No Scan data to submit")
            logging.critical("Exiting")
            exit(1)
        r_data = {
            "scan": self.scan_data,
        }
        url = self.api_url + "/scan-submit"
        headers = {
            "Token": self.token,
            "Content-Type": "application/json"
        }
        logging.info(f"Sending payload\n {r_data}")
        response = requests.post(url, headers=headers, json=r_data)
        if response.status_code != 201:
            msg = f"Failed to submit scan, got response code: {response.status_code}"
            msg += f"\n{response.text}"
            logging.error(msg)
            exit(1)
        import ipdb; ipdb.set_trace()
        return True

    def api_login(self) -> bool:
        """Logs into the Lan Nanny Api. Setting a self.token variable if successfull."""
        logging.info(f"Logging into to {self.api_url}")
        headers = {
            "X-Api-Key": self.api_key,
            "Client-Id": self.api_client_id,
            "Content-Type": "application/json"
        }
        url = self.api_url + "/auth"
        request = requests.post(url, headers=headers)
        if request.status_code != 200:
            logging.critical(
                f"Could not connect to api: {self.api_url} got code: {request.status_code}")
            logging.critical("Exiting")
            import ipdb; ipdb.set_trace()
            exit(1)
        response_json = request.json()
        self.token = response_json["token"]
        logging.info("Successfully got token from Lan Nanny Api")
        return True

if __name__ == "__main__":
    Scanner().run()

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/scan.py
