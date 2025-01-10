"""
    Lan Nanny - Api
    Model Scan

"""
from lan_nanny.shared.models.scan import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class Scan(BaseEntityMeta):

    model_name = "scan"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Scan, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "scans"
        self.createable = True
        self.setup()

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/scan.py
