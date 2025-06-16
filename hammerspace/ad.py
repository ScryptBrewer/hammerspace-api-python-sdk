# hammerspace/ad.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class AdClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all AD configurations or a specific one by its identifier.

        If 'identifier' is provided, fetches a single AD configuration.
        (Corresponds to GET /ad/{identifier} - OpId: getAdByIdentifier)
        Optional kwargs for get by ID: include_discovery_info (bool)

        Otherwise, lists all AD configurations.
        (Corresponds to GET /ad - OpId: listAdConfiguration)
        Optional kwargs for listing: include_discovery_info (bool), spec (str),
                                     page (int), page_size (int), page_sort (str),
                                     page_sort_dir (str)
        """
        query_params = {}
        if "include_discovery_info" in kwargs: # Common for both list and get by ID
            query_params["includeDiscoveryInfo"] = str(kwargs["include_discovery_info"]).lower()

        if identifier:
            path = f"/ad/{identifier}"
            logger.info(f"Getting AD by identifier: {identifier} with params: {query_params}")
            # Note: The spec for GET /ad/{identifier} also has includeDiscoveryInfo
        else:
            path = "/ad"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing AD configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def discover_ad_realm_info_by_domain(self, domain: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get discovered realm information. (GET /ad/discover/{domain}) - OpId: discoverAdRealmInfoByDomain
        Optional kwargs: include_server_time (bool)
        """
        path = f"/ad/discover/{domain}"
        query_params = {}
        if "include_server_time" in kwargs:
            query_params["includeServerTime"] = str(kwargs["include_server_time"]).lower()
            
        logger.info(f"Discovering AD realm info for domain '{domain}' with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def flush_ad_cache(self, monitor_task: bool = True, task_timeout_seconds: int = 120) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Flush AD cache. (POST /ad/flush_cache) - OpId: flushAdCache"""
        path = "/ad/flush_cache"
        logger.info("Flushing AD cache.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self, identifier: str, ad_data: Dict[str, Any],
        monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Configure AD. (PUT /ad/{identifier}) - OpId: updateAdConfigurationByIdentifier
        ad_data corresponds to the SambaAdView schema.
        """
        path = f"/ad/{identifier}"
        logger.info(f"Updating AD configuration for identifier '{identifier}'. Body: {ad_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=ad_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
