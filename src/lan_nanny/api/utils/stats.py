"""
    Lan Nanny - Api
    Utils
    Stats
    Collect relevant scans for the api.

"""

import logging

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.collects.device_macs import DeviceMacs
from lan_nanny.api.collects.device_ports import DevicePorts
from lan_nanny.api.collects.scan_ports import ScanPorts
from lan_nanny.api.collects.scan_hosts import ScanHosts


def entity_stats() -> dict:
    device_col = Devices()
    device_total = device_col.get_count_all()

    device_mac_col = DeviceMacs()
    deivce_macs_total = device_mac_col.get_count_all()

    device_ports_col = DevicePorts()
    deivce_ports_total = device_ports_col.get_count_all()

    ret = {
        "devices": device_total,
        "device_macs": deivce_macs_total,
        "device_ports": deivce_ports_total
    }
    return ret


def scan_stats() -> dict:
    """Get statitics on Scans run recently."""
    logging.info("Getting scan stats")
    sh_col = ScanHosts()
    scan_hosts_total = sh_col.get_count_all()
    
    sp_col = ScanPorts()
    scan_ports_total = sp_col.get_count_all()
    total_scans = scan_hosts_total
    ret = {
        "total_scan": total_scans,
        "hosts": {
            "total": scan_hosts_total
        },
        "ports": {
            "total": scan_ports_total
        }
    }
    return ret

# End File: politeauthroity/lan-nanny/src/lan_nanny/api/utils/stats.py
