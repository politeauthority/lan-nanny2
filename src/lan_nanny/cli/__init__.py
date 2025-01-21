"""
 Lan Nanny - CLI

"""
from lan_nanny.api.version import version
from lan_nanny.client import LanNannyClient


class Cli:

    def __init__(self):
        self.api_client = LanNannyClient()
        self.options = {}

    def run(self):
        print("Starting Lan Nanny CLI: v%s" % version)
        self.who_am_i()
        self.options = self.api_client.get_options()

    def who_am_i(self):
        self.api_client.get_whoami()

if __name__ == "__main__":
    Cli().run()

# End File: politeauthority/lan-nanny/src/lan_nanny/cli/__init__.py
