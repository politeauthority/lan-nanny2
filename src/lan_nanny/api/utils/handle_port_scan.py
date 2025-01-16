"""
    Lan Nanny - Api
    Utils
    Handle Port Scan
    Primary handler for Port Scans submitted to the Lan Nanny Api

"""

import logging

# import arrow
from flask import request

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.models.scan_port import ScanPort
from lan_nanny.api.collects.vendors import Vendors


class HandlePortScan:

    def __init__(self):
        self.scan = ScanPort()
        self.scan_data = {}
        self.device_id = None
        self.device_col = Devices()
        self.devices = {}
        self.device_macs_col = DeviceMacs()
        self.device_macs = {}
        self.vendors_col = Vendors()
        self.tasks = {
            "created": {},
        }

    def run(self, scan_meta: dict, scan_data: dict) -> bool:
        """Run a single Scan's data through the system."""
        logging.info("Starting Handle Scan")
        self.setup_scan(scan_meta)
        self.scan_data = scan_data
        self.hydrate()
        # logging.info("Recived Scan: %s" % data)
        logging.debug("NOT SURE WTF TO DO HERE")
        self.handle_finalize()
        return True

    def setup_scan(self, scan_meta: dict) -> bool:
        logging.debug("\n\nScan meta\n\n")
        if "User-Agent" in request.headers:
            self.scan.user_agent = request.headers["User-Agent"]
        # logging.debug("\n\nScan meta")
        # logging.debug(scan_meta)
        self.scan.scan_command = scan_meta["cmd"]
        self.scan.scan_type = scan_meta["type"]

    def hydrate(self) -> bool:
        """To run this Host Scan we need to hydrate the following resources to the class to ensure
        we have all the runtime data we need.
        """
        logging.info("Hydrating Host Scan Data")
        device_list = self.device_col.get_all()
        for device in device_list:
            self.devices[device.id] = device
        logging.debug("Hydrage: Loaded %s Devices" % len(self.devices))

        self.device_macs = {}
        device_macs_list = self.device_macs_col.get_all()

        # Convert Device Macs a dict
        for dm in device_macs_list:
            self.device_macs[dm.address] = dm
        logging.debug("Hydrage: Loaded %s Devices" % len(self.device_macs))

        self.vendors = self.vendors_col.get_all()
        logging.debug("Hydrage: Loaded %s Vendors" % len(self.vendors))

        if "User-Agent" in request.headers:
            self.scan.scan_agent = request.headers["User-Agent"]
        else:
            self.scan.scan_agent = "Unknown"
        logging.info("Completed hydration")
        return True

    def handle_finalize(self) -> bool:
        """Handle the wrap up of the Scan import."""
        logging.debug("Saving scan")
        # if not self.scan_data{"ports"}
        if "ports" not in self.scan_data:
            logging.error("No Ports for Port scan to save")
        else:
            self.scan.ports_found = len(self.scan_data["ports"])
        port_scan = self.scan.save()
        if not port_scan:
            logging.error("Failed to save scan!")
        else:
            logging.info("Saved %s" % port_scan)
        return True

# End File: politeauthroity/lan-nanny/src/lan_nanny/api/utils/handle_port_scan.py
