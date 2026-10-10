"""Spec-generated client for the "logical-volumes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedLogicalVolumesClient:
    """Typed coverage for all 5 "logical-volumes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LogicalVolumeView], gen.LogicalVolumeView, Any]:
        'Get all logical volumes'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/logical-volumes', method="GET", query_params=query_params, model=gen.LogicalVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LogicalVolumeView, raw=raw)

    def create(self, node_name: Optional[Any] = None, device_path: Optional[Any] = None, force: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LogicalVolumeView], gen.LogicalVolumeView, Any]:
        'Create a logical volume'
        query_params = {}
        if node_name is not None: query_params['nodeName'] = node_name
        if device_path is not None: query_params['devicePath'] = device_path
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path='/logical-volumes',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LogicalVolumeView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LogicalVolumeView], gen.LogicalVolumeView, Any]:
        'Delete logical volume by ID'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/logical-volumes/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LogicalVolumeView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LogicalVolumeView], gen.LogicalVolumeView, Any]:
        'Get logical volume by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/logical-volumes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.LogicalVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LogicalVolumeView, raw=raw)

    def discover(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LogicalVolumeView], gen.LogicalVolumeView, Any]:
        'Discover a logical volume'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/logical-volumes/{_urlquote(identifier, safe='')}/discover", method="GET", query_params=query_params, model=gen.LogicalVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LogicalVolumeView, raw=raw)
