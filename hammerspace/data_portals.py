# hammerspace/data_portals.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class DataPortalsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the DataPortalsClient.
        """
        self.api_client = api_client
        logger.info("DataPortalsClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all data portals or a specific data portal by its identifier.

        If 'identifier' is provided, fetches a single data portal.
        (Corresponds to GET /data-portals/{identifier} - OpId: getDataPortalByIdentifier)
        Note: The GET /data-portals/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all data portals.
        (Corresponds to GET /data-portals - OpId: listDataPortals)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/data-portals/{identifier}"
            logger.info(f"Getting data portal by identifier: {identifier}")
            # No query parameters are defined for GET /data-portals/{identifier} in the spec.
        else:
            path = "/data-portals"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all data portals with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: DataPortalView or List[DataPortalView]

    def create_data_portal(
        self,
        portal_data: Dict[str, Any], # requestBody is DataPortalView
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new data portal.
        (Corresponds to POST /data-portals - OpId: createDataPortal)
        The API spec indicates a 202 Accepted response.

        Args:
            portal_data (Dict[str, Any]): The data for the new data portal (DataPortalView schema).
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = "/data-portals"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Creating data portal with data: {portal_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=portal_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)

    def update_data_portal(
        self,
        identifier: str,
        portal_data: Dict[str, Any], # requestBody is DataPortalView
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing data portal by its identifier.
        (Corresponds to PUT /data-portals/{identifier} - OpId: updateDataPortalByIdentifier)
        The API spec indicates a 202 Accepted response.

        Args:
            identifier (str): The identifier of the data portal to update.
            portal_data (Dict[str, Any]): The new data for the portal (DataPortalView schema).
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = f"/data-portals/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating data portal '{identifier}' with data: {portal_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=portal_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)

    def delete_data_portal(
        self,
        identifier: str,
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a data portal by its identifier.
        (Corresponds to DELETE /data-portals/{identifier} - OpId: deleteDataPortalByIdentifier)
        The API spec indicates a 202 Accepted response.

        Args:
            identifier (str): The identifier of the data portal to delete.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = f"/data-portals/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        
        logger.info(f"Deleting data portal '{identifier}'")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)