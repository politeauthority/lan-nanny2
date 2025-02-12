"""
    Lan Nanny Migrate
    Data - Rbac

"""
import logging

from lan_nanny.api.utils import db
from lan_nanny.api.models.role import Role
from lan_nanny.api.models.role_perm import RolePerm
from lan_nanny.api.models.perm import Perm


class DataRbac:

    def create(self):
        db.connect()
        admin_role_id = self.create_admin_rbac()
        reader_role_id = self.create_reader_rbac()
        contributor_role_id = self.create_contributor_rbac()
        ingestor_role_id = self.create_ingestor_rbac()
        engineer_role_id = self.create_engineer_rbac()

        return {
            "admin_role_id": admin_role_id,
            "reader_role_id": reader_role_id,
            "contributor_role_id": contributor_role_id,
            "ingestor_role_id": ingestor_role_id,
            "engineer_role_id": engineer_role_id
        }

    def create_admin_rbac(self) -> int:
        """Create admin level rbac with read/write all."""
        # Create Role
        role = self.create_role("Admin", "admin")

        # Create the Perms
        perm_write_all = self.create_perm("Write All", "write-all")
        perm_read_all = self.create_perm("Read All", "read-all")
        perm_delete_all = self.create_perm("Delete All", "delete-all")

        # Create RolePerms
        self.create_role_perm(role, perm_write_all)
        self.create_role_perm(role, perm_read_all)
        self.create_role_perm(role, perm_delete_all)
        return role.id

    def create_reader_rbac(self) -> int:
        """Create reader level rbac with read all."""
        # Create Role
        role = self.create_role("Reader", "reader")

        # Create the Perms
        perm_read_all = self.create_perm("Read All", "read-all")

        # Create RolePerms
        self.create_role_perm(role, perm_read_all)
        return role.id

    def create_contributor_rbac(self) -> int:
        """Create cotnributor level rbac with limited read-write"""
        # Create Role
        role = self.create_role("Contributor", "contributor")

        # Create the Perms and Bindings
        perm_read_info = self.create_perm("Read Info", "read-info")
        self.create_role_perm(role, perm_read_info)

        perm_read_image = self.create_perm("Read Image", "read-image")
        self.create_role_perm(role, perm_read_image)

        perm_read_image = self.create_perm("Read Image", "write-image")
        self.create_role_perm(role, perm_read_image)

        return role.id

    def create_ingestor_rbac(self) -> int:
        """Create ingestor role with write scan and read info."""
        # Create Role
        role = self.create_role("Ingestor", "ingestor")

        # Create the Perms and Bindings
        perm_write_scan_info = self.create_perm("Write Scan", "write-ingest")
        self.create_role_perm(role, perm_write_scan_info)

        perm_read_info = self.create_perm("Read Info", "read-info")
        self.create_role_perm(role, perm_read_info)

        return role.id

    def create_engineer_rbac(self) -> int:
        """Create engineer role with write and read all.
        @todo: This role needs to have permissions cutback.
        """
        # Create Role
        role = self.create_role("Engineer", "engineer")

        # Create the Perms and Bindings
        perm_write_scan_info = self.create_perm("Write Scan", "write-ingest")
        self.create_role_perm(role, perm_write_scan_info)

        perm_read_all = self.create_perm("Read All", "read-all")
        self.create_role_perm(role, perm_read_all)

        perm_write_all = self.create_perm("Write All", "write-all")
        self.create_role_perm(role, perm_write_all)

        return role.id

    def create_engine_rbac(self) -> int:
        """Create ingestor role with write scan and read info."""
        # Create Role
        role = self.create_role("Engine", "engine")

        # Create the Perms and Bindings
        perm_write_scan_info = self.create_perm("Write Scan", "write-scan")
        self.create_role_perm(role, perm_write_scan_info)

        perm_read_info = self.create_perm("Read Info", "read-info")
        self.create_role_perm(role, perm_read_info)

        return role.id

    def create_role(self, role_name: str, role_slug_name: str) -> Role:
        """Create the admin role with read/write all, if it doesn't exist."""
        role = Role()
        if role.get_by_field("slug_name", role_slug_name):
            logging.info("%s role exists, not creating" % role_name)
            return role
        role = Role()
        role.name = role_name
        role.slug_name = role_slug_name
        role.save()
        logging.info("Created Role: %s" % role)
        return role

    def create_perm(self, perm_name: str, perm_slug: str) -> int:
        """Generic Perm creator. Will check if the Perm slug-name already exsits before creating."""
        perm = Perm()
        if perm.get_by_field("slug_name", perm_slug):
            logging.debug('Perm: "%s" exists, not creating' % perm_name)
            return perm
        perm.name = perm_name
        perm.slug_name = perm_slug
        perm.save()
        logging.info("Created Perm: %s" % perm)
        return perm

    def create_role_perm(self, role, perm):
        "Generic RolePerm creator. Will check if the binding exists, if not it will creating it."
        role_perm = RolePerm()
        if role_perm.get_by_role_perm(role.id, perm.id):
            logging.debug("RolePerm for %s %s exists, not creating" % (role, perm))
            return True
        role_perm.role_id = role.id
        role_perm.perm_id = perm.id
        role_perm.save()
        logging.info("Created Role Perm: %s for %s - %s" % (role_perm, role, perm))


# End File: politeauthority/lan-nanny/src/lan_nanny/migrate/data/data_rbac.py
