# hammerspace/identity.py
import logging
from typing import Optional, Dict, Any
logger = logging.getLogger(__name__)

class IdentityClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(self, identifier: str) -> Optional[Dict[str, Any]]:
        # GET /identity/{identifier}
        # Operation ID: getIdentityByIdentifier
        path = f"/identity/{identifier}"
        logger.info(f"Getting identity for identifier '{identifier}'.")
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)
