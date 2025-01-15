"""
    Lan Nanny - Api
    Utils - Handle Scan
    Primary Handler for all Scan data submitted through the api.

"""

import logging

import arrow
from flask import request

from lan_nanny.api.models.device import Device
from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.models.device_mac import DeviceMac
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.models.scan import Scan
from lan_nanny.api.collects.vendors import Vendors
from lan_nanny.api.models.vendor import Vendor


class HandleScan:

    def __init__(self):
        self.scan = Scan()
        self.scan_data = {}
        self.device_col = Devices()
        self.devices = {}
        self.device_macs_col = DeviceMacs()
        self.device_macs = {}
        self.vendors_col = Vendors()
        self.tasks = {
            "created": {},
        }

    def run(self, data: dict) -> bool:
        """Run a single Scan's data through the system."""
        logging.info("Starting Handle Scan")
        self.scan_data = data
        self.hydrate()
        # logging.info("Recived Scan: %s" % data)
        for host_mac, host_data in data["hosts"].items():
            self.handle_host(host_data)
        # self.handle_finalize()

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

    def handle_host(self, host_data: dict) -> bool:
        """Handle a single host data information coming from a scan."""
        logging.info("Handling Host: %s" % host_data)

        # Handle Vendor
        if "vendor" not in host_data:
            logging.error("Payload is missing Host Vendor data")
        else:
            vendor_id = self.handle_host_vendor(host_data["vendor"])
            logging.info("Got Vendor ID: %s" % vendor_id)
        # Handle Device Mac
        device_mac = self.handle_device_mac(host_data, vendor_id)
        if device_mac.device_id:
            self.handle_device(device_mac)

    def handle_host_vendor(self, vendor_name: str) -> int:
        """Get the Vendor ID for a given Vendor based on name, returning the Vendor ID. As well as
        creating Vendor if needed.
        :ret: int
        """
        if not vendor_name:
            return None
        logging.info("Handling Vendor: %s" % vendor_name)
        create = True
        vendor_id = None
        for vendor in self.vendors:
            if vendor.name == vendor_name:
                create = False
                vendor_id = vendor.id
                break
        logging.debug("Vendor: %s" % vendor_name)
        if create:
            vendor = Vendor()
            vendor.name = vendor_name
            if vendor.save():
                logging.debug("Saved %s" % vendor)
                self.tasks["created"]["vendors"] = [vendor]
                vendor_id = vendor.id
                self.vendors.append(vendor)
        return vendor_id

    def handle_device_mac(self, host_data: dict, vendor_id: int) -> DeviceMac:
        """Handle the Scan's device mac address for a single discovered host. If the Device Mac is
        associated to known Device.id we will return that Device.Id, or False if not."""
        logging.info("Starting handling of Device Mac")
        # If it's a new DeviceMac
        if host_data["mac"] not in self.device_macs:
            device_mac = DeviceMac()
            device_mac.address = host_data["mac"]
            device_mac.first_seen = arrow.utcnow()

        # If its a known mac address
        else:
            device_mac = self.device_macs[host_data["mac"]]

        device_mac.last_seen = arrow.utcnow()
        if vendor_id:
            device_mac.vendor_id = vendor_id
        device_mac.last_ip = host_data["ipv4"]

        if not device_mac.save():
            logging.error("Could not save device mac for host: %s" % device_mac)
        else:
            logging.info("Saved new unqique MAC: %s" % device_mac.address)
        if device_mac.device_id:
            logging.info("Device ID: %s" % device_mac.device_id)
        return device_mac

    def handle_device(self, device_mac: DeviceMac) -> Device:
        """Handle updating a single Device."""
        logging.info("Handling Device: %s" % device_mac.device_id)
        if device_mac.device_id not in self.devices:
            logging.error("Cant find a Device with ID: %s" % device_mac.device_id)
            return False
        device = self.devices[device_mac.device_id]
        if not device.first_seen:
            device.first_seen = device_mac.first_seen
        if not device.vendor_id:
            device.vendor_id = device_mac.vendor_id
        device.last_seen = device_mac.last_seen
        device.ip = device_mac.last_ip
        if device.save():
            logging.info("Saved %s" % device)
        else:
            logging.error("Failed to saved %s" % device)
        return device

    def handle_finalize(self):
        """Handle the wrap up of the Scan import."""
        self.scan.scan_time = ""

# End File: politeauthroity/lan-nanny/src/lan_nanny/api/utils/handle_scan.py
