# hammerspace/object_store_logical_volumes.py
import logging
from typing import Optional, Dict, Any
logger = logging.getLogger(__name__)

class ObjectStoreLogicalVolumesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Get the shared information for a shared object storage volume by its UUID.
        (Corresponds to GET /object-store-logical-volumes/{identifier} - OpId: listObjectStoreLogicalVolumesByIdentifier)
        """
        # This endpoint is specifically for getting by ID, no "list all" variant.
        path = f"/object-store-logical-volumes/{identifier}"
        logger.info(f"Getting object store logical volume by identifier: {identifier}")
        # No query params defined in spec for this GET
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)

    def discover(self, identifier: str) -> Optional[Dict[str, Any]]: # Renamed from discover_object_store_logical_volume_by_identifier
        """
        Discover an object store logical volume (bucket).
        (Corresponds to GET /object-store-logical-volumes/{identifier}/discover - OpId: discoverObjectStorageVolumesByIdentifier)
        """
        path = f"/object-store-logical-volumes/{identifier}/discover"
        logger.info(f"Discovering object store logical volume: {identifier}")
        # No query params defined in spec for this GET
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)