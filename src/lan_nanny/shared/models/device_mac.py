"""
    Lan Nanny - Shared
    Model Device Mac

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
    "address": {
        "name": "address",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "last_ip": {
        "name": "last_ip",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "device_id": {
        "name": "device_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "vendor_id": {
        "name": "vendor_id",
        "type": "int",
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
        "api_searchable": True
    },
    "hide": {
        "name": "hide",
        "type": "datetime",
        "api_searchable": True
    },
    "last_port_scan": {
        "name": "last_port_scan",
        "type": "datetime",
        "api_searchable": True
    },
    "port_scan_lock": {
        "name": "port_scan_lock",
        "type": "bool",
        "api_searchable": True
    },
    "host_names": {
        "name": "host_names",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "kind_id": {
        "name": "kind_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "identified": {
        "name": "identified",
        "type": "bool",
        "api_searchable": True
    },

    "deleted": {
        "name": "deleted",
        "type": "bool",
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

# End File: politeauthority/bookmarky-api/src/bookmarky/shared/models/user.py
