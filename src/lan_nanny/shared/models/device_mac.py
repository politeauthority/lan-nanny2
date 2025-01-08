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
    "ip": {
        "name": "ip",
        "type": "str",
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
        "name": "last_access",
        "type": "datetime",
        "api_searchable": True
    },
    "last_port_scanccess": {
        "name": "last_access",
        "type": "datetime",
        "api_searchable": True
    },
    "identified": {
        "name": "identified",
        "type": "bool",
        "api_searchable": True
    },
    "hide": {
        "name": "hide",
        "type": "bool",
        "api_searchable": True
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
