# hammerspace/data_copy_to_object.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class DataCopyToObjectClient:
    def __init__(self, api_client: Any):
        """
        Initializes the DataCopyToObjectClient.
        """
        self.api_client = api_client
        logger.info("DataCopyToObjectClient initialized using provided OpenAPI spec.")

    def start_data_copy_to_object_task(
        self,
        object_node_data: Dict[str, Any], # requestBody is NodeView (for specifying the object store node)
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 7200, # Data copy can be very long
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Starts a data copy to object task.
        (Corresponds to POST /data-copy-to-object - OpId: createDataCopyToObjectTask)
        The API spec indicates a 202 Accepted response.

        Args:
            object_node_data (Dict[str, Any]): Data identifying the object storage node (NodeView schema).
                                               This is passed in the request body.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        
        Required kwargs (as query parameters):
            bucket (str): The target object storage bucket name.
            share (str): The source share name or UUID.
            source_path (str): The path within the source share to copy from.
            dest_path (str): The destination path within the object bucket (optional, can be root).

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = "/data-copy-to-object"
        query_params = {}

        required_query_params = ["bucket", "share", "source_path"]
        for param in required_query_params:
            if param not in kwargs:
                raise ValueError(f"Missing required query parameter: '{param}' for start_data_copy_to_object_task")
            query_params[param] = kwargs[param]
        
        if "dest_path" in kwargs: # Optional destination path
            query_params["destPath"] = kwargs["dest_path"]
        
        logger.info(f"Starting data copy to object task. Query Params: {query_params}, Object Node Data: {object_node_data}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            initial_json_data=object_node_data, # NodeView in body
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)

    def list_object_storage_buckets(
        self,
        object_node_data: Dict[str, Any], # requestBody is NodeView
        monitor_task: bool = False, # Spec says 200 OK with List[str]
        task_timeout_seconds: int = 120
    ) -> Union[Optional[str], Optional[List[str]]]:
        """
        Returns a listing of buckets from the specified object storage node.
        (Corresponds to POST /data-copy-to-object/list-buckets - OpId: listDataCopyToObjectBuckets)
        The API spec indicates a 200 OK response with a list of bucket names.

        Args:
            object_node_data (Dict[str, Any]): Data identifying the object storage node (NodeView schema).
                                               This is passed in the request body.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
                                 (Unlikely for a list operation, but kept for consistency).
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.

        Returns:
            A list of bucket name strings if successful and not monitoring,
            or task ID/result if monitoring (though direct result is more likely). None on failure.
        """
        path = "/data-copy-to-object/list-buckets"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Listing object storage buckets for object node: {object_node_data}")
        if monitor_task:
            # It's unusual for a list operation to be a task, but we'll support the pattern
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=object_node_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=object_node_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: List[str]
