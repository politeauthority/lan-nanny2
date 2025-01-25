"""
    Lan Nanny - Api
    Model Device

"""
import logging

from lan_nanny.shared.models.device import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class Device(BaseEntityMeta):

    model_name = "device"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Device, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "devices"
        self.createable = True
        self.setup()

    def delete(self) -> bool:
        """Delete a Device removing it from all it's other participating records."""
        device_id = self.id
        self._scrub_device_id_from_device_macs(device_id)
        super(Device, self).delete()
        return True

    def _scrub_device_id_from_device_macs(self, device_id: int) -> bool:
        sql = """
            UPDATE device_macs
            SET device_id = NULL
            WHERE device_id = %s;
        """
        self.cursor.execute(sql, (device_id,))
        # self.cursor.commit()
        logging.info("Removed DEVICE ID: %s from device_macs" % device_id)
        return True

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/device.py
