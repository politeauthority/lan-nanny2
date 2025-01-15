"""
    Lan Nanny - Scanner
    Scan
    Main entrypoint to the Scan portion of Lan Nanny
"""
import logging
from logging.config import dictConfig

import arrow
import requests

from lan_nanny.scanner.modules.nmap_scan import NmapScan
from lan_nanny.scanner.utils import glow

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
        self.process_start = None
        self.process_end = None
        self.options = []
        self.scan_data = {}
        self.api_url = glow.api["API_URL"]
        self.api_client_id = glow.api["API_CLIENT_ID"]
        self.api_key = glow.api["API_KEY"]
        self.token = ""

    def run(self) -> bool:
        """Primary entrypot for Scan"""
        if glow.general["ENV"] == "DEV":
            logging.info("\n\n  -- Development Environment -- ")
        logging.info("Running Scanner")
        self.api_login()
        self.hydrate()
        if not self.options["scan-enabled"]["value"]:
            logging.warning("Scanning is not enabled by Lan Nanny Options, exiting")
            exit(0)
        self.run_host_scan()
        self.run_extra_scans()

    def hydrate(self):
        """Logs into the Lan Nanny Api. Setting a self.token variable if successfull."""
        logging.info(f"Getting options from {self.api_url}")
        headers = {
            "Token": self.token,
            "Content-Type": "application/json",
            "User-Agent": "LanNanny/Scanner v%s" % glow.general["VERSION"]
        }
        url = self.api_url + "/options"
        request = requests.get(url, headers=headers)
        if request.status_code != 200:
            logging.critical(
                f"Could not fetch options from api: {self.api_url} got code: {request.status_code}")
            logging.critical("Exiting")
            exit(1)
        response_json = request.json()
        options = {}
        for opt in response_json["objects"]:
            options[opt["name"]] = opt
        self.options = options
        # logging.debug(self.options)
        logging.info("Successfully got Options from Lan Nanny Api")
        return True

    def run_host_scan(self) -> bool:
        """Run and manage the host scan of the given network."""
        if not self.options["scan-hosts-enabled"]["value"]:
            logging.info("Host scanning is not enabled by Lan Nanny Options, exiting")
            return True
        self.process_start = arrow.utcnow()
        self.run_nmap()
        self.scan_submit()
        self.process_end = arrow.utcnow()
        elapsed = (self.process_end - self.process_start)
        logging.info("Finished entire process in %s.%s seconds" % (
            (elapsed.seconds, elapsed.microseconds)))
        return True

    def run_nmap(self) -> bool:
        """Runs an Nmap Scan and saves the parsed data to self.scan_sdata"""
        logging.info("Starting NMap scan")
        nmap = NmapScan()
        if not nmap.run_scan():
            logging.error("Nmap Scan failed")
            logging.critical("Exiting")
            exit(1)
        self.scan_data = nmap.data
        self.scan_meta = nmap.scan_meta
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
            "meta": self.scan_meta,
            "scan": self.scan_data,
        }
        url = self.api_url + "/scan/submit-host"
        logging.info("\n\nSubmmitting scan data to %s\n\n" % url)
        headers = {
            "Token": self.token,
            "Content-Type": "application/json"
        }
        # logging.info(f"Sending payload\n {r_data}")
        logging.info("Sending host scan payload")
        response = requests.post(url, headers=headers, json=r_data)
        if response.status_code != 201:
            msg = f"Failed to submit scan, got response code: {response.status_code}"
            msg += f"\n{response.text}"
            logging.error(msg)
            exit(1)
        logging.info("Scan submitted successfully!")
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
            exit(1)
        response_json = request.json()
        self.token = response_json["token"]
        logging.info("Successfully got token from Lan Nanny Api")
        return True

    def run_extra_scans(self) -> bool:
        """Ask the api for other scan operations for the Agent to run.
        """
        if not self.options["scan-ports-enabled"]["value"]:
            logging.info("Port scanning is not enabled by Lan Nanny Options, exiting")
            return True
        attempt_threshold = 1
        port_scan_order = self.get_port_scan_order()
        if len(port_scan_order["scan_targets"]) == 0:
            logging.info("Got no hosts ready for port scanning from api.")
            return True
        else:
            logging.info("Got %s hosts ready for port scanning, only attempting %s on this run." % (
                len(port_scan_order["scan_targets"]),
                attempt_threshold
            ))
        device_mac = port_scan_order["scan_targets"][0]
        data = NmapScan().run_port_scan(device_mac["last_ip"])
        self.scan_port_submit(device_mac["id"], data)
        return True

    def get_port_scan_order(self) -> dict:
        logging.info("Requesting Port Scan order from api")
        url = self.api_url + "/scan/port-scan-order"
        headers = {
            "Token": self.token,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 201:
            msg = f"Failed to get port scan order, got response code: {response.status_code}"
            msg += f"\n{response.text}"
            logging.error(msg)
            exit(1)
        response_json = response.json()
        logging.info("Recieved port scan orders: \n\n%s\n\n" % response_json)
        return response_json

    def scan_port_submit(self, device_mac_id: int, data: dict) -> bool:
        """Submit port scan data"""
        logging.info("Sunmitting Port Scan to api")
        url = self.api_url + "/scan/submit-port/%s" % device_mac_id
        headers = {
            "Token": self.token,
            "Content-Type": "application/json"
        }
        logging.info("Submitting payload: %s" % data)
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            msg = f"Failed to submit port scan, got response code: {response.status_code}"
            msg += f"\n{response.text}"
            logging.error(msg)
            exit(1)
        response_json = response.json()
        print(response_json)
        logging.info("Successfully submitted port scan to api")
        # logging.info("Recieved port scan orders: \n\n%s\n\n" % response_json)
        return response_json
        


if __name__ == "__main__":
    Scanner().run()

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/scan.py
