"""
    Lan Nanny - Client
    The Lan Nanny Api Python client, to help simplify api interactions run via Python

"""
import logging
import json
import os

from polite_lib.utils import xlate

from lan_nanny.api.version import version

import requests


class LanNannyClient:

    def __init__(self):
        self.api_url = os.environ.get("LAN_NANNY_API_URL")
        self.api_client_id = os.environ.get("LAN_NANNY_API_CLIENT_ID")
        self.api_key = os.environ.get("LAN_NANNY_API_KEY")
        self.token = None
        self.headers = {
            "Content-Type": "application/json",
            "Token": None,
            "User-Agent": "LanNannyClient/v%s" % version
        }

    def login(self) -> bool:
        """Logs into the Lan Nanny Api. Setting a self.token variable if successfull."""
        logging.info(f"Logging into to {self.api_url}")
        headers = {
            "X-Api-Key": self.api_key,
            "Client-Id": self.api_client_id,
            "Content-Type": "application/v%s" % version
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
        self.headers["Token"] = self.token
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

    def submit_host_scan(self, scan_meta: dict, scan_data: dict):
        """Submit a Host Scan the Lan Nanny Api.
        #@todo: This should probably be moved to somewhere more specific.
        """
        url = "/scan/submit-host"
        payload = {
            "meta": scan_meta,
            "scan": scan_data,
        }
        # logging.info("Making request to %s" % url)
        request = self.make_request(url, method="POST", payload=payload)
        # if request.status_code < 399:
        #     logging.error(request)
        # logging.debug("Successful request: %s" % url)
        return True

    def submit_port_scan(self, device_mac_id: str, scan_meta: dict, scan_data: dict):
        """Submit a Host Scan the Lan Nanny Api.
        #@todo: This should probably be moved to somewhere more specific.
        """
        url = "/scan/submit-port/%s" % device_mac_id
        payload = {
            "meta": scan_meta,
            "scan": scan_data,
        }
        request = self.make_request(url, method="POST", payload=payload)
        logging.info("Submit Port Scan Result: %s" % request)
        return True

    def get_port_scan_order(self):
        """Submit a Host Scan the Lan Nanny Api.
        #@todo: This should probably be moved to somewhere more specific.
        """
        url = "/scan/port-scan-order"
        request_data = self.make_request(url, method="GET")
        return request_data

    def get_options(self) -> dict:
        """Get all Options available to the current user, keyed by the Option.name."""
        url = "/options"
        request_data = self.make_request(url, method="GET")
        options = {}
        for opt in request_data["objects"]:
            options[opt["name"]] = opt
        return options

    def make_request(self, url: str, method: str = "GET", payload: dict = {}) -> dict:
        """Generic request maker to the Lan Nanny Api. Attempting to return a python dictionary."""

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

    def _handle_error(self, response, request_args) -> bool:
        url = request_args["url"]
        if "token" in request_args:
            request_args.pop("token")
        if "x-api-key" in request_args:
            request_args.pop("x-api-key")
        msg = f"\nISSUE WITH REQUEST: {response.status_code} - {url}\n"
        msg += "Api was sent:\n {request_args}\n"
        msg += "\tHeaders: \n\t %s " % request_args["headers"]
        # msg += f"Payload: \t{request_args["headers"]}\n"
        # msg += f"Payload: \n\5\n {request_args["headers"]}\n"

        msg += f"API Repsonsed: {response.text}\n"
        logging.error(msg)
        return False

    def _get_base_request_args(self, url: str, method: str) -> dict:
        """Get the base request args for requests on the Cver Api.
        :unit-test: TestClient::test___get_base_request_args
        """
        request_args = {
            "headers": self.headers,
            "method": method,
            "url": f"{self.api_url}/{url}"
        }
        request_args["headers"].update(self.headers)
        return request_args

# End File: politeauthority/lan-nanny/src/lan_nanny/client/__init__.py
