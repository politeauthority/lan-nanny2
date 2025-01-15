"""
    Lan Nanny - Client
    The Lan Nanny Api Python client, to help simplify api interactions run via Python

"""
import logging
import json
import os

from polite_lib.utils import xlate

import requests


class LanNannyClient:

    def __init__(self):
        self.api_url = os.environ.get("LAN_NANNY_API_URL")
        self.api_client_id = os.environ.get("LAN_NANNY_API_CLIENT_ID")
        self.api_key = os.environ.get("LAN_NANNY_API_KEY")
        self.token = None

    def login(self) -> bool:
        """Logs into the Lan Nanny Api. Setting a self.token variable if successfull."""
        logging.info(f"Logging into to {self.api_url}")
        headers = {
            "X-Api-Key": self.api_key,
            "Client-Id": self.api_client_id,
            "Content-Type": "application/json"
        }
        if not self._validate_login_request(headers):
            return False
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

    def _validate_login_request(self, headers: dict) -> bool:
        """Validate that we have the correct headers for an authentication request."""
        if "X-Api-Key" not in headers:
            logging.critical("Missing Lan Nanny Api Key!")
            return False
        if "Client-Id" not in headers:
            logging.critical("Missing Lan Nanny Client ID!")
            return False
        return True

    def make_request(self, url: str, method: str = "GET", payload: dict = {}):
        if not self.token:
            if not self.login():
                return False
        request_args = self._get_base_request_args(url, method)
        if request_args:
            if method == "GET":
                apply_query_field = False
                if isinstance(payload, dict) and "query" in payload:
                    apply_query_field = True
                if apply_query_field:
                    request_args["url"] += "?query=" + xlate.url_encode_json(
                        "%s" % payload["query"])
                else:
                    request_args["params"] = payload

            elif method == "POST":
                request_args["data"] = json.dumps(payload)
                if "id" in payload:
                    request_args["url"] += "/%s" % payload["id"]
                    payload.pop("id")
        request_args["verify"] = False     # @todo fix
        # debug
        logging.info("\n\n%s - %s\n%s" % (
            request_args["method"],
            request_args["url"],
            request_args))

        response = requests.request(**request_args)

        # If our token has expired, attempt to get a new one, skipping using the current one.
        if response.status_code in [412, 401]:
            self.destroy_token()
            # @todo we need to retry here

        if response.status_code > 399:
            if response.status_code == 404:
                logging.debug(f"Got 404: {response.url}")
            else:
                self._handle_error(response, request_args)
                return {}

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            logging.error("Could not get json from response.\n%s" % response.text)
            return False
        self.response_last = response
        self.response_last_json = response_json
        return response_json

    def _validate_request(self, headers: dict) -> bool:
        """Validate that we have the correct headers for an authentication request."""
        if "Token" not in headers:
            logging.critical("Missing Lan Nanny Api Key!")
            return False
        return True

    def _get_base_request_args(self, url: str, method: str) -> dict:
        """Get the base request args for requests on the Cver Api.
        :unit-test: TestClient::test___get_base_request_args
        """
        request_args = {
            "headers": {
                "token": self.token,
                "content-type": "application/json",
            },
            "method": method,
            "url": f"{self.api_url}/{url}"
        }
        request_args["headers"].update(self.headers)
        return request_args

# End File: politeauthority/lan-nanny/src/lan_nanny/client/__init__.py
