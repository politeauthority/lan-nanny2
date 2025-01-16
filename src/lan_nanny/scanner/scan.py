"""
    Lan Nanny - Scanner
    Scan
    Main entrypoint to the Scan portion of Lan Nanny
"""
import logging
from logging.config import dictConfig

import arrow
import requests

from lan_nanny.shared.utils import log_configs
from lan_nanny.scanner.modules.nmap_scan import NmapScan
from lan_nanny.scanner.utils import glow
from lan_nanny.client import LanNannyClient

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


if glow.general["ENV"].lower() == "dev":
    logging.config.dictConfig(log_configs.config_dev)
else:
    logging.config.dictConfig(log_configs.configs_prod)
logger = logging.getLogger(__name__)
logger.propagate = True


class Scanner:

    def __init__(self):
        self.api_client = LanNannyClient()
        self.process_start = None
        self.process_end = None
        self.options = []
        self.scan_data = {}

    def run(self) -> bool:
        """Primary entrypot for Scan"""
        if glow.general["ENV"] == "DEV":
            logging.info("\n\n  -- Development Environment -- ")
        logging.info("Running Scanner")
        self.hydrate()
        if not self.options["scan-enabled"]["value"]:
            logging.warning("Scanning is not enabled by Lan Nanny Options, exiting")
            exit(0)
        self.run_host_scan()
        self.run_extra_scans()

    def hydrate(self):
        """Hydrate get information needed to run the Scanner.
         - Options
        """
        logging.info("Getting options")
        self.options = self.api_client.get_options()
        logging.info("Successfully got Options from Lan Nanny Api")
        return True

    def run_host_scan(self) -> bool:
        """Run and manage the host scan of the given network."""
        if not self.options["scan-hosts-enabled"]["value"]:
            logging.info("Host scanning is not enabled by Lan Nanny Options, exiting")
            return True
        self.process_start = arrow.utcnow()
        self.run_hosts()
        self.host_scan_submit()
        self.process_end = arrow.utcnow()
        elapsed = (self.process_end - self.process_start)
        logging.info("Finished Host Scan process in %s.%s seconds" % (
            (elapsed.seconds, elapsed.microseconds)))
        return True

    def run_hosts(self) -> bool:
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

    def host_scan_submit(self) -> bool:
        """Submit a Scan to the Lan Nanny Api"""
        logging.info("Starting to submit the Scan")
        submitted = self.api_client.submit_host_scan(self.scan_meta, self.scan_data)
        if submitted:
            logging.info("Submitted scan successfully")
        else:
            logging.error("Failed submitting scan")
        return True

    def run_extra_scans(self) -> bool:
        """Ask the api for other scan operations for the Agent to run.
        """
        self.run_port_scan()
        return True

    def run_port_scan(self) -> bool:
        """Run Port Scans against a suggested target on the network."""
        if not self.options["scan-ports-enabled"]["value"]:
            logging.info("Port scanning is not enabled by Lan Nanny Options, exiting")
            return True
        attempt_threshold = 1
        port_scan_order = self.api_client.get_port_scan_order()
        if len(port_scan_order["scan_targets"]) == 0:
            logging.warning("Got no hosts ready for port scanning from api.")
            return True
        else:
            logging.info("Got %s hosts ready for port scanning, only attempting %s on this run." % (
                len(port_scan_order["scan_targets"]),
                attempt_threshold
            ))
        device_mac = port_scan_order["scan_targets"][0]
        logging.debug("CLIENT: HANDLE PORT SCAN: Chose first DeviceMac: %s" % device_mac)
        nmap = NmapScan()
        results = nmap.run_port_scan(device_mac["last_ip"])
        if not results:
            logging.error("Couldnt get results from port scan")
            return False
        # self.scan_data = results["data"]
        self.scan_meta = nmap.scan_meta
        self.scan_data = results["ports"]
        logging.info("SCAN_META: \n%s" % self.scan_meta)
        logging.info("SCAN_RESULTS: \n%s" % self.scan_data)
        self.port_scan_submit(device_mac["id"], self.scan_meta, self.scan_data)
        return True

    def port_scan_submit(self, device_mac_id: int, scan_meta: dict, scan_data: dict) -> bool:
        """Submit a Port Scan to the Lan Nanny Api"""
        logging.info("Starting to submit the Port Scan")
        submitted = self.api_client.submit_port_scan(device_mac_id, scan_meta, scan_data)
        if submitted:
            logging.info("Submitted scan successfully")
        else:
            logging.error("Failed submitting scan")
        return True

if __name__ == "__main__":
    Scanner().run()

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/scan.py
