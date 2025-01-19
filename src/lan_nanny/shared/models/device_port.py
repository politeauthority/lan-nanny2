"""
    Lan Nanny - Shared
    Model Device Ports

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
    "device_id": {
        "name": "device_id",
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
    "last_scan_port_id": {
        "name": "last_scan_port_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "state": {
        "name": "state",
        "type": "varchar",
        "api_writeable": True,
        "api_searchable": True
    },
    "last_seen": {
        "name": "last_seen",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True
    },
    "first_seen": {
        "name": "first_seen",
        "type": "datetime",
        "api_searchable": True,
        "api_writeable": True,
    },
    "protocol": {
        "name": "protocol",
        "type": "str",
        "api_searchable": True,
        "api_writeable": True,
    },
    "port_num": {
        "name": "port_num",
        "type": "int",
        "api_searchable": True,
        "api_writeable": True,
    },
}

# FIELD_MAP_METAS = {
#     "display_hidden": {
#         "name": "display_hidden",
#         "type": "bool"
#     },
#     "beta_features": {
#         "name": "beta_features",
#         "type": "bool"
#     }
# }

FIELD_META = {
    "ux_key": ["device_mac_id", "protocol", "port_num"]
}


# End File: politeauthority/bookmarky-api/src/bookmarky/shared/models/device_ports.py
