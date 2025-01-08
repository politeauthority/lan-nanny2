"""
    Lan Nanny - Api
    Model Vendor

"""
from lan_nanny.shared.models.vendor import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class Vendor(BaseEntityMeta):

    model_name = "device"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Vendor, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "vendors"
        self.createable = True
        self.setup()

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/vendor.py
