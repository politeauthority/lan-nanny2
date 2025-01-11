"""
    Lan Nanny - Api
    Utils - Handle Scan
    Primary Handler for all Scan data submitted through the api.

"""

import logging

import arrow

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.collects.vendors import Vendors
from lan_nanny.api.models.device_mac import DeviceMac
from lan_nanny.api.models.vendor import Vendor


class HandleScan:

    def __init__(self):
        self.device_col = Devices()
        self.devices = {}
        self.device_macs_col = DeviceMacs()
        self.device_macs = {}
        self.vendors_col = Vendors()
        self.tasks = {
            "created": {},
        }

    def hydrate(self) -> bool:
        """To run this Host Scan we need to hydrate the following resources to the class to ensure
        we have all the runtime data we need.
        """
        logging.info("Hydrating Host Scan Data")
        self.devices = self.device_col.get_all()
        logging.debug("Hydrage: Loaded %s Devices" % len(self.devices))

        self.device_macs = {}
        device_macs_list = self.device_macs_col.get_all()

        # Convert Device Macs a dict
        for dm in device_macs_list:
            self.device_macs[dm.address] = dm
        logging.debug("Hydrage: Loaded %s Devices" % len(self.device_macs))

        self.vendors = self.vendors_col.get_all()
        logging.debug("Hydrage: Loaded %s Vendors" % len(self.vendors))
        logging.info("Completed hydration")
        return True

    def run(self, data: dict) -> bool:
        """Run a single Scan's data through the system."""
        logging.info("Starting Handle Scan")
        self.hydrate()
        logging.info("Recived Scan: %s" % data)
        for host_mac, host_info in data["hosts"].items():
            self.handle_host(host_info)

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
        self.handle_device_mac(host_data, vendor_id)

    def handle_device_mac(self, host_data: dict, vendor_id: int) -> bool:
        """Handle the Scan's device mac address for a single discovered host."""
        logging.info("Standing Handling of Device Mac")
        # If this is a NEW mac
        if host_data["mac"] not in self.device_macs:
            device_mac = DeviceMac()
            device_mac.address = host_data["mac"]
            device_mac.first_seen = arrow.utcnow()
            if not device_mac.save():
                logging.error("Could not save device mac for host: %s" % device_mac)
            else:
                logging.info("Saved new unqique MAC: %s" % device_mac.address)

        # If its a known mac address
        else:
            logging.debug(host_data)
            logging.debug(self.device_macs)
            device_mac = self.device_macs[host_data["mac"]]

        device_mac.last_seen = arrow.utcnow()
        device_mac.vendor_id = vendor_id
        device_mac.last_ip = host_data["ipv4"]

        if not device_mac.save():
            logging.error("Could not save device mac for host: %s" % device_mac)
        else:
            logging.info("Saved new unqique MAC: %s" % device_mac.address)

    def handle_host_vendor(self, vendor_name: str) -> int:
        """Get the Vendor ID for a given Vendor based on name, returning the Vendor ID. As well as
        creating Vendor if needed.
        :ret: int
        """
        logging.info("Handling Vendor: %s" % vendor_name)
        create = True
        vendor_id = None
        for vendor in self.vendors:
            if vendor.name == vendor_name:
                create = False
                vendor_id = vendor.id
            logging.debug(vendor_name)
        if create:
            vendor = Vendor()
            vendor.name = vendor_name
            if vendor.save():
                logging.debug("Saved %s" % vendor)
                self.tasks["created"]["vendors"] = [vendor]
                vendor_id = vendor.id
                self.vendors.append(vendor)
        if not vendor_id:
            logging.error("Could not find a Vendor ID")
            return False
        return vendor_id

# End File: politeauthroity/lan-nanny/src/lan_nanny/api/utils/handle_scan.py
