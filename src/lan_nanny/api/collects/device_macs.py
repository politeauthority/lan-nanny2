"""
    Lan Nanny - Api
    Collection DeviceMacs

"""
import arrow

from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.device_mac import DeviceMac


class DeviceMacs(BaseEntityMetas):

    collection_name = "device_macs"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(DeviceMacs, self).__init__(conn, cursor)
        self.table_name = DeviceMac().table_name
        self.collect_model = DeviceMac
        self.field_map = self.collect_model().field_map
        self.per_page = 20
    
    def ready_for_port_scan(self) -> list:
        """Gets a list of DeviceMacs that are allowed to have port scans and have been recently
        seen online.
        """
        last_seen = arrow.utcnow()
        last_seen_search = last_seen.shift(minutes=-120)
        sql = """
            SELECT *
            FROM device_macs
            WHERE
                port_scan_enabled = true AND
                last_seen >= %s
            ORDER BY last_port_scan DESC
            LIMIT 10;
        """
        self.cursor.execute(sql, (last_seen_search.datetime,))
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

# End File: politeauthority/lan-nanny/src/lan_nannyy/api/collects/device_macs.py
