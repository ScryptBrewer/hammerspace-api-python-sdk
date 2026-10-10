"""Spec-generated client for the "sites" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedSitesClient:
    """Typed coverage for all 7 "sites" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SiteView], gen.SiteView, Any]:
        'Get all sites'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/sites', method="GET", query_params=query_params, model=gen.SiteView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SiteView, raw=raw)

    def add_remote_site(self, body: Optional[gen.RemoteSiteView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SiteView], gen.SiteView, Any]:
        'Add a new remote site'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/sites',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SiteView,
            raw=raw,
        )

    def discover_remote_site(self, address: str, sync: Optional[Any] = None, validate_replication_ports: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SiteView], gen.SiteView, Any]:
        'Discover a remote site and possibly update a matching existing one'
        query_params = {}
        if sync is not None: query_params['sync'] = sync
        if validate_replication_ports is not None: query_params['validateReplicationPorts'] = validate_replication_ports
        response = self.api_client.make_rest_call(path=f"/sites/discover/{_urlquote(address, safe='')}", method="GET", query_params=query_params, model=gen.SiteView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SiteView, raw=raw)

    def get_local(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SiteView], gen.SiteView, Any]:
        'Get the local site'
        query_params = {}
        response = self.api_client.make_rest_call(path='/sites/local', method="GET", query_params=query_params, model=gen.SiteView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SiteView, raw=raw)

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.CommandResultView], gen.CommandResultView, Any]:
        'Remove a remote site'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/sites/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.CommandResultView,
            raw=raw,
        )

    def get(self, identifier: str, type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SiteView], gen.SiteView, Any]:
        'Get a site by ID'
        query_params = {}
        if type is not None: query_params['type'] = type
        response = self.api_client.make_rest_call(path=f"/sites/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.SiteView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SiteView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.SiteView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SiteView], gen.SiteView, Any]:
        'Update a site'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/sites/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SiteView,
            raw=raw,
        )
