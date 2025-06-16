# hammerspace/volume_groups.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class VolumeGroupsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the VolumeGroupsClient.
        """
        self.api_client = api_client
        logger.info("VolumeGroupsClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all volume groups or a specific volume group by its identifier.

        If 'identifier' is provided, fetches a single volume group.
        (Corresponds to GET /volume-groups/{identifier} - OpId: getVolumeGroupByIdentifier)
        Note: The GET /volume-groups/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all volume groups.
        (Corresponds to GET /volume-groups - OpId: listVolumeGroups)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/volume-groups/{identifier}"
            logger.info(f"Getting volume group by identifier: {identifier}")
            # No query parameters are defined for GET /volume-groups/{identifier} in the spec.
        else:
            path = "/volume-groups"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all volume groups with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: VolumeGroupView or List[VolumeGroupView]

    def create(
        self,
        group_data: Dict[str, Any], # requestBody is VolumeGroupView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new volume group.
        (Corresponds to POST /volume-groups - OpId: createVolumeGroup)
        The API spec indicates a 200 OK response with the created VolumeGroupView object.

        Args:
            group_data (Dict[str, Any]): The data for the new volume group (VolumeGroupView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created VolumeGroupView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/volume-groups"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /volume-groups supports them

        logger.info(f"Creating volume group with data: {group_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=group_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=group_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: VolumeGroupView

    def update(
        self,
        identifier: str,
        group_data: Dict[str, Any], # requestBody is VolumeGroupView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing volume group by its identifier.
        (Corresponds to PUT /volume-groups/{identifier} - OpId: updateVolumeGroupByIdentifier)
        The API spec indicates a 200 OK response with the updated VolumeGroupView object.

        Args:
            identifier (str): The identifier of the volume group to update.
            group_data (Dict[str, Any]): The new data for the group (VolumeGroupView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated VolumeGroupView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/volume-groups/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        # Process any kwargs for query parameters if your API's PUT /volume-groups/{id} supports them

        logger.info(f"Updating volume group '{identifier}' with data: {group_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=group_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=group_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: VolumeGroupView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a volume group by its identifier.
        (Corresponds to DELETE /volume-groups/{identifier} - OpId: deleteVolumeGroupByIdentifier)
        The API spec indicates a 200 OK response with the deleted VolumeGroupView object.

        Args:
            identifier (str): The identifier of the volume group to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted VolumeGroupView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/volume-groups/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        # Process any kwargs for query parameters if your API's DELETE /volume-groups/{id} supports them

        logger.info(f"Deleting volume group '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: VolumeGroupView
