# hammerspace/ntps.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class NtpsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all NTP configurations or a specific one by its identifier.

        If 'identifier' is provided, fetches a single NTP configuration.
        (Corresponds to GET /ntps/{identifier} - OpId: listNtpsByIdentifier)

        Otherwise, lists all NTP configurations.
        (Corresponds to GET /ntps - OpId: listNtps)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /ntps/{id} has no query params in spec
        if identifier:
            path = f"/ntps/{identifier}"
            logger.info(f"Getting NTP configuration by identifier: {identifier}")
        else:
            path = "/ntps"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing NTP configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def update( 
        self, identifier: str, ntp_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update NTP configuration. (PUT /ntps/{identifier}) - OpId: updateNtpsByIdentifier
        The OpenAPI spec does not show a POST /ntps for creation, so PUT is likely used for create/update.
        """
        path = f"/ntps/{identifier}"
        logger.info(f"Updating NTP configuration '{identifier}' with data: {ntp_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=ntp_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
