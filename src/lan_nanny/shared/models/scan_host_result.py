"""
    Lan Nanny - Shared
    Model
    Scan Hosts Result

"""

FIELD_MAP = {
    "id": {
        'name': 'id',
        'type': 'int',
        'primary': True,
    },
    "created_ts": {
        'name': 'created_ts',
        'type': 'datetime',
    },
    "updated_ts": {
        'name': 'updated_ts',
        'type': 'datetime',
    },
    "scan_host_id": {
        "name": "scan_host_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "device_mac_id": {
        "name": "device_mac_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "device_id": {
        "name": "device_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
}


# End File: politeauthority/lan-nanny/src/lan_nanny/shared/models/scan_host_result.py
