"""
    Lan Nanny - Scanner
    Nmap
    Runs and manages the parsing of an Nmap scan to a format that Lan Nanny is ready to read.

"""
import logging
import os
import time
import subprocess

import arrow
from bs4 import BeautifulSoup

from polite_lib.utils import date_utils


class NmapScan:

    def __init__(self):
        self.tmp_space = "/tmp"
        self.export_file = os.path.join(self.tmp_space, "output.xml")
        self.scan_start = None
        self.scan_end = None
        self.scan_total = None
        self.cmd = None
        self.scan_meta = {
            "type": "nmap",
            "cmd": "",
            "scan_time": ""
        }
        self.data = {
            "hosts": {}
        }

    def run_scan(self):
        """Wrapper for the Nmap scan"""
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

    def run_port_scan(self, ip_address: str) -> dict:
        # ip_address = "192.168.50.1"
        cmd = ["nmap", "-Pn", ip_address, "-oX", self.export_file]
        logging.info("Running port scan command: %s" % " ".join(cmd))
        self.scan_meta["cmd"] = " ".join(cmd)
        self.scan_start = time.time()
        try:
            subprocess.check_output(cmd)
        except Exception as e:
            logging.error("Error running port scan: %s" % e)
            return False
        self.scan_end = time.time()
        self.scan_total = self.scan_end - self.scan_start
        self.scan_meta["elapsed"] = self.scan_total
        return self.parse_port_scan()

    def parse_port_scan(self) -> dict:
        """Parses an Nmap XML file for a scan on a single host, extracting port information."""
        if not self.export_file:
            logging.crtiical("No Export file to read, unable to parse file")
            exit(1)
            return False
        # Open and read the XML file
        with open(self.export_file, "r") as file:
            contents = file.read()

        data = {
            "host": {
                "ip_address": "",
                "mac_address": "",
            },
            "ports": []
        }
        soup = BeautifulSoup(contents, 'xml')

        # Get the Device address details
        hosthint = soup.find('hosthint')
        if not hosthint:
            return False
        for addy in hosthint.find_all("address"):
            if addy.attrs["addrtype"] == "ipv4":
                data["host"]["ip_address"] = addy.attrs["addr"]
            elif addy.attrs["addrtype"] == "mac":
                data["host"]["mac_address"] = addy.attrs["addr"]

        # Get the Device port details
        ports = soup.find_all('port')
        for port in ports:
            port_data = {
                "protocol": "",
                "port_id": "",
                "reason": "",
                "state": "",
                "state_reason": "",
                "service_name": ""
            }
            port_data["port_id"] = int(port.attrs["portid"])
            port_data["protocol"] = port.attrs["protocol"]
            if hasattr(port, "state"):
                if port.state.attrs["state"] == "open":
                    port_data["state"] = "open"
                else:
                    port_data["state"] = "closed"
            else:
                port_data["state"] = "unknown"
            if hasattr(port, "service"):
                if "name" in port.service.attrs:
                    port_data["service_name"] = port.service.attrs["name"]
            data["ports"].append(port_data)
        self.scan_meta["scan_time"] = date_utils.json_date(arrow.utcnow().datetime)
        return data


# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/nmap_scan.py
