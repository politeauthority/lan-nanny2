"""
    Lan Nanny - Api
    Model DeviceMac

"""
from lan_nanny.shared.models.device_mac import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class DeviceMac(BaseEntityMeta):

    model_name = "device_macs"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(DeviceMac, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "device_macs"
        self.createable = True
        self.setup()


# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/device_mac.py
