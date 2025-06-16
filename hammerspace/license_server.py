# hammerspace/license_server.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class LicenseServerClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get_metered_licenses( 
        self, **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get all metered licenses from the license server.
        (Corresponds to GET /license-server - OpId: listMeteredLicenses)

        Optional kwargs:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        path = "/license-server"
        query_params = {}
        if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
        if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        
        logger.info(f"Listing metered licenses with effective query params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def report_license_server_usage_by_uuid(
        self, uuid: str, usage_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 120
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Report license usage. (PUT /license-server/report-usage/{uuid}) - OpId: reportLicenseServerUsageByUuid"""
        path = f"/license-server/report-usage/{uuid}"
        logger.info(f"Reporting license server usage for UUID '{uuid}'. Body: {usage_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=usage_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )