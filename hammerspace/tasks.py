# hammerspace/tasks.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class TasksClient:
    def __init__(self, api_client: Any):
        """
        Initializes the TasksClient.
        """
        self.api_client = api_client
        logger.info("TasksClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all tasks or a specific task by its identifier.

        If 'identifier' is provided, fetches a single task.
        (Corresponds to GET /tasks/{identifier} - OpId: getTaskByIdentifier)
        Note: The GET /tasks/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all tasks.
        (Corresponds to GET /tasks - OpId: listTasks)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/tasks/{identifier}"
            logger.info(f"Getting task by identifier: {identifier}")
            # No query parameters are defined for GET /tasks/{identifier} in the spec.
        else:
            path = "/tasks"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all tasks with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: TaskView or List[TaskView]

    def cancel(
        self,
        identifier: str,
        monitor_task: bool = True, # Cancelling might involve an operation
        task_timeout_seconds: int = 120,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Default response is empty {}
        """
        Cancels a running task by its identifier.
        (Corresponds to POST /tasks/{identifier}/cancel - OpId: cancelTaskByIdentifier)

        Args:
            identifier (str): The identifier of the task to cancel.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            An empty dictionary if successful and not monitoring, or task ID/result if monitoring.
            None on failure.
        """
        path = f"/tasks/{identifier}/cancel"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /tasks/{id}/cancel supports them

        logger.info(f"Cancelling task '{identifier}'")
        # Even if spec says default response, cancellation might be an operation to monitor
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
