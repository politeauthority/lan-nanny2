"""
    Lan Nanny - Api
    Collection
    DeviceMacs

"""
import logging

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
        self.per_page = 100

    def get_by_device_id(self, device_id: int) -> list:
        """Get a Device by it's ID."""
        prestines = self.get_by_field("device_id", device_id)
        return prestines

    def search(self, query: str):
        """Run a general search on DeviceMacs, returning a hyradted list if any results are found.
        """
        sql = """
            SELECT *
            FROM device_macs
            WHERE
                address LIKE %s OR
                last_ip LIKE %s;
        """
        query = f"%{query}%"
        self.cursor.execute(sql, (query, query))
        raws = self.cursor.fetchall()
        return self.build_from_lists(raws)

    def ready_for_port_scan(self) -> list:
        """Gets a list of DeviceMacs that are allowed to have port scans and have been recently
        seen online.
        @todo: make sure the order here is correct
        """
        device_macs_to_scan = []
        never_scanned = self._rfp_never_scanned()
        the_rest = self._rfp_last_scaned()
        device_macs_to_scan = device_macs_to_scan + never_scanned
        device_macs_to_scan = device_macs_to_scan + the_rest
        return device_macs_to_scan

    def _rfp_never_scanned(self) -> list:
        sql = """
            SELECT *
            FROM device_macs
            WHERE
                port_scan_enabled = true AND
                last_port_scan is NULL
            ORDER BY last_port_scan DESC
            LIMIT 10;
        """
        # the_values = (last_seen_search.datetime,)
        self.cursor.execute(sql)
        # logging.info(self.cursor.mogrify(sql, the_values))
        # self.cursor.execute(sql, the_values)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        return prestines

    def _rfp_last_scaned(self):
        sql = """
            SELECT *
            FROM device_macs
            WHERE
                port_scan_enabled = true
            ORDER BY last_port_scan ASC
            LIMIT 10;
            """
        logging.debug("We're about to run a READY FOR PORT SCAN statement")
        logging.info(self.cursor.mogrify(sql))
        self.cursor.execute(sql)
        # logging.info(self.cursor.mogrify(sql, the_values))
        # self.cursor.execute(sql, the_values)
        raws = self.cursor.fetchall()
        prestines = self.build_from_lists(raws)
        logging.debug("FETURE/PORT-SCAN: Found %s DeviceMac for Port Scanning" % len(prestines))
        return prestines

    def num_online(self, online_threshold: int = None) -> int:
        sec_per_min = 60
        logging.info("Getting Device Macs Online")
        sql = """
            SELECT count(*)
            FROM device_macs
            WHERE
                last_seen IS NOT null AND
                last_seen >= %s;
        """
        now = arrow.utcnow()
        if not online_threshold:
            # 20 minutes
            online_threshold = (sec_per_min * 20) * -1
        last_seen = str(now.shift(seconds=online_threshold).datetime)[:-13]
        logging.info("\n\nSQL:\n%s" % sql)
        logging.info("\n\nVALUES\n%s" % last_seen)
        self.cursor.execute(sql, (last_seen,))
        raw = self.cursor.fetchone()
        logging.info("Got this back: %s" % raw)
        return raw[0]

# End File: politeauthority/lan-nanny/src/lan_nannyy/api/collects/device_macs.py
