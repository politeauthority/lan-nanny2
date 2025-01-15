"""
    Lan Nanny - Api
    Model Device

"""
from lan_nanny.shared.models.device import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class Device(BaseEntityMeta):

    model_name = "device"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Device, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "devices"
        self.createable = True
        self.setup()

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/device.py
