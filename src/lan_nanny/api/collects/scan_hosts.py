"""
    Lan Nanny - Api
    Collection
    Scan Hosts

"""
from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.scan_host import ScanHost


class ScanHosts(BaseEntityMetas):

    collection_name = "scan_hosts"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(ScanHosts, self).__init__(conn, cursor)
        self.table_name = ScanHost().table_name
        self.collect_model = ScanHost
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/scan_hosts.py
