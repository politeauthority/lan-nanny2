"""
    Lan Nanny - Shared
    Model
    Scan Hosts

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
    "scan_agent": {
        "name": "scan_agent",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "scan_type": {
        "name": "scan_type",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "hosts_found": {
        "name": "hosts_found",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "scan_command": {
        "name": "scan_command",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "scan_time": {
        "name": "scan_time",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "raw_data": {
        "name": "raw_data",
        "type": "json",
        "api_writeable": True,
        "api_searchable": True
    },
}


# End File: politeauthority/lan-nanny/src/lan-nanny/shared/models/scan_host.py
