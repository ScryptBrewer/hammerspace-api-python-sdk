# hammerspace/snapshot_retentions.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class SnapshotRetentionsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the SnapshotRetentionsClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client
        logger.info("SnapshotRetentionsClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all snapshot retention policies or a specific one by its identifier.

        If 'identifier' is provided, fetches a single snapshot retention policy.
        (Corresponds to GET /snapshot-retentions/{identifier} - OpId: getSnapshotRetentionByIdentifier)
        Note: The GET /snapshot-retentions/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all snapshot retention policies.
        (Corresponds to GET /snapshot-retentions - OpId: listSnapshotRetentions)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/snapshot-retentions/{identifier}"
            logger.info(f"Getting snapshot retention policy by identifier: {identifier}")
            # No query parameters are defined for GET /snapshot-retentions/{identifier} in the spec.
        else:
            path = "/snapshot-retentions"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all snapshot retention policies with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: SnapshotRetentionView or List[SnapshotRetentionView]

    def create_snapshot_retention(
        self,
        retention_data: Dict[str, Any],
        monitor_task: bool = False, # Default to False as API spec shows 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new snapshot retention policy.
        (Corresponds to POST /snapshot-retentions - OpId: createSnapshotRetention)
        The API spec indicates a 200 OK response with the created object.
        If the operation can be long-running, set monitor_task=True.

        Args:
            retention_data (Dict[str, Any]): The data for the new snapshot retention policy (SnapshotRetentionView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created SnapshotRetentionView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/snapshot-retentions"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /snapshot-retentions supports them

        logger.info(f"Creating snapshot retention policy with data: {retention_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=retention_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=retention_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: SnapshotRetentionView

    def update(
        self,
        identifier: str,
        retention_data: Dict[str, Any],
        monitor_task: bool = False, # Default to False as API spec shows 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing snapshot retention policy by its identifier.
        (Corresponds to PUT /snapshot-retentions/{identifier} - OpId: updateSnapshotRetentionByIdentifier)
        The API spec indicates a 200 OK response with the updated object.
        If the operation can be long-running, set monitor_task=True.

        Args:
            identifier (str): The identifier of the snapshot retention policy to update.
            retention_data (Dict[str, Any]): The new data for the policy (SnapshotRetentionView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated SnapshotRetentionView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/snapshot-retentions/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        # Process any kwargs for query parameters if your API's PUT /snapshot-retentions/{id} supports them

        logger.info(f"Updating snapshot retention policy '{identifier}' with data: {retention_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=retention_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=retention_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: SnapshotRetentionView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Default to False as API spec shows 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a snapshot retention policy by its identifier.
        (Corresponds to DELETE /snapshot-retentions/{identifier} - OpId: deleteSnapshotRetentionByIdentifier)
        The API spec indicates a 200 OK response with the deleted object (or perhaps empty).
        If the operation can be long-running, set monitor_task=True.

        Args:
            identifier (str): The identifier of the snapshot retention policy to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted SnapshotRetentionView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/snapshot-retentions/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        # Process any kwargs for query parameters if your API's DELETE /snapshot-retentions/{id} supports them

        logger.info(f"Deleting snapshot retention policy '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            # The spec says 200 OK with SnapshotRetentionView, which is unusual for DELETE.
            # Often DELETE returns 204 No Content or 200 with a simple confirmation.
            # Parsing as JSON based on spec.
            return self.api_client.read_and_parse_json_body(response)
