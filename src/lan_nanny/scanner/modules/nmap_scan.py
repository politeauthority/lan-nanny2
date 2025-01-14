"""
    Lan Nanny - Scanner
    Nmap
    Runs and manages the parsing of an Nmap scan to a format that Lan Nanny is ready to read.

"""
from bs4 import BeautifulSoup

import logging
import os
import time
import subprocess


class NmapScan:

    def __init__(self):
        self.tmp_space = "/tmp"
        self.export_file = ""
        self.scan_start = None
        self.scan_end = None
        self.scan_total = None
        self.cmd = None
        self.scan_meta = {
            "type": "nmap",
            "cmd": ""
        }
        self.data = {
            "hosts": {}
        }

    def run_scan(self):
        """Wrapper for the Nmap scan"""
        self.export_file = os.path.join(self.tmp_space, "output.xml")
        scan_cidr = "192.168.50.1-255"
        # scan_options_cli = ""
        # scan_options = []
        # # scan_options.append("Pn")
        # scan_options.append("-sn")
        # if scan_options:
        #     for opt in scan_options:
        #         scan_options_cli += f" {opt}"
        scan_options_cli = "-sn"
        self.cmd = ["nmap", scan_cidr, scan_options_cli, "-oX", self.export_file]
        logging.info(
            f"Running scan {scan_cidr} options: {scan_options_cli} export file: {self.export_file}")
        self.scan_start = time.time()
        subprocess.check_output(self.cmd)
        self.scan_end = time.time()
        self.scan_total = self.scan_end - self.scan_start
        logging.info("Finished Nmap scan in %s" % self.scan_total)
        # logging.debu("Finished Nmap Scan")
        self.parse_scan()
        self.scan_meta["cmd"] = " ".join(self.cmd)
        return True

    def parse_scan(self) -> bool:
        """Parses an Nmap XML file, returnning da data structure of unique devices in a python3
        dictionary.
        :ret: {
            "meta": {
                "scan_type": "nmap
            },
            "hosts: {
                "00:00:00:00:00:00" {
                    "ipv4: "192.168.50.1",
                    "mac: "192.168.50.1",
                }
            }
        }
        """
        if not self.export_file:
            logging.crtiical("No Export file to read, unable to parse file")
            exit(1)
            return False
        # Open and read the XML file
        with open(self.export_file, "r") as file:
            contents = file.read()
        soup = BeautifulSoup(contents, 'xml')
        hosts = soup.find_all('host')
        for host in hosts:
            device = {
                "ipv4": "",
                "mac": "",
                "vendor": ""
            }
            addresses = host.find_all('address')

            for address in addresses:
                addy_atrrs = address.attrs
                if "addrtype" in addy_atrrs and addy_atrrs["addrtype"] == "ipv4":
                    device["ipv4"] = address.attrs["addr"]
                elif "addrtype" in addy_atrrs and addy_atrrs["addrtype"] == "mac":
                    device["mac"] = address.attrs["addr"]
                    if "vendor" in address.attrs:
                        device["vendor"] = address.attrs["vendor"]
            if not device["mac"]:
                logging.error("Device has not mac_address. {address}")
                continue
            self.data["hosts"][device["mac"]] = device
        return True

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/nmap_scan.py
