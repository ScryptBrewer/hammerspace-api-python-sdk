"""Spec-generated client for the "versions" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedVersionsClient:
    """Typed coverage for all 4 "versions" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list_available(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SwVersionView], gen.SwVersionView, Any]:
        'List available packages'
        query_params = {}
        response = self.api_client.make_rest_call(path='/versions/available', method="GET", query_params=query_params, model=gen.SwVersionView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SwVersionView, raw=raw)

    def delete_packages(self, package_name: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Delete packages'
        query_params = {}
        if package_name is not None: query_params['package-name'] = package_name
        return self.api_client.execute_and_monitor_task(
            path='/versions/delete',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def upload_package(self, body: Optional[gen.InputStream] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Upload package'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/versions/upload',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def upload_package_upload(self, package_location: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Upload package'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/versions/upload/{_urlquote(package_location, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
