"""Spec-generated client for the "license-server" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedLicenseServerClient:
    """Typed coverage for all 2 "license-server" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LicenseActivationView], gen.LicenseActivationView, Any]:
        'Get all metered licenses'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/license-server', method="GET", query_params=query_params, model=gen.LicenseActivationView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LicenseActivationView, raw=raw)

    def report_usage(self, uuid: str, body: Optional[gen.LicenseActivationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Report license usage.'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/license-server/report-usage/{_urlquote(uuid, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
