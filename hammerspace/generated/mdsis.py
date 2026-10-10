"""Spec-generated client for the "mdsis" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedMdsisClient:
    """Typed coverage for all 4 "mdsis" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.MdsiView], gen.MdsiView, Any]:
        'Get all MDSIs'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/mdsis', method="GET", query_params=query_params, model=gen.MdsiView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.MdsiView, raw=raw)

    def create(self, body: Optional[gen.MdsiView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Add MDSI and related MDSI container node'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/mdsis',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, force: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove MDSI and related MDSI container node if there is one'
        query_params = {}
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path=f"/mdsis/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.MdsiView], gen.MdsiView, Any]:
        'Get MDSI by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/mdsis/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.MdsiView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.MdsiView, raw=raw)
