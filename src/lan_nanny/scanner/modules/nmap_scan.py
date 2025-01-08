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

    def run_scan(self):
        self.export_file = os.path.join(self.tmp_space, "output.xml")
        scan_cidr = "192.168.50.1"
        scan_options = []
        cmd = ["nmap", scan_cidr, "-oX", self.export_file]

        print(f"Running scan {scan_cidr} options: {scan_options} export file: {self.export_file}")
        # subprocess.check_output(cmd)
        self.parse_scan()

    def parse_scan(self):
        if not self.export_file:
            logging.crtiical("No Export file to read, unable to parse file")
            exit(1)
            return False
        # Open and read the XML file
        with open(self.export_file, "r") as file:
            contents = file.read()

        # Parse the XML
        soup = BeautifulSoup(contents, 'xml') 

        hosts = soup.find_all('host')
        for book in hosts:
            title = book.find('title').text
            author = book.find('author').text
            print(f"Title: {title}, Author: {author}")

        import ipdb; ipdb.set_trace()



# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/nmap_scan.py