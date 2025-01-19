"""
    Lan Nanny - Api
    Collection
    Scan Ports

"""
from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.scan_port import ScanPort


class ScanPorts(BaseEntityMetas):

    collection_name = "scan_ports"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(ScanPorts, self).__init__(conn, cursor)
        self.table_name = ScanPort().table_name
        self.collect_model = ScanPort
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/lan-nanny/src/lan_nanny/api/collects/scan_ports.py
