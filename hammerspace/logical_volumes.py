# hammerspace/logical_volumes.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class LogicalVolumesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all logical volumes or a specific one by its identifier.

        If 'identifier' is provided, fetches a single logical volume.
        (Corresponds to GET /logical-volumes/{identifier} - OpId: getLogicalVolumeByIdentifier)

        Otherwise, lists all logical volumes.
        (Corresponds to GET /logical-volumes - OpId: listLogicalVolumes)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} 
        if identifier:
            path = f"/logical-volumes/{identifier}"
            logger.info(f"Getting logical volume by identifier: {identifier}")
        else:
            path = "/logical-volumes"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing logical volumes with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Create a logical volume. (POST /logical-volumes) - OpId: createLogicalVolume
        Optional kwargs for query parameters:
            node_name (str): (API name: nodeName)
            device_path (str): (API name: devicePath)
            force (bool): (API name: force)
        """
        path = "/logical-volumes"
        query_params = {}
        if "node_name" in kwargs: query_params["nodeName"] = kwargs["node_name"]
        if "device_path" in kwargs: query_params["devicePath"] = kwargs["device_path"]
        if "force" in kwargs: query_params["force"] = str(kwargs["force"]).lower()
        
        logger.info(f"Creating logical volume with query params: {query_params}")
        # This POST has query params, not a body in the spec.
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Delete logical volume by ID. (DELETE /logical-volumes/{identifier}) - OpId: deleteLogicalVolumeByIdentifier
        """
        path = f"/logical-volumes/{identifier}"
        logger.info(f"Deleting logical volume '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def discover(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Discover a logical volume. (GET /logical-volumes/{identifier}/discover) - OpId: discoverLogicalVolumeByIdentifier
        This is a GET, likely synchronous.
        """
        path = f"/logical-volumes/{identifier}/discover"
        logger.info(f"Discovering logical volume '{identifier}'.")
        # No query params defined in spec for this GET
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)
