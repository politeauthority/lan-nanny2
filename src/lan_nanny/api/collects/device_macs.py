"""
    Lan Nanny - Api
    Collection DeviceMacs

"""
from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.device_mac import DeviceMac


class DeviceMacs(BaseEntityMetas):

    collection_name = "devices"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(DeviceMacs, self).__init__(conn, cursor)
        self.table_name = DeviceMac().table_name
        self.collect_model = DeviceMac
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: politeauthority/lan-nanny/src/lan_nannyy/api/collects/device_macs.py
