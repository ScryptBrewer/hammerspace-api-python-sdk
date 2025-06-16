# hammerspace/object_storage_volumes.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class ObjectStorageVolumesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the ObjectStorageVolumesClient.
        This client manages logical object storage volumes, which are typically
        created on top of object storage targets.
        """
        self.api_client = api_client
        logger.info("ObjectStorageVolumesClient initialized.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all object storage volumes or a specific volume by its identifier.

        If 'identifier' is provided, fetches a single object storage volume.
        (Assumed OpId: getObjectStorageVolumeByIdentifier)

        Otherwise, lists all object storage volumes.
        (Assumed OpId: listObjectStorageVolumes)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/object-storage-volumes/{identifier}"
            logger.info(f"Getting object storage volume by identifier: {identifier}")
            # Assuming no specific query params for get by ID based on pattern
        else:
            path = "/object-storage-volumes"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all object storage volumes with query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        # Expected: ObjectStorageVolumeView or List[ObjectStorageVolumeView]
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self,
        volume_data: Dict[str, Any], # requestBody is ObjectStorageVolumeView (assumed)
        monitor_task: bool = True,   # Assuming 202 Accepted
        task_timeout_seconds: int = 600, # Volume creation can take time
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new object storage volume.
        (Assumed OpId: createObjectStorageVolume)
        Assumes a 202 Accepted response indicating an asynchronous task.

        Args:
            volume_data (Dict[str, Any]): Data for the new volume.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Optional query parameters (none assumed for create).

        Returns:
            Task ID or result if monitoring, or initial response. None on failure.
        """
        path = "/object-storage-volumes"
        query_params = {} # Process kwargs if any query params are defined for POST
        
        logger.info(f"Creating object storage volume with data: {volume_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=volume_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self,
        identifier: str,
        volume_data: Dict[str, Any], # requestBody is ObjectStorageVolumeView (assumed)
        monitor_task: bool = True,   # Assuming 202 Accepted
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing object storage volume by its identifier.
        (Assumed OpId: updateObjectStorageVolumeByIdentifier)
        Assumes a 202 Accepted response indicating an asynchronous task.

        Args:
            identifier (str): The identifier of the volume to update.
            volume_data (Dict[str, Any]): New data for the volume.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Optional query parameters (none assumed for update).

        Returns:
            Task ID or result if monitoring, or initial response. None on failure.
        """
        path = f"/object-storage-volumes/{identifier}"
        query_params = {} # Process kwargs if any query params are defined for PUT
        
        logger.info(f"Updating object storage volume '{identifier}' with data: {volume_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=volume_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self,
        identifier: str,
        monitor_task: bool = True,   # Assuming 202 Accepted
        task_timeout_seconds: int = 600, # Deletion can also take time
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes an object storage volume by its identifier.
        (Assumed OpId: deleteObjectStorageVolumeByIdentifier)
        Assumes a 202 Accepted response indicating an asynchronous task.

        Args:
            identifier (str): The identifier of the volume to delete.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Optional query parameters (none assumed for delete).

        Returns:
            Task ID or result if monitoring, or initial response. None on failure.
        """
        path = f"/object-storage-volumes/{identifier}"
        query_params = {} # Process kwargs if any query params are defined for DELETE
        
        logger.info(f"Deleting object storage volume '{identifier}'")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )