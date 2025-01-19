"""
    Lan Nanny - Api
    Collection
    Device Ports

"""
from lan_nanny.api.collects.base_entity_metas import BaseEntityMetas
from lan_nanny.api.models.device_port import DevicePort


class DevicePorts(BaseEntityMetas):

    collection_name = "device_ports"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
        collections target model.
        """
        super(DevicePorts, self).__init__(conn, cursor)
        self.table_name = DevicePort().table_name
        self.collect_model = DevicePort
        self.field_map = self.collect_model().field_map
        self.per_page = 20

    def get_by_device_mac_id(self, device_mac_id: int) -> list:
        """Get DevicePorts by DeviceMac.id"""
        sql = """
            SELECT *
            FROM device_ports
            WHERE
                device_mac_id = %s;
        """
        self.cursor.execute(sql, (device_mac_id,))
        raws = self.cursor.fetchall()
        return self.build_from_lists(raws)

# End File: politeauthority/lan-nanny/src/lan_nannyy/api/collects/device_port.py
