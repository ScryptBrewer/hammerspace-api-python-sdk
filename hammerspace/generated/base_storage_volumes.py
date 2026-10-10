"""Spec-generated client for the "base-storage-volumes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedBaseStorageVolumesClient:
    """Typed coverage for all 2 "base-storage-volumes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BaseStorageVolumeView], gen.BaseStorageVolumeView, Any]:
        'Get all volumes (File and Object)'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/base-storage-volumes', method="GET", query_params=query_params, model=gen.BaseStorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.BaseStorageVolumeView, raw=raw)

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BaseStorageVolumeView], gen.BaseStorageVolumeView, Any]:
        'Get a volume by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/base-storage-volumes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.BaseStorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.BaseStorageVolumeView, raw=raw)
