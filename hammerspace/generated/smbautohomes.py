"""Spec-generated client for the "smbautohomes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedSmbautohomesClient:
    """Typed coverage for all 8 "smbautohomes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmbAutoHomeView], gen.SmbAutoHomeView, Any]:
        'Get SMB autohome'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/smbautohomes', method="GET", query_params=query_params, model=gen.SmbAutoHomeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SmbAutoHomeView, raw=raw)

    def create(self, body: Optional[gen.SmbAutoHomeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmbAutoHomeView], gen.SmbAutoHomeView, Any]:
        'Create a new SMB autohome'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/smbautohomes',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SmbAutoHomeView,
            raw=raw,
        )

    def delete_default(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove the default SMB autohome'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/smbautohomes/default',
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete_by_username(self, username: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove an SMB autohome by username'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/smbautohomes/username/{_urlquote(username, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get_by_username(self, username: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmbAutoHomeView], gen.SmbAutoHomeView, Any]:
        'Get SMB autohome by username'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/smbautohomes/username/{_urlquote(username, safe='')}", method="GET", query_params=query_params, model=gen.SmbAutoHomeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SmbAutoHomeView, raw=raw)

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove an SMB autohome'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/smbautohomes/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmbAutoHomeView], gen.SmbAutoHomeView, Any]:
        'Get SMB autohome'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/smbautohomes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.SmbAutoHomeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SmbAutoHomeView, raw=raw)

    def update(self, identifier: str, force: Optional[Any] = None, body: Optional[gen.SmbAutoHomeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmbAutoHomeView], gen.SmbAutoHomeView, Any]:
        'Update SMB autohome'
        query_params = {}
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path=f"/smbautohomes/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SmbAutoHomeView,
            raw=raw,
        )
