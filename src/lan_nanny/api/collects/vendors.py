"""
    Lan Nanny - Api
    Collection Vendors

"""
from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.vendor import Vendor


class Vendors(BaseEntityMetas):

    collection_name = "vendors"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(Vendors, self).__init__(conn, cursor)
        self.table_name = Vendor().table_name
        self.collect_model = Vendor
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/lan-nannyi/src/lan_nanny/api/collects/venors.py
