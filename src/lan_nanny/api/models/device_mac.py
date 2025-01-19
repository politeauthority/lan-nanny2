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

    def __repr__(self):
        """Model representation.
        """
        if self.id:
            if self.address:
                return "<%s: %s - %s>" % (self.__class__.__name__, self.id, self.address)
            else:
                return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_by_mac(self, mac_address: str) -> bool:
        """Get a DeviceMac by a mac address."""
        return self.get_by_field("address", mac_address)

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/device_mac.py
