# hammerspace/sw_update.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class SwUpdateClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client
        logger.info("SwUpdateClient initialized using provided OpenAPI spec.")

    def get_sw_update_status(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns SwUpdateStatusView
        """
        Get software update status.
        (Corresponds to GET /sw-update - OpId: getSwUpdateStatus)
        Optional kwargs:
            check_for_updates (bool): If true, check for available updates. (API name: checkForUpdates)
        """
        path = "/sw-update"
        query_params = {}
        if "check_for_updates" in kwargs:
            query_params["checkForUpdates"] = str(kwargs["check_for_updates"]).lower()
        logger.info(f"Getting software update status with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def download_sw_update(
        self, monitor_task: bool = True, task_timeout_seconds: int = 1800, **kwargs # Downloads can be long
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Default response {}
        """
        Download software update.
        (Corresponds to POST /sw-update/download - OpId: downloadSwUpdate)
        Optional kwargs:
            version (str): Version to download (if not latest).
        """
        path = "/sw-update/download"
        query_params = {}
        if "version" in kwargs: query_params["version"] = kwargs["version"]
        logger.info(f"Downloading software update with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def install_sw_update(
        self, monitor_task: bool = True, task_timeout_seconds: int = 3600, **kwargs # Installs can be very long
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Default response {}
        """
        Install software update.
        (Corresponds to POST /sw-update/install - OpId: installSwUpdate)
        Optional kwargs:
            skip_prechecks (bool): If true, skip pre-installation checks. (API name: skipPrechecks)
        """
        path = "/sw-update/install"
        query_params = {}
        if "skip_prechecks" in kwargs:
            query_params["skipPrechecks"] = str(kwargs["skip_prechecks"]).lower()
        logger.info(f"Installing software update with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )