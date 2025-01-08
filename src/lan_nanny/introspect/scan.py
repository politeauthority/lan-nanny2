"""
    Lan Nanny
    Introspect
    Scan

    Run Scans for Lan Nanny

"""
import json

from lan_nanny.api.utils import db
from lan_nanny.api.utils.export import Export as ExportUtil


class Scan:
    def __init__(self):
        if not db.connect():
            print("Failed database connection, exiting")
            exit(1)
        self.export_data = {}
        self.user_id = 1

    def run(self):
        self.export_data = ExportUtil().run(self.user_id)
        self.create_export_file()

    def create_export_file(self) -> bool:
        """Create the export file."""
        export_data = json.dumps(self.export_data)
        export_file = open("export.json", "w")
        export_file.write(export_data)
        export_file.close()
        print("Successfully wrote export file")
        print("Bookmarks: %s" % len(self.export_data["bookmarks"]))
        print("Tags: %s" % len(self.export_data["tags"]))
        print("Dirs: %s" % len(self.export_data["directories"]))
        return True


if __name__ == "__main__":
    Scan().run()


# End File: politeauthority/lan-nanny/src/lan_nanny/introspect/scan.py
