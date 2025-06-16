# hammerspace/network_interfaces.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class NetworkInterfacesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all network interfaces or a specific one by its identifier.
        Also used for resolving by node and ifName via kwargs.

        If 'identifier' is provided, fetches a single network interface.
        (Corresponds to GET /network-interfaces/{identifier} - OpId: listNetworkInterfacesByIdentifier)

        If 'node' and 'if_name' are in kwargs, resolves a specific interface.
        (Corresponds to GET /network-interfaces/resolve - OpId: listNetworkInterfacesResolve)

        Otherwise, lists all network interfaces.
        (Corresponds to GET /network-interfaces - OpId: listNetworkInterfaces)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        Optional kwargs for resolving: node (str), if_name (str) (API names: node, ifName)
        """
        query_params = {}
        if identifier:
            path = f"/network-interfaces/{identifier}"
            logger.info(f"Getting network interface by identifier: {identifier}")
            # GET /network-interfaces/{id} has no query params in spec
        elif "node" in kwargs and "if_name" in kwargs:
            path = "/network-interfaces/resolve"
            query_params["node"] = kwargs["node"]
            query_params["ifName"] = kwargs["if_name"]
            logger.info(f"Resolving network interface by node '{kwargs['node']}' and ifName '{kwargs['if_name']}'")
        else:
            path = "/network-interfaces"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing network interfaces with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def update_network_interface( # Renamed from updateNetworkInterfaces
        self, identifier: str, interface_data: Dict[str, Any], # requestBody is BaseEntityView
        monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update network interface by ID. (PUT /network-interfaces/{identifier}) - OpId: updateNetworkInterfaces"""
        path = f"/network-interfaces/{identifier}"
        logger.info(f"Updating network interface '{identifier}' with data: {interface_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=interface_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def create_virtual_network_interface( # Renamed from createNetworkInterfaces
        self, identifier: str, # This is a path param, usually for the parent/host node
        interface_data: Dict[str, Any], # requestBody is NetworkInterfaceView
        monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create virtual network interface. (POST /network-interfaces/{identifier}) - OpId: createNetworkInterfaces"""
        path = f"/network-interfaces/{identifier}" # The {identifier} here is for the existing NI to add a VNI to? Or node? Check API logic.
        logger.info(f"Creating virtual network interface on '{identifier}' with data: {interface_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=interface_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_network_interface( # Renamed from deleteNetworkInterfaces
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete network interface by ID. (DELETE /network-interfaces/{identifier}) - OpId: deleteNetworkInterfaces"""
        path = f"/network-interfaces/{identifier}"
        logger.info(f"Deleting network interface '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )