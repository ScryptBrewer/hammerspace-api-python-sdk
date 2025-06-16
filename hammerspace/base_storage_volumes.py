# hammerspace/base_storage_volumes.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class BaseStorageVolumesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the BaseStorageVolumesClient.
        This client is used to get information about all types of storage volumes (File and Object).
        For specific operations on file storage volumes, see StorageVolumesClient.
        For specific operations on object storage volumes, see ObjectStorageVolumesClient.
        """
        self.api_client = api_client
        logger.info("BaseStorageVolumesClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all base storage volumes (File and Object) or a specific one by its identifier.

        If 'identifier' is provided, fetches a single base storage volume.
        (Corresponds to GET /base-storage-volumes/{identifier} - OpId: getBaseStorageVolumeByIdentifier)
        Note: The GET /base-storage-volumes/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all base storage volumes.
        (Corresponds to GET /base-storage-volumes - OpId: listBaseStorageVolumes)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        
        Returns:
            A list of BaseStorageVolumeView dictionaries or a single BaseStorageVolumeView dictionary,
            or None on failure.
        """
        query_params = {}
        if identifier:
            path = f"/base-storage-volumes/{identifier}"
            logger.info(f"Getting base storage volume by identifier: {identifier}")
            # No query parameters are defined for GET /base-storage-volumes/{identifier} in the spec.
        else:
            path = "/base-storage-volumes"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all base storage volumes with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: BaseStorageVolumeView or List[BaseStorageVolumeView]
