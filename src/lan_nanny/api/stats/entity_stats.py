"""
"""

from lan_nanny.api.collects.devices import Devices
from lan_nanny.api.collects.device_macs import DeviceMacs


def get_online_now():
    d_col = Devices()
    dm_col = DeviceMacs()
    ret = {
        "device_macs_online": dm_col.num_online(),
        "devices_online": d_col.num_online(),
    }
    return ret

# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/stats/entity_stats.py
