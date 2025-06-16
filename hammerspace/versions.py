# hammerspace/versions.py
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class VersionsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the VersionsClient.
        """
        self.api_client = api_client
        logger.info("VersionsClient initialized using provided OpenAPI spec.")

    def get_versions(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns VersionView
        """
        Get version information.
        (Corresponds to GET /versions - OpId: getVersions)
        The provided spec does not list any query parameters for this endpoint.
        **kwargs are included for future-proofing or if the full spec differs.

        Args:
            **kwargs: Optional keyword arguments for query parameters.

        Returns:
            A dictionary containing version information (VersionView schema) or None on failure.
        """
        path = "/versions"
        query_params = {}
        # Process any kwargs for query parameters if your API's GET /versions supports them
        # Example: if "component" in kwargs: query_params["component"] = kwargs["component"]
        
        logger.info(f"Getting version information with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)