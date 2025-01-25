"""
    Lan Nanny - Api
    Collection
    Devices

"""
import logging

import arrow

from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.device import Device


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

    def num_online(self, online_threshold: int = None) -> int:
        sec_per_min = 60
        logging.info("Getting Devices Online")
        sql = """
            SELECT count(*)
            FROM devices
            WHERE
                last_seen IS NOT null AND
                last_seen >= %s;
        """
        now = arrow.utcnow()
        if not online_threshold:
            # 20 minutes
            online_threshold = (sec_per_min * 20) * -1
        last_seen = str(now.shift(seconds=online_threshold).datetime)[:-13]
        logging.info("\n\nSQL:\n%s"  % sql)
        logging.info("\n\nVALUES\n%s"  % last_seen)
        self.cursor.execute(sql, (last_seen,))
        raw = self.cursor.fetchone()
        logging.info("Got this back: %s" % raw)
        return raw[0]

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/devices.py
