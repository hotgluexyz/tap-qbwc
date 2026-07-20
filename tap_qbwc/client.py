import requests
import backoff
import time
import xmlschema
from logging import Logger
from typing import Optional
from requests.exceptions import RequestException


class QBWCClient:
    """QBWC client class."""

    def __init__(self, config: dict, qbd_xml_schemas: xmlschema.XMLSchema, logger: Logger):
        self.logger = logger
        self.config = config
        self.session_id = None
        self.request_timeout = self.config["request_timeout"]
        self.qbwc_is_alive_timeout = self.config["qbwc_is_alive_timeout"]
        self.qbd_xml_schemas = qbd_xml_schemas
        self.base_url = "https://qbwc-qa.hotglue.xyz" if self.config.get("is_sandbox", False) else "https://qbwc.hotglue.com"
        self.total_estimated_records_count = 0
        self.total_processed_records_count = 0

    def create_session(self) -> None:
        """Get session id using the token."""
        self.logger.info("Creating QBWC client session")

        try:
            response = requests.post(
                f"{self.base_url}/authenticate",
                headers={"Authorization": f"Bearer {self.config['token']}"},
                timeout=30,
            )
        except Exception as e:
            raise Exception(f"Failed to authenticate: {e}") from e

        if response.status_code != 200:
            raise Exception(f"Failed to authenticate: {response.status_code} - {response.text}")

        self.session_id = response.json()["session_id"]
        self.logger.info(f"Created session id: {self.session_id}")

    def check_qbwc_is_alive(self) -> None:
        """Pings QBWC to check if it is alive."""
        self.logger.info("Pinging QBWC to check if it is alive")
        try:
            request_data = {"HostQueryRq": {}}
            response = self.make_request(request_data, self.qbwc_is_alive_timeout)
            host_query_data = response["HostQueryRs"][0]
            if host_query_data["@statusCode"] != 0:
                raise Exception(
                    f"{host_query_data.get('@statusCode')} - {host_query_data.get('@statusMessage')} - {host_query_data}"
                )
        except Exception as e:
            raise Exception(f"Failed pinging QBWC to check if it is alive: {e}") from e

    @backoff.on_exception(backoff.expo, RequestException, max_time=60)
    def _make_request(self, request_data: str, request_timeout: int) -> str:
        """Make a request to QBWC and returns the request_id that needs to be polled for the result."""
        payload = {
            "request_payload": request_data,
            "request_timeout": request_timeout,
            "total_processed_records_count": self.total_processed_records_count,
            "total_estimated_records_count": self.total_estimated_records_count,
        }

        if self.total_estimated_records_count > 0 and self.total_processed_records_count > 0:
            payload["completed_percentage"] = int(
                self.total_processed_records_count / self.total_estimated_records_count * 100
            )

        response = requests.post(
            f"{self.base_url}/send_qbwc_request",
            params={"session_id": self.session_id},
            json=payload,
            timeout=30,
        )

        if response.status_code == 429:
            raise RequestException(
                f"{response.status_code} - {response.text}",
                request=response.request,
                response=response,
            )
        if response.status_code != 200:
            raise Exception(f"Failed to make request: {response.status_code} - {response.text}")

        return response.json()["request_id"]

    @backoff.on_exception(backoff.expo, RequestException, max_time=60)
    def _make_poll_request(self, request_id: str) -> dict:
        """Poll the request for the result."""
        response = requests.get(
            f"{self.base_url}/get_qbwc_response",
            params={"session_id": self.session_id, "request_id": request_id},
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    def _poll_request(self, request_id: str, request_xml: str, request_timeout: int) -> dict:
        """Poll the request for the result."""

        while True:
            self.logger.info(f"Polling request {request_id} for the result")
            data = self._make_poll_request(request_id)
            if data["status"] == "completed":
                self.logger.info(f"Request {request_id} completed")
                return data["response_payload"]
            elif data["status"] == "error":
                raise Exception(
                    f"Request failed: {data.get('error_code')} - {data.get('error_message')} - Request XML: {request_xml}"
                )
            elif data["status"] == "timeout":
                raise Exception(
                    f"Request timed out after {request_timeout} seconds - Request XML: {request_xml}"
                )
            elif data["status"] in ["queued", "in_progress"]:
                self.logger.info(
                    f"Request {request_id} is '{data['status']}'. Retrying in 1 second..."
                )
                time.sleep(1)
            else:
                raise Exception(
                    f"Unknown response status: {data['status']} - Response: {data} - Request XML: {request_xml}"
                )

    def make_request(self, request_data: dict, request_timeout: Optional[int] = None) -> dict:
        """Make a request to QBWC."""
        if not self.session_id:
            raise Exception("Session ID not found. Please create a session first.")

        request_timeout = request_timeout or self.request_timeout
        request_xml = self.convert_request_data_to_xml(request_data)
        request_id = self._make_request(request_xml, request_timeout)
        response_xml = self._poll_request(request_id, request_xml, request_timeout)
        response_dict = self.convert_response_xml_to_dict(response_xml)
        return response_dict

    def convert_response_xml_to_dict(self, response_xml: str) -> dict:
        """Convert the response XML to a dictionary."""
        try:
            self.logger.info("Converting response XML to dictionary")
            response_dict = self.qbd_xml_schemas.decode(response_xml)
            return response_dict["QBXMLMsgsRs"]
        except xmlschema.XMLSchemaValidationError as e:
            raise Exception(f"Response XML to dictionary conversion failed: {e}") from e

    def convert_request_data_to_xml(self, request_data: dict) -> str:
        """Convert the request data to XML."""
        try:
            self.logger.info("Converting request data to XML")
            payload_dict = {
                "QBXMLMsgsRq": {
                    "@onError": "stopOnError",
                    **request_data,
                }
            }
            xml_element = self.qbd_xml_schemas.encode(payload_dict, path="QBXML", unordered=True)
            xml_string = xmlschema.etree_tostring(xml_element, encoding="utf-8")

            qbxml_header = '<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>\n'
            final_payload = f"{qbxml_header}\n{xml_string.decode('utf-8')}"

            self.logger.info("Successfully generated and validated qbXML payload")
            return final_payload
        except xmlschema.XMLSchemaValidationError as e:
            raise Exception(
                f"Dict mapping failed validation against XSD rules. Payload data: {payload_dict} - Error: {e}"
            ) from e
