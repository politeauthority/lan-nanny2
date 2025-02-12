"""
    Bookmarky Api
    Collects - Users

"""
from lan_nanny.api.collects.base import Base
from lan_nanny.api.models.user import User


class Users(Base):
    """Collection class for gathering a group of Users."""

    collection_name = "users"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Users, self).__init__(conn, cursor)
        self.table_name = User().table_name
        self.collect_model = User
        self.field_map = self.collect_model().field_map

    def get_admins(self) -> list:
        """Get admin users."""
        sql = """
            SELECT *
            FROM `%(table)s`
            WHERE `role_id`=%(admin_role)s;
        """ % {
            "table": self.table_name,
            "admin_role": 1,
        }
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        users = self.build_from_lists(raws)
        return users

# End File: bookmarky/src/bookmarky/api/collects/users.py
