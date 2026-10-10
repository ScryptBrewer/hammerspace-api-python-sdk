"""Spec-generated client for the "cntl" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedCntlClient:
    """Typed coverage for all 6 "cntl" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, view_type: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdClusterView], gen.PdClusterView, Any]:
        'Get cluster info'
        query_params = {}
        if view_type is not None: query_params['viewType'] = view_type
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/cntl', method="GET", query_params=query_params, model=gen.PdClusterView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PdClusterView, raw=raw)

    def accept_eula(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Accept the EULA at https://hammerspace.com/company/EULA/'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/cntl/accept-eula',
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def shutdown(self, poweroff: Optional[Any] = None, reboot: Optional[Any] = None, reason: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Shutdown'
        query_params = {}
        if poweroff is not None: query_params['poweroff'] = poweroff
        if reboot is not None: query_params['reboot'] = reboot
        if reason is not None: query_params['reason'] = reason
        return self.api_client.execute_and_monitor_task(
            path='/cntl/shutdown',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def list_cntl(self, with_uncleared_event_severity: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdClusterView], gen.PdClusterView, Any]:
        'Get cluster info'
        query_params = {}
        if with_uncleared_event_severity is not None: query_params['withUnclearedEventSeverity'] = with_uncleared_event_severity
        response = self.api_client.make_rest_call(path='/cntl/state', method="GET", query_params=query_params, model=gen.PdClusterView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PdClusterView, raw=raw)

    def get(self, identifier: str, view_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdClusterView], gen.PdClusterView, Any]:
        'Get cluster info'
        query_params = {}
        if view_type is not None: query_params['viewType'] = view_type
        response = self.api_client.make_rest_call(path=f"/cntl/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.PdClusterView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PdClusterView, raw=raw)

    def update(self, identifier: str, view_type: Optional[Any] = None, body: Optional[gen.PdClusterView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdClusterView], gen.PdClusterView, Any]:
        'Update Cluster'
        query_params = {}
        if view_type is not None: query_params['viewType'] = view_type
        return self.api_client.execute_and_monitor_task(
            path=f"/cntl/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.PdClusterView,
            raw=raw,
        )
