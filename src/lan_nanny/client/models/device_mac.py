"""
    Lan Nanny - Client
    Model
    Device Mac

"""
from lan_nanny.shared.models.device_mac import FIELD_MAP
from lan_nanny.client.models.base import Base


class DeviceMac(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(DeviceMac, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "device_mac"
        self.model_url = "device-mac"
        self.setup()
    
    def get_by_ip(self, ip: str):
        dm = self.get_by_field(field_name="ip", field_value=ip)
        print(dm)
        import ipdb; ipdb.set_trace()
        

# End File: politeauthority/lan-nanny/src/lan_nanny/client/models/device_mac.py
