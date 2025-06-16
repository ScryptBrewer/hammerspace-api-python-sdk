# hammerspace/antivirus.py
import logging
from typing import Optional, List, Dict, Any, Union
# from .client import HammerspaceApiClient

logger = logging.getLogger(__name__)

class AntivirusClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list_antivirus_services(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all antivirus services. (GET /antivirus)
        Operation ID: listAntivirusServices
        """
        path = "/antivirus"
        logger.info("Listing antivirus services.")
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)

    def create_antivirus_service(
        self,
        antivirus_data: Dict[str, Any],
        create_placement_objectives: Optional[bool] = None,
        monitor_task: bool = True, # Assuming create might be async
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add an antivirus service. (POST /antivirus)
        Operation ID: createAntivirusService
        """
        path = "/antivirus"
        query_params = {}
        if create_placement_objectives is not None:
            query_params["createPlacementObjectives"] = str(create_placement_objectives).lower()
        
        logger.info(f"Creating antivirus service with params: {query_params}")
        # The OpenAPI spec shows 200 for this POST, but create operations can often be async (202)
        # Using execute_and_monitor_task to handle both possibilities if monitor_task is True
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            initial_json_data=antivirus_data,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def get(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Get an antivirus service by identifier. (GET /antivirus/{identifier})
        Operation ID: getAntivirusServiceByIdentifier
        """
        path = f"/antivirus/{identifier}"
        logger.info(f"Getting antivirus service by identifier '{identifier}'.")
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)

    def update(
        self,
        identifier: str,
        antivirus_data: Dict[str, Any],
        monitor_task: bool = True, 
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update an antivirus service. (PUT /antivirus/{identifier})
        Operation ID: updateAntivirusServiceByIdentifier
        """
        path = f"/antivirus/{identifier}"
        logger.info(f"Updating antivirus service '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="PUT",
            initial_json_data=antivirus_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self,
        identifier: str,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Remove an antivirus service. (DELETE /antivirus/{identifier})
        Operation ID: deleteAntivirusServiceByIdentifier
        """
        path = f"/antivirus/{identifier}"
        logger.info(f"Deleting antivirus service '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )
