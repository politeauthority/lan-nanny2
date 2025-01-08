"""
    Bookmark Api
    Model
    Entity Meta

How to use:
    The Bookmark model is a good example to follow.

    To give a model the ability to use EntityMetas the class must:
        - extend the BaseEntityMeta
        - define a `self.metas = {}` in the init

    To set a new EntityMeta value for an object which may or may not have the EntityMeta yet.
        if 'notes' not in device.metas:
            # Create the notes meta if it doesn't exist
            device.metas['notes'] = EntityMeta()
            device.metas['notes'].create(
                meta_name='notes',
                meta_type='str',
                meta_value=device_notes)
        else:
            # Update the device notes.
            device.metas['notes'].value = request.form['device_notes']

"""
import logging

from polite_lib.utils import xlate
from polite_lib.utils import date_utils

from lan_nanny.shared.models.entity_meta import FIELD_MAP, FIELD_META
from lan_nanny.api.models.base import Base


class EntityMeta(Base):

    def __init__(self, conn=None, cursor=None):
        super(EntityMeta, self).__init__(conn, cursor)

        self.table_name = 'entity_metas'
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.createable = True
        self.setup()

    def __repr__(self):
        """Set the class representation
        :unit-test: TestEntityMeta::__repr__
        """
        if self.entity_type and self.name:
            return "<EntityMeta %s %s:%s>" % (self.entity_type, self.name, self.value)
        return "<EntityMeta>"

    def build_from_list(self, raw: list):
        """Build a model from an ordered list, converting data types to their desired type where
        possible.
        :param raw: A list of raw results from the database.
        @todo: This doesnt cover enough meta data type potentials
        """
        count = 0
        for field, info in self.field_map.items():
            setattr(self, info['name'], raw[count])
            count += 1
        if self.type == "bool":
            self.value = xlate.convert_str_to_bool(raw[7])
        elif self.type == "int":
            self.value = self.convert_str_to_int(raw[7])
        else:
            self.value = raw[7]
        return True

    def create(
        self,
        meta_name: str,
        meta_type: str,
        entity_id: int,
        meta_value: str = None
    ) -> bool:
        """Initiate a new EntityMeta object with a name, type and optional value.

        :param meta_name: The meta key name for the entity meta.
        :param meta_type: The meta's data type. Supported str, int and bool currently.
        :param meta_value: The value to set for the meta.
        """
        self.name = meta_name
        self.type = meta_type
        self.entity_id = entity_id
        self.value = meta_value
        self.entity_type = self.table_name

        # Validate the data type for the entity meta
        if self.type not in ['str', 'int', 'bool']:
            raise AttributeError('Invalid EntityMeta type: %s' % self.type)

        # Validate the entity_type, which requires the model to set the `self.table_name` var.
        if not self.entity_type:
            raise AttributeError(
                "Invalid EntityType type: %s, must set model's self.table_name" % self.entity_type)

        return True

    def json(self) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. This
        instance extends the Base Model's json method and adds "clusters" to the output.
        """
        json_ret = {
            "created_ts": date_utils.json_date(self.created_ts),
            "updated_ts": date_utils.json_date(self.updated_ts),
            "name": self.name,
            "type": self.type,
            "value": self.value
        }
        return json_ret

    def convert_str_to_int(self, value: str) -> bool:
        """Convert a string value to an int value if one can be derrived.
        :unit-test: TestXlate::test__convert_str_to_int
        """
        if not value:
            return None
        if isinstance(value, int):
            return value
        if not isinstance(value, str):
            logging.error('Cannot convert value "%s" of type %s to int' % (value, type(value)))
            return None
        if value.isdigit():
            return int(value)
        else:
            logging.error('Cannot convert value "%s" of type %s to int' % (value, type(value)))
            return None

# End File: politeauthority/bookmarky-api//src/api/models/entity_meta.py
