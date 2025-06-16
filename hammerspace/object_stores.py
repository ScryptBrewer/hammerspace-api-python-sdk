# hammerspace/object_stores.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class ObjectStoresClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all internal object stores or a specific one by its identifier.

        If 'identifier' is provided, fetches a single internal object store.
        (Corresponds to GET /object-stores/{identifier} - OpId: getObjectStoresByIdentifier)

        Otherwise, lists all internal object stores.
        (Corresponds to GET /object-stores - OpId: listObjectStoreVolumes)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /object-stores/{id} has no query params in spec
        if identifier:
            path = f"/object-stores/{identifier}"
            logger.info(f"Getting internal object store by identifier: {identifier}")
        else:
            path = "/object-stores"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing internal object stores with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self, store_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Create an internal object store. (POST /object-stores) - OpId: createObjectStore
        store_data: The main request body (ObjectStoreView schema).
        Optional kwargs for query parameters:
            create_placement_objectives (bool): (API name: createPlacementObjectives)
        """
        path = "/object-stores"
        query_params = {}
        if "create_placement_objectives" in kwargs:
            query_params["createPlacementObjectives"] = str(kwargs["create_placement_objectives"]).lower()
        
        logger.info(f"Creating internal object store. Body: {store_data}, Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=store_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete an internal object store. (DELETE /object-stores/{identifier}) - OpId: deleteObjectStoresByIdentifier"""
        path = f"/object-stores/{identifier}"
        logger.info(f"Deleting internal object store '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
