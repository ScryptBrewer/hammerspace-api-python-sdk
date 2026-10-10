"""Spec-generated client for the "ad" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedAdClient:
    """Typed coverage for all 5 "ad" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, include_discovery_info: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SambaAdView], gen.SambaAdView, Any]:
        'Get AD configuration'
        query_params = {}
        if include_discovery_info is not None: query_params['includeDiscoveryInfo'] = include_discovery_info
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/ad', method="GET", query_params=query_params, model=gen.SambaAdView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SambaAdView, raw=raw)

    def discover_realm(self, domain: str, include_server_time: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.RealmDiscoverInfoView], gen.RealmDiscoverInfoView, Any]:
        'Get discovered realm information'
        query_params = {}
        if include_server_time is not None: query_params['includeServerTime'] = include_server_time
        response = self.api_client.make_rest_call(path=f"/ad/discover/{_urlquote(domain, safe='')}", method="GET", query_params=query_params, model=gen.RealmDiscoverInfoView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.RealmDiscoverInfoView, raw=raw)

    def flush_cache(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Flush AD cache'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/ad/flush_cache',
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, include_discovery_info: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SambaAdView], gen.SambaAdView, Any]:
        'Get an AD by ID'
        query_params = {}
        if include_discovery_info is not None: query_params['includeDiscoveryInfo'] = include_discovery_info
        response = self.api_client.make_rest_call(path=f"/ad/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.SambaAdView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SambaAdView, raw=raw)

    def update(self, identifier: str, nfs_spns_action: Optional[Any] = None, body: Optional[gen.SambaAdView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SambaAdView], gen.SambaAdView, Any]:
        'Configure AD'
        query_params = {}
        if nfs_spns_action is not None: query_params['nfs-spns-action'] = nfs_spns_action
        return self.api_client.execute_and_monitor_task(
            path=f"/ad/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SambaAdView,
            raw=raw,
        )
