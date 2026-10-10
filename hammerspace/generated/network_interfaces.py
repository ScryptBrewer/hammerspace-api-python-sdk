"""Spec-generated client for the "network-interfaces" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedNetworkInterfacesClient:
    """Typed coverage for all 6 "network-interfaces" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NetworkInterfaceView], gen.NetworkInterfaceView, Any]:
        'Get all network interfaces'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/network-interfaces', method="GET", query_params=query_params, model=gen.NetworkInterfaceView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NetworkInterfaceView, raw=raw)

    def resolve(self, node: Optional[Any] = None, if_name: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NetworkInterfaceView], gen.NetworkInterfaceView, Any]:
        'Get network interface by node and name'
        query_params = {}
        if node is not None: query_params['node'] = node
        if if_name is not None: query_params['ifName'] = if_name
        response = self.api_client.make_rest_call(path='/network-interfaces/resolve', method="GET", query_params=query_params, model=gen.NetworkInterfaceView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NetworkInterfaceView, raw=raw)

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NetworkInterfaceView], gen.NetworkInterfaceView, Any]:
        'Delete network interface by ID'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/network-interfaces/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NetworkInterfaceView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NetworkInterfaceView], gen.NetworkInterfaceView, Any]:
        'Get network interface by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/network-interfaces/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.NetworkInterfaceView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NetworkInterfaceView, raw=raw)

    def create(self, identifier: str, body: Optional[gen.NetworkInterfaceView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NetworkInterfaceView], gen.NetworkInterfaceView, Any]:
        'Create virtual network interface'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/network-interfaces/{_urlquote(identifier, safe='')}",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NetworkInterfaceView,
            raw=raw,
        )

    def update(self, identifier: str, override_data_check: Optional[Any] = None, body: Optional[gen.NetworkInterfaceView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NetworkInterfaceView], gen.NetworkInterfaceView, Any]:
        'Update network interface by ID'
        query_params = {}
        if override_data_check is not None: query_params['overrideDataCheck'] = override_data_check
        return self.api_client.execute_and_monitor_task(
            path=f"/network-interfaces/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NetworkInterfaceView,
            raw=raw,
        )
