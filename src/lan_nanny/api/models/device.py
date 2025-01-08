"""
    Bookmarky Api
    Model Device

"""
from lan_nanny.shared.models.auto_feature import FIELD_MAP
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

    def __repr__(self):
        """Device model representation."""
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        else:
            return "<%s>" % (self.__class__.__name__)

# End File: politeauthority/la-nanny/src/lan_nanny/api/models/device.py.py
