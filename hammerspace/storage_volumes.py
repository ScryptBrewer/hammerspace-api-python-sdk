# hammerspace/storage_volumes.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class StorageVolumesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the StorageVolumesClient.
        Manages file storage volumes. For object storage volumes, see ObjectStorageVolumesClient.
        """
        self.api_client = api_client
        logger.info("StorageVolumesClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all file storage volumes or a specific one by its identifier.

        If 'identifier' is provided, fetches a single file storage volume.
        (Corresponds to GET /storage-volumes/{identifier} - OpId: listStorageVolumesByIdentifier)
        Note: This specific GET by ID endpoint has no query params in the spec.

        Otherwise, lists all file storage volumes.
        (Corresponds to GET /storage-volumes - OpId: listStorageVolumes)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/storage-volumes/{identifier}"
            logger.info(f"Getting file storage volume by identifier: {identifier}")
            # No query params defined for GET /storage-volumes/{identifier} in the spec
        else:
            path = "/storage-volumes"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing file storage volumes with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self,
        volume_data: Dict[str, Any],
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new file storage volume.
        (Corresponds to POST /storage-volumes - OpId: createStorageVolumes)

        Args:
            volume_data (Dict[str, Any]): Data for the new volume (StorageVolumeView schema).
            monitor_task (bool): Whether to monitor the task.
            task_timeout_seconds (int): Timeout for task monitoring.
        Optional kwargs for query parameters:
            create_placement_objectives (bool): When true, create default 'place-on' and 'exclude-from' objectives.
                                                (API name: createPlacementObjectives)
        """
        path = "/storage-volumes"
        query_params = {}
        if "create_placement_objectives" in kwargs:
            query_params["createPlacementObjectives"] = str(kwargs["create_placement_objectives"]).lower()
        
        logger.info(f"Creating file storage volume. Body: {volume_data}, Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=volume_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self,
        identifier: str,
        volume_data: Dict[str, Any],
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing file storage volume by its identifier.
        (Corresponds to PUT /storage-volumes/{identifier} - OpId: updateStorageVolumesByIdentifier)

        Args:
            identifier (str): The identifier of the volume to update.
            volume_data (Dict[str, Any]): New data for the volume (StorageVolumeView schema).
            monitor_task (bool): Whether to monitor the task.
            task_timeout_seconds (int): Timeout for task monitoring.
        Optional kwargs for query parameters:
            force (bool): Allows decommissioning a volume depended upon by a GFS. (API name: force)
        """
        path = f"/storage-volumes/{identifier}"
        query_params = {}
        if "force" in kwargs:
            query_params["force"] = str(kwargs["force"]).lower()
            
        logger.info(f"Updating file storage volume '{identifier}'. Body: {volume_data}, Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=volume_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self,
        identifier: str,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a file storage volume by its identifier.
        (Corresponds to DELETE /storage-volumes/{identifier} - OpId: deleteStorageVolumesByIdentifier)

        Args:
            identifier (str): The identifier of the volume to delete.
            monitor_task (bool): Whether to monitor the task.
            task_timeout_seconds (int): Timeout for task monitoring.
        Optional kwargs for query parameters:
            skip_gfs_validation (bool): Allows removing a volume depended upon by a GFS. (API name: skipGfsValidation)
            bypass_decommission (str): If "DataLossRiskAcknowledged", immediately removes volume.
                                       WARNING: Probable data loss. (API name: bypassDecommission)
        """
        path = f"/storage-volumes/{identifier}"
        query_params = {}
        if "skip_gfs_validation" in kwargs:
            query_params["skipGfsValidation"] = str(kwargs["skip_gfs_validation"]).lower()
        if "bypass_decommission" in kwargs:
            query_params["bypassDecommission"] = kwargs["bypass_decommission"]
            
        logger.info(f"Deleting file storage volume '{identifier}'. Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def decommission_storage_volume(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 600
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Decommissions a file storage volume.
        (Corresponds to POST /storage-volumes/{identifier}/decommission - OpId: decommissionStorageVolumesByIdentifier)
        """
        path = f"/storage-volumes/{identifier}/decommission"
        logger.info(f"Decommissioning file storage volume '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def discover_storage_volume(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 120
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Discovers a file storage volume.
        (Corresponds to POST /storage-volumes/{identifier}/discover - OpId: discoverStorageVolumesByIdentifier)
        """
        path = f"/storage-volumes/{identifier}/discover"
        logger.info(f"Discovering file storage volume '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def replace_storage_volume(
        self, identifier: str, locations_data: List[Dict[str, Any]],
        monitor_task: bool = True, task_timeout_seconds: int = 600
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Replaces a file storage volume.
        (Corresponds to POST /storage-volumes/{identifier}/replace - OpId: replaceStorageVolumesByIdentifier)
        Args:
            identifier (str): The identifier of the volume to replace.
            locations_data (List[Dict[str, Any]]): List of LocationView objects for replacement.
        """
        path = f"/storage-volumes/{identifier}/replace"
        logger.info(f"Replacing file storage volume '{identifier}' with locations: {locations_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=locations_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def get_related_storage_volumes(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Get all file storage volumes filtered by relation to another entity.
        (Corresponds to GET /storage-volumes/related-list - OpId: StorageVolumesByRelated)
        Optional kwargs:
            filter_uuid (str): (API name: filterUuid)
            filter_object_type (str): (API name: filterObjectType)
            sort (str): (API name: sort)
            terse (bool): (API name: terse)
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        path = "/storage-volumes/related-list"
        query_params = {}
        if "filter_uuid" in kwargs: query_params["filterUuid"] = kwargs["filter_uuid"]
        if "filter_object_type" in kwargs: query_params["filterObjectType"] = kwargs["filter_object_type"]
        if "sort" in kwargs: query_params["sort"] = kwargs["sort"]
        if "terse" in kwargs: query_params["terse"] = str(kwargs["terse"]).lower()
        if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
        if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        
        logger.info(f"Listing related file storage volumes with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)
