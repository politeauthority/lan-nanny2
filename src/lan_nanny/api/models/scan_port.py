"""
    Lan Nanny - Api
    Model
    Scan Port

"""
from lan_nanny.shared.models.scan_port import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class ScanPort(BaseEntityMeta):

    model_name = "scan_port"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ScanPort, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "scan_ports"
        self.createable = True
        self.setup()

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/scan_scan_port.py
