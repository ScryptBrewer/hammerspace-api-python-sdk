"""Spec-generated client for the "object-store-logical-volumes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedObjectStoreLogicalVolumesClient:
    """Typed coverage for all 2 "object-store-logical-volumes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStoreLogicalVolume], gen.ObjectStoreLogicalVolume, Any]:
        'Get the shared information for a shared object storage volume by the UUID which is in the hs_osv_details file in the OSVs bucket'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/object-store-logical-volumes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ObjectStoreLogicalVolume, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectStoreLogicalVolume, raw=raw)

    def discover(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectVolumeDiscoveryInfoView], gen.ObjectVolumeDiscoveryInfoView, Any]:
        'Discover an object store logical volume (bucket)'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/object-store-logical-volumes/{_urlquote(identifier, safe='')}/discover", method="GET", query_params=query_params, model=gen.ObjectVolumeDiscoveryInfoView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectVolumeDiscoveryInfoView, raw=raw)
