# hammerspace/disk_drives.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class DiskDrivesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the DiskDrivesClient.
        """
        self.api_client = api_client
        logger.info("DiskDrivesClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all disk drives or a specific disk drive by its identifier.

        If 'identifier' is provided, fetches a single disk drive.
        (Corresponds to GET /disk-drives/{identifier} - OpId: getDiskDriveByIdentifier)
        Note: The GET /disk-drives/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all disk drives.
        (Corresponds to GET /disk-drives - OpId: listDiskDrives)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/disk-drives/{identifier}"
            logger.info(f"Getting disk drive by identifier: {identifier}")
            # No query parameters are defined for GET /disk-drives/{identifier} in the spec.
        else:
            path = "/disk-drives"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all disk drives with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: DiskDriveView or List[DiskDriveView]
