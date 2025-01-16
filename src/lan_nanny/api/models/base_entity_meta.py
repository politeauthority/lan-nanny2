"""
    Cver Api - Model
    Base Entity Meta Model
    Base model class for all models requiring meta storage.

"""
import logging

from lan_nanny.api.models.base import Base
from lan_nanny.api.models.entity_meta import EntityMeta
from lan_nanny.api.utils import glow


class BaseEntityMeta(Base):

    def __init__(self, conn=None, cursor=None):
        """Base Entity Meta model constructor."""
        super(BaseEntityMeta, self).__init__(conn, cursor)
        self.table_name = None
        self.table_name_meta = EntityMeta().table_name
        self.metas = {}

    def __repr__(self):
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_by_id(self, model_id: int) -> bool:
        """Get a single model object from db based on an object ID with all meta data loaded into
           self.metas.
        """
        if not super(BaseEntityMeta, self).get_by_id(model_id):
            return False
        self.load_meta()
        return True

    def build_from_list(self, raw: list, meta=False) -> bool:
        """Build a model from list, and pull its meta data."""
        super(BaseEntityMeta, self).build_from_list(raw)
        if meta:
            self.load_meta()

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        This extends the original to unpack meta objects.
        """
        super(BaseEntityMeta, self).build_from_dict(raw)
        if 'meta' not in raw:
            return True

        for meta_key, meta_value in raw["meta"].items():
            self.meta[meta_key] = meta_value

        return True

    def save(self) -> bool:
        """Extend the Base model save, settings saves for all model self.metas objects.
        @todo: This needs some work, we're having trouble getting the correct value stored.
        """
        super(BaseEntityMeta, self).save()
        if not self.metas:
            # logging.debug("No Meta to save, skipping")
            return True

        if not self.id:
            raise AttributeError('Model %s cant save entity metas with out id' % self)

        logging.debug("Saving Metas")
        existing_metas = self.load_raw_meta()
        logging.debug("Found %s metas to save" % len(self.metas))
        for meta_name, meta in self.metas.items():
            if isinstance(meta, EntityMeta):
                self._save_single_meta(existing_metas[meta_name], meta_name, meta.value)
            else:
                self._save_single_meta(False, meta_name, meta)
        return True

    def json(self, get_api: bool = False) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. If get_api
        is specified and a model doesnt have api_display=False, it will export in the output.
        We extend the Base model's json method and make sure that we also turn the meta fields into
        json friendly output.
        """
        json_out = super(BaseEntityMeta, self).json()
        if not self.metas:
            return json_out
        for meta_key, meta in self.metas.items():
            if isinstance(meta, EntityMeta):
                if "metas" not in json_out:
                    json_out["metas"] = {}
                json_out["metas"][meta_key] = meta.json()
            else:
                logging.error(f"Entity {self} meta key {meta_key} not not instance of EntityMeta")
                continue
        return json_out

    def delete(self) -> bool:
        """Delete a model item and it's meta."""
        super(BaseEntityMeta, self).delete()
        sql = f"""
            DELETE FROM {self.table_name_meta}
            WHERE
                entity_id = %s AND
                entity_type = %s
            """
        self.cursor.execute(sql, (self.id, self.table_name))
        self.conn.commit()
        return True

    def get_meta(self, meta_name: str):
        """Get a meta key from an entity if it exists, or return None. """
        if meta_name not in self.metas:
            return False
        else:
            return self.metas[meta_name]

    def meta_update(self, meta_name: str, meta_value, meta_type: str = 'str') -> bool:
        """Set a models entity value if it currently exists or not."""
        if meta_name not in self.metas:
            self.metas[meta_name] = EntityMeta(self.conn, self.cursor)
            self.metas[meta_name].name = meta_name
            self.metas[meta_name].type = meta_type
        self.metas[meta_name].value = meta_value
        return True

    def load_meta(self, set_values: bool = True) -> dict:
        """Load the model's meta data. Setting the meta values to the instance if requested, and
        returning the meta values as a dict.
        """
        sql = f"""
            SELECT *
            FROM {self.table_name_meta}
            WHERE
                entity_id = %s AND
                entity_type = %s;
            """
        self.cursor.execute(sql, (self.id, self.table_name))
        meta_raws = self.cursor.fetchall()
        logging.debug(f"Loading meta data for {self}")
        metas = self._load_from_meta_raw(meta_raws)
        if set_values:
            metas.update(self.metas)
            self.metas = metas
        return metas

    def load_raw_meta(self) -> dict:
        """Load an entity's meta values and return them as EntityMeta objects in a dict, keyed by
        the EntityMeta's name.
        """
        sql = f"""
            SELECT *
            FROM {self.table_name_meta}
            WHERE
                entity_id = %s AND
                entity_type = %s;
            """
        self.cursor.execute(sql, (self.id, self.table_name))
        meta_raws = self.cursor.fetchall()
        return self._load_from_meta_raw(meta_raws)

    def _load_from_meta_raw(self, meta_raws: list) -> dict:
        """Load meta data from the database, returning it as a dictionary"""
        ret_metas = {}
        for meta_raw in meta_raws:
            em = EntityMeta(self.conn, self.cursor)
            em.build_from_list(meta_raw)
            ret_metas[em.name] = em
        return ret_metas
        # self.metas = ret_metas

    def _save_single_meta(self, existing_meta, meta_name: str, meta_value) -> bool:
        """Save a single meta field.
        :param existing_meta: An EntityMeta object if the meta record exists already, or False if
            it does not.
        """
        logging.debug("\n\nSaving Single Meta: meta_name")
        logging.debug(meta_name)
        if meta_name not in self.field_map_metas:
            logging.error(f"Model {self} does not allow meta key {meta_name}")
            return False
        if not existing_meta:
            logging.debug("Meta is NOT existing, lets create it")
            meta_desc = self.field_map_metas[meta_name]
            entity_meta = EntityMeta()
            entity_meta.entity_type = self.table_name
            entity_meta.entity_id = self.id
            entity_meta.name = meta_name
            entity_meta.type = meta_desc["type"]
            entity_meta.user_id = glow.user["user_id"]
            entity_meta.value = meta_value
            entity_meta.save()
        else:
            logging.debug("Meta is existing, lets update")
            entity_meta = existing_meta
            entity_meta.value = meta_value
            entity_meta.update()

        if entity_meta.save():
            return True
        else:
            logging.error("Error saving EntityMeta: %s" % entity_meta)
            return False


# End File: politeauthority/bookmarky-api/src/bookmarky/models/base_entity_meta.py
