# hammerspace/nodes.py
import logging
from typing import Optional, List, Dict, Any
# from .client import HammerspaceApiClient

logger = logging.getLogger(__name__)

class NodesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list_nodes(
        self,
        spec: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        page_sort: Optional[str] = None,
        page_sort_dir: Optional[str] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all nodes. (GET /nodes) - Operation ID: listNodes"""
        path = "/nodes"
        query_params = {}
        if spec is not None: query_params["spec"] = spec
        if page is not None: query_params["page"] = page
        if page_size is not None: query_params["page.size"] = page_size
        if page_sort is not None: query_params["page.sort"] = page_sort
        if page_sort_dir is not None: query_params["page.sort.dir"] = page_sort_dir
        
        logger.info(f"Listing nodes with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_node(
        self, node_data: Dict[str, Any], create_placement_objectives: Optional[bool] = None, task_timeout_seconds: int = 300
    ) -> Optional[str]:
        """Create node. (POST /nodes) - Operation ID: createNodes. Returns 202 Accepted."""
        path = "/nodes"
        query_params = {}
        if create_placement_objectives is not None:
            query_params["createPlacementObjectives"] = str(create_placement_objectives).lower()
        
        logger.info(f"Creating node with data: {node_data}, params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            initial_json_data=node_data,
            initial_query_params=query_params,
            task_timeout_seconds=task_timeout_seconds
        )

    def list_related_nodes(
        self,
        filter_uuid: Optional[str] = None,
        filter_object_type: Optional[str] = None,
        sort: Optional[str] = None,
        terse: Optional[bool] = None,
        spec: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        page_sort: Optional[str] = None, # Note: 'sort' and 'page.sort' are different
        page_sort_dir: Optional[str] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all nodes filtered by relation to other entity. (GET /nodes/related-list) - Operation ID: ListrelatedNodes"""
        path = "/nodes/related-list"
        query_params = {}
        if filter_uuid is not None: query_params["filterUuid"] = filter_uuid
        if filter_object_type is not None: query_params["filterObjectType"] = filter_object_type
        if sort is not None: query_params["sort"] = sort
        if terse is not None: query_params["terse"] = str(terse).lower()
        if spec is not None: query_params["spec"] = spec
        if page is not None: query_params["page"] = page
        if page_size is not None: query_params["page.size"] = page_size
        if page_sort is not None: query_params["page.sort"] = page_sort
        if page_sort_dir is not None: query_params["page.sort.dir"] = page_sort_dir

        logger.info(f"Listing related nodes with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def list_unauthenticated_nodes(self) -> Optional[List[Dict[str, Any]]]:
        """Get unauthenticated nodes. (GET /nodes/unauthenticated) - Operation ID: listUnauthenticatedNodes"""
        path = "/nodes/unauthenticated"
        logger.info("Listing unauthenticated nodes.")
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)

    def get(self, identifier: str, block_device_info: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        """Get node by ID. (GET /nodes/{identifier}) - Operation ID: listNodesByIdentifier"""
        path = f"/nodes/{identifier}"
        query_params = {}
        if block_device_info is not None:
            query_params["blockDeviceInfo"] = str(block_device_info).lower()
        
        logger.info(f"Getting node by ID: {identifier} with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def update(
        self, identifier: str, node_data: Dict[str, Any], skip_object_volume_validations: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]: # Assuming 200 OK response with updated node data
        """Update node. (PUT /nodes/{identifier}) - Operation ID: updateNodesByIdentifierr"""
        path = f"/nodes/{identifier}"
        query_params = {}
        if skip_object_volume_validations is not None:
            query_params["skipObjectVolumeValidations"] = str(skip_object_volume_validations).lower()
            
        logger.info(f"Updating node ID: {identifier} with data: {node_data}, params: {query_params}")
        response = self.api_client.make_rest_call(
            path=path, method="PUT", json_data=node_data, query_params=query_params
        )
        return self.api_client.read_and_parse_json_body(response) # Or monitor if it becomes async

    def delete(self, identifier: str, force: Optional[bool] = None, task_timeout_seconds: int = 300) -> Optional[str]:
        """Delete node. (DELETE /nodes/{identifier}) - Operation ID: deleteNodesByidentifier. Returns 202 Accepted."""
        path = f"/nodes/{identifier}"
        query_params = {}
        if force is not None:
            query_params["force"] = str(force).lower()
            
        logger.info(f"Deleting node ID: {identifier} with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="DELETE",
            initial_query_params=query_params,
            task_timeout_seconds=task_timeout_seconds
        )

    def refresh(
        self, identifier: str, rescan: Optional[bool] = None, reconcile_components: Optional[bool] = None, task_timeout_seconds: int = 300
    ) -> Optional[str]:
        """Refresh node. (POST /nodes/{identifier}/refresh) - Operation ID: refreshNodesByidentifier. Returns 202 Accepted."""
        path = f"/nodes/{identifier}/refresh"
        query_params = {}
        if rescan is not None: query_params["rescan"] = str(rescan).lower()
        if reconcile_components is not None: query_params["reconcileComponents"] = str(reconcile_components).lower()
        
        logger.info(f"Refreshing node ID: {identifier} with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST", # POST for actions
            initial_query_params=query_params,
            task_timeout_seconds=task_timeout_seconds
        )

    def set_node_mode(self, identifier: str, mode: str) -> Optional[Dict[str, Any]]:
        """Change node mode. (POST /nodes/{identifier}/set-mode/{mode}) - Operation ID: updateNodesByidentifier (note: duplicated opId)"""
        path = f"/nodes/{identifier}/set-mode/{mode}"
        logger.info(f"Setting mode for node ID: {identifier} to mode: {mode}")
        response = self.api_client.make_rest_call(path=path, method="POST")
        return self.api_client.read_and_parse_json_body(response)
