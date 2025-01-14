"""
    Lan Nanny - Client
    The Lan Nanny Api Python client, to help simplify api interactions run via Python

"""
import logging
import os

import requests


class LanNannyClient:

    def __init__(self):
        self.api_url = os.environ.get("LAN_NANNY_API_URL")
        self.api_client_id = os.environ.get("LAN_NANNY_CLIENT_ID")
        self.api_key = os.environ.get("LAN_NANNY_CLIENT_ID")

    def api_login(self) -> bool:
        """Logs into the Lan Nanny Api. Setting a self.token variable if successfull."""
        logging.info(f"Logging into to {self.api_url}")
        headers = {
            "X-Api-Key": self.api_key,
            "Client-Id": self.api_client_id,
            "Content-Type": "application/json"
        }
        url = self.api_url + "/auth"
        request = requests.post(url, headers=headers)
        if request.status_code != 200:
            logging.critical(
                f"Could not connect to api: {self.api_url} got code: {request.status_code}")
            logging.critical("Exiting")
            exit(1)
        response_json = request.json()
        self.token = response_json["token"]
        logging.info("Successfully got token from Lan Nanny Api")
        return True


# End File: politeauthority/lan-nanny/src/lan_nanny/client/lan_nanny_client.py
