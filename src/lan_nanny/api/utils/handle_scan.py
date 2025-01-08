"""
    Lan Nanny - Api
    Utils Handle Scan

"""

import logging

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.collects.device_macs import DevicesMacs
from lan_nanny.api.collects.vendors import Vendors
from lan_nanny.api.models.vendor import Vendor


class HandleScan:

    def __init__(self):
        self.device_col = Devices()
        self.devices = {}
        self.device_macs_col = DevicesMacs()
        self.device_macs = {}
        self.vendors_col = Vendors()
        self.tasks = {
            "created": {},
        }

    def hydrate(self) -> bool:
        """Load all the data needed to process the Scan event."""
        logging.info("Hydrating Host Scan Data")
        self.devices = self.device_col.get_all()
        logging.debug("Hydrage: Loaded %s Devices" % len(self.devices))
        
        self.device_macs = DevicesMacs.get_all()
        logging.debug("Hydrage: Loaded %s Devices" % len(self.device_macs))
        
        self.vendors = self.vendors_col.get_all()
        logging.debug("Hydrage: Loaded %s Vendors" % len(self.vendors))
        logging.info("Completed hydration")
        return True

    def run(self, data: dict) -> bool:
        logging.info("Starting Handle Scan")
        self.hydrate()
        logging.info("Recived Scan: %s" % data)
        for host_mac, host_info in data["hosts"].items():
            self.handle_host(host_info)

    def handle_host(self, host_data: dict) -> bool:
        """Handle a single host data information coming from a scan."""
        logging.info("Handling Host: %s" % host_data)
        vendor_id = self.handle_host_vendor(host_data["vendor"])
        logging.info("Got Vendor ID: %s" % vendor_id)
        import ipdb; ipdb.set_trace()
        print(vendor_id)

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
