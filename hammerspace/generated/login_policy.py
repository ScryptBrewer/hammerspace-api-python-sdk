"""Spec-generated client for the "login-policy" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedLoginPolicyClient:
    """Typed coverage for all 5 "login-policy" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LoginPolicyView], gen.LoginPolicyView, Any]:
        'Get all login policies'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/login-policy', method="GET", query_params=query_params, model=gen.LoginPolicyView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LoginPolicyView, raw=raw)

    def create(self, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LoginPolicyView], gen.LoginPolicyView, Any]:
        'Create a login policy'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/login-policy',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LoginPolicyView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LoginPolicyView], gen.LoginPolicyView, Any]:
        'Delete a login policy'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/login-policy/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LoginPolicyView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LoginPolicyView], gen.LoginPolicyView, Any]:
        'Get a login policy'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/login-policy/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.LoginPolicyView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LoginPolicyView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.LoginPolicyView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LoginPolicyView], gen.LoginPolicyView, Any]:
        'Update a login policy'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/login-policy/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LoginPolicyView,
            raw=raw,
        )
