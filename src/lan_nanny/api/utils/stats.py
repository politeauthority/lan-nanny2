"""
    Lan Nanny - Api
    Utils
    Stats
    Collect relevant scans for the api.

"""

import logging

from lan_nanny.api.collects.scan_hosts import ScanHosts


def scan_stats() -> dict:
    """Get statitics on Scans run recently."""
    logging.info("Getting scan stats")
    sh_col = ScanHosts()
    scan_hosts_total = sh_col.get_count_all()
    total_scans = scan_hosts_total
    import ipdb; ipdb.set_trace()
    
    ret = {
        "total_scan": total_scans,
        "hosts": {
            "total": scan_hosts_total
        }
    }
    return ret

# End File: politeauthroity/lan-nanny/src/lan_nanny/api/utils/stats.py
