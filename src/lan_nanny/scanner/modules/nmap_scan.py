"""
    Lan Nanny - Scanner
    Nmap

"""
import logging
import os
import subprocess


class NmapScan:

    def __init__(self):
        self.tmp_space = "/tmp"

    def run_scan(self):
        export_file = os.path.join(self.tmp_space, "output.xml")
        scan_cidr = "192.168.50.1"
        scan_options = []
        cmd = ["nmap", scan_cidr, "-oX", export_file]
        print(f"Running scan {scan_cidr} options: {scan_options}")
        x = subprocess.check_output(cmd)
        print(x)

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/nmap_scan.py