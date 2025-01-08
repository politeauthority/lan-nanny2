"""
    Lan Nanny - Scanner

"""

from lan_nanny.scanner.modules.nmap_scan import NmapScan


class Scanner:

    def run(self):
        """Primary entrypot for Scan"""
        print("Running Scanner")
        self.run_nmap()

    def run_nmap(self):
        nmap = NmapScan()
        nmap.run_scan()



if __name__ == "__main__":
    Scanner().run()

# End File: politeauthority/lan-nanny/src/lan_nanny/scanner/scan.py
