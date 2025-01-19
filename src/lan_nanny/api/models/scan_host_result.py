"""
    Lan Nanny - Api
    Model
    Scan Host Result

"""
from lan_nanny.shared.models.scan_host import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class ScanHostResult(BaseEntityMeta):

    model_name = "scan_host_result"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ScanHostResult, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "scan_hosts"
        self.createable = True
        self.setup()

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/scan_host_result.py
