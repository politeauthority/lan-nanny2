"""
    Lan Nanny - Api
    Collection
    Devices

"""
from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.device import Device
from lan_nanny.api.utils import glow


class Devices(BaseEntityMetas):

    collection_name = "devices"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(Devices, self).__init__(conn, cursor)
        self.table_name = Device().table_name
        self.collect_model = Device
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/bookmarks.py
