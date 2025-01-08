"""
    Lan Nanny - Scanner
    Nmap

"""
from bs4 import BeautifulSoup

import logging
import os
import subprocess


class NmapScan:

    def __init__(self):
        self.tmp_space = "/tmp"
        self.export_file = ""
        self.data = {
            "meta": {
                "scan_type": "nmap"
            },
            "hosts": {}
        } 

    def run_scan(self):
        self.export_file = os.path.join(self.tmp_space, "output.xml")
        scan_cidr = "192.168.50.1-20"
        scan_options = []
        cmd = ["nmap", scan_cidr, "-oX", self.export_file]

        print(f"Running scan {scan_cidr} options: {scan_options} export file: {self.export_file}")
        subprocess.check_output(cmd)
        self.parse_scan()

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
                "mac_addr": "",
            }
            addresses = host.find_all('address')

            for address in addresses:
                addy_atrrs = address.attrs
                if "addrtype" in addy_atrrs and addy_atrrs["addrtype"] == "ipv4":
                    device["ipv4"] = addresses[1].attrs["addr"]
                elif "addrtype" in addy_atrrs and addy_atrrs["addrtype"] == "mac":
                    device["mac"] = addresses[1].attrs["addr"]
            if not device["mac"]:
                logging.error("Device has not mac_address. {address}")
                continue
            self.data["hosts"][device["mac"]] = device
        return True

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/nmap_scan.py
