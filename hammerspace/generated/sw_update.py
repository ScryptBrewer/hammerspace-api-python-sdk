"""Spec-generated client for the "sw-update" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedSwUpdateClient:
    """Typed coverage for all 5 "sw-update" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SwUpdateTaskView], gen.SwUpdateTaskView, Any]:
        'Get all sw update tasks'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/sw-update', method="GET", query_params=query_params, model=gen.SwUpdateTaskView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SwUpdateTaskView, raw=raw)

    def apply(self, version: str, node_identifier: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Apply update'
        query_params = {}
        if node_identifier is not None: query_params['node-identifier'] = node_identifier
        return self.api_client.execute_and_monitor_task(
            path=f"/sw-update/apply/{_urlquote(version, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def apply_system(self, version: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Apply update'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/sw-update/apply/{_urlquote(version, safe='')}/system",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SwUpdateTaskView], gen.SwUpdateTaskView, Any]:
        'Get sw update task'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/sw-update/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.SwUpdateTaskView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SwUpdateTaskView, raw=raw)

    def cancel(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Cancel software update task'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/sw-update/{_urlquote(identifier, safe='')}/cancel",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
