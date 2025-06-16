# hammerspace/system.py
import logging
from typing import Optional, Dict, Any, Union

logger = logging.getLogger(__name__)

class SystemClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client
        logger.info("SystemClient initialized using provided OpenAPI spec.")

    def get_system_settings(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns SystemView
        """
        Get system settings.
        (Corresponds to GET /system - OpId: getSystemSettings)
        Optional kwargs:
            with_unclear_event_severity (List[str]): Augment response with unclearedEvents.
                                                      (API name: withUnclearedEventSeverity, array)
        """
        path = "/system"
        query_params = {}
        if "with_unclear_event_severity" in kwargs:
            query_params["withUnclearedEventSeverity"] = kwargs["with_unclear_event_severity"]
        logger.info(f"Getting system settings with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def update_system_settings(
        self,
        system_data: Dict[str, Any], # requestBody is SystemView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update system settings.
        (Corresponds to PUT /system - OpId: updateSystemSettings)
        """
        path = "/system"
        query_params = {} # No query params for PUT in spec
        logger.info(f"Updating system settings with data: {system_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=system_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=path, method="PUT", json_data=system_data, query_params=query_params)
            return self.api_client.read_and_parse_json_body(response) # Returns SystemView