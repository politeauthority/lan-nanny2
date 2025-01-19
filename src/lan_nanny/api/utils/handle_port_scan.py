"""
    Lan Nanny - Api
    Utils
    Handle Port Scan
    Primary handler for Port Scans submitted to the Lan Nanny Api

"""

import logging

import arrow
from flask import request

from lan_nanny.api.models.device import Device
from lan_nanny.api.models.device_port import DevicePort
from lan_nanny.api.models.device_mac import DeviceMac
from lan_nanny.api.collects.device_ports import DevicePorts
from lan_nanny.api.models.scan_port import ScanPort


class HandlePortScan:

    def __init__(self):
        self.scan_meta = {}
        self.scan_data = {}
        self.mac_address = ""
        self.device_mac = DeviceMac()
        self.device = Device()
        self.device_ports_col = DevicePorts()
        self.device_ports = []
        self.scan = ScanPort()
        # self.scan_data = {}
        # self.device_id = None
        # self.device_col = Devices()
        # self.devices = {}
        # self.device_macs_col = DeviceMacs()
        # self.device_macs = {}
        # self.vendors_col = Vendors()
        self.tasks = {
            "created": {},
        }

    def run(self, mac_address: str, scan_meta: dict, scan_data: dict) -> bool:
        """Run a single Scan's data through the system."""
        logging.info("Starting Handle Scan")
        self.scan_meta = scan_meta
        self.scan_data = scan_data
        self.mac_address = mac_address

        self.setup_scan()

        self.scan.scan_success = True
        if not self.hydrate():
            logging.error("Hydrate failed exiting Handle Port Scan")
            return False

        logging.info("Processing scan for: %s" % self.device_mac)
        self.process_ports(scan_data)
        self.handle_finalize()
        return True

    def run_error(self, mac_address: str, scan_meta: dict):
        """
        @todo: hydrate here is greedy
        """
        self.mac_address = mac_address
        self.scan_meta = scan_meta
        logging.info("Handling Port Scan error")
        self.setup_scan()
        if not self.hydrate():
            logging.error("Hydrate failed exiting Handle Port Scan")
            return False

        self.scan.scan_success = False
        self.scan.save()
        self.handle_finalize()
        return True

    def setup_scan(self) -> bool:
        """Setup the Scan Port record and prepare for the parsing the data."""
        logging.debug("\n\nScan meta\n\n")
        self.scan.scan_agent = "Unknown"
        if "User-Agent" in request.headers:
            self.scan.user_agent = request.headers["User-Agent"]
        # @todo: This is stupid fucking fragile
        if "scan_time" in self.scan_meta and isinstance(self.scan_meta["scan_time"], str):
            self.scan_time = arrow.get(self.scan_meta["scan_time"][:-7])
        else:
            self.scan_time = None
            logging.error("Unable to set scan time from meta data")
        self.scan_agent = "nmap"
        self.scan.scan_command = self.scan_meta["cmd"]
        self.scan.scan_type = self.scan_meta["type"]
        self.scan.scan_time = self.scan_time.datetime
        self.scan.elapsed_time = self.scan_meta["elapsed"]
        # self.scan,elapsed_time = ""
        return True

    def hydrate(self) -> bool:
        """To run this Host Scan we need to hydrate the following resources to the class to ensure
        we have all the runtime data we need.
        """
        logging.info("Hydrating Host Scan Data")
        if not self.device_mac.get_by_mac(self.mac_address):
            logging.error("Unabled to find Device Mac with mac address: %s" % self.mac_address)
            return False
        logging.debug("Hydrating data for: %s" % self.device_mac)

        if self.device_mac.device_id:
            self.device.get_by_id(self.device_mac.device_id)
        else:
            logging.debug("Device Mac does not have a Device.id: %s" % self.device_mac)

        self.device_ports = self.device_ports_col.get_by_device_mac_id(self.device_mac.id)
        logging.debug("Loaded %s DevicePorts" % len(self.device_ports))

        self.scan.device_mac_id = self.device_mac.id
        self.scan.ports_found = len(self.scan_data)
        if not self.scan.save():
            logging.error("Failed to save Scan Port")
            return False
        logging.info("Completed hydration")
        return True

    def process_ports(self, scan_data) -> bool:
        logging.info("Processing Scan Port Data")
        for port_found in scan_data:
            self.process_single_port(port_found)

    def process_single_port(self, port_found: dict) -> bool:
        found_device_port = self._match_existing_device_port(port_found)
        if found_device_port:
            device_port = found_device_port
        else:
            device_port = DevicePort()
            device_port.device_mac_id = self.device_mac.id
            device_port.first_seen = self.scan_time
            device_port.protocol = port_found["protocol"]
            device_port.port_num = port_found["port_id"]

        if self.device:
            device_port.device_id = self.device.id
        device_port.last_seen = self.scan_time.datetime
        device_port.status = port_found["state"]
        device_port.last_scan_port_id = self.scan.id
        if device_port.save():
            logging.info("Saved %s successfully" % device_port)
            return True
        else:
            logging.error("Error saving: Device Port")
            return False

    def handle_finalize(self) -> bool:
        """Handle the wrap up of the Scan import."""
        self.device_mac.last_port_scan = self.scan_time.datetime
        if not self.device_mac.save():
            logging.error("Failed to saved %s" % self.device_mac)
        else:
            logging.info("Saved: %s" % self.device_mac)
        logging.info("Saved Scan Port")
        return True

    def _match_existing_device_port(self, port_data: dict):
        for device_port in self.device_ports:
            if (
                device_port.protocol == port_data["protocol"] and
                device_port.port_num == port_data["port_id"]):
                return device_port
        else:
            return None

# End File: politeauthroity/lan-nanny/src/lan_nanny/api/utils/handle_port_scan.py
