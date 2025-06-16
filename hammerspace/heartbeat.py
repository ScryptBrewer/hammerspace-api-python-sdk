# hammerspace/heartbeat.py
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class HeartbeatClient:
    def __init__(self, api_client: Any):
        """
        Initializes the HeartbeatClient.
        """
        self.api_client = api_client
        logger.info("HeartbeatClient initialized using provided OpenAPI spec.")

    def get_heartbeat(self, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Gets the heartbeat status of the API.
        (Corresponds to GET /heartbeat - OpId: getHeartbeat)

        Args:
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this GET).

        Returns:
            A dictionary containing heartbeat information (HeartbeatView schema) or None on failure.
        """
        path = "/heartbeat"
        query_params = {} # No query parameters defined in spec for GET /heartbeat
        
        logger.info("Getting API heartbeat.")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: HeartbeatView

    