# hammerspace/system_info.py
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SystemInfoClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client
        logger.info("SystemInfoClient initialized using provided OpenAPI spec.")

    def get_system_info(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns SystemInfoView
        """
        Get system info.
        (Corresponds to GET /system-info - OpId: getSystemInfo)
        Optional kwargs:
            key (List[str]): Keys to include in the response. (API name: key, array)
        """
        path = "/system-info"
        query_params = {}
        if "key" in kwargs:
            query_params["key"] = kwargs["key"] # List of strings
        logger.info(f"Getting system info with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)