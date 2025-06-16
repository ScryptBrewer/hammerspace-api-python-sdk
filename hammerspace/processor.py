# hammerspace/processor.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class ProcessorClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs # No query params for list or get by ID in spec
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all processor services or a specific one by its identifier.

        If 'identifier' is provided, fetches a single processor service.
        (Corresponds to GET /processor/{identifier} - OpId: listProcessorByIdentifier)

        Otherwise, lists all processor services.
        (Corresponds to GET /processor - OpId: listProcessor)
        """
        query_params = {} # No query params defined in spec for these GETs
        if identifier:
            path = f"/processor/{identifier}"
            logger.info(f"Getting processor service by identifier: {identifier}")
        else:
            path = "/processor"
            logger.info(f"Listing all processor services.")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_processor(
        self, processor_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add a processor service. (POST /processor) - OpId: createProcessorByIdentifier (OpId seems mismatched)
        processor_data: The main request body (ProcessorView schema).
        Optional kwargs for query parameters:
            create_placement_objectives (bool): (API name: createPlacementObjectives)
        """
        path = "/processor"
        query_params = {}
        if "create_placement_objectives" in kwargs:
            query_params["createPlacementObjectives"] = str(kwargs["create_placement_objectives"]).lower()
        
        logger.info(f"Creating processor service. Body: {processor_data}, Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=processor_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update_processor(
        self, identifier: str, processor_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update a processor service. (PUT /processor/{identifier}) - OpId: updateProcessorByIdentifier"""
        path = f"/processor/{identifier}"
        logger.info(f"Updating processor service '{identifier}'. Body: {processor_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=processor_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_processor(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Remove a processor service. (DELETE /processor/{identifier}) - OpId: deleteProcessorByIdentifier"""
        path = f"/processor/{identifier}"
        logger.info(f"Deleting processor service '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
