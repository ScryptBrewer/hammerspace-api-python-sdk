"""Spec-generated client for the "object-stores" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedObjectStoresClient:
    """Typed coverage for all 4 "object-stores" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStoreView], gen.ObjectStoreView, Any]:
        'Get all internal object stores'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/object-stores', method="GET", query_params=query_params, model=gen.ObjectStoreView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectStoreView, raw=raw)

    def create(self, create_placement_objectives: Optional[Any] = None, body: Optional[gen.ObjectStoreView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStoreView], gen.ObjectStoreView, Any]:
        'Create an internal object store'
        query_params = {}
        if create_placement_objectives is not None: query_params['createPlacementObjectives'] = create_placement_objectives
        return self.api_client.execute_and_monitor_task(
            path='/object-stores',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectStoreView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStoreView], gen.ObjectStoreView, Any]:
        'Delete an internal object store'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/object-stores/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectStoreView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStoreView], gen.ObjectStoreView, Any]:
        'Get an internal object store by ID, Name, or Internal ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/object-stores/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ObjectStoreView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectStoreView, raw=raw)
