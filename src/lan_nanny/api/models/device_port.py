"""
    Lan Nanny - Api
    Model
    Device Port

"""
from lan_nanny.shared.models.device_port import FIELD_MAP
from lan_nanny.api.models.base_entity_meta import BaseEntityMeta


class DevicePort(BaseEntityMeta):

    model_name = "device_ports"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(DevicePort, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.table_name = "device_ports"
        self.createable = True
        self.setup()

    def get_by_scan_details(self, device_mac_id: int, port_id: int, protocol: str):
        """Get a DevicePort based off of a DeviceMac.id, Port number (port_id), and protocol.
        """
        sql = """
            SELECT *
            FROM device_ports
            WHERE
                device_mac_id = %s AND
                port_id = %s AND
                protocol = %s;
        """
        self.cursor.execute(sql, (device_mac_id, port_id, protocol))
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: politeauthority/lan-nanny/src/lan_nanny/api/models/device_port.py
