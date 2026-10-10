"""Spec-generated client for the "domain-idmaps" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedDomainIdmapsClient:
    """Typed coverage for all 6 "domain-idmaps" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapIdMapView], gen.LdapIdMapView, Any]:
        'Get all LDAP ID maps'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/domain-idmaps', method="GET", query_params=query_params, model=gen.LdapIdMapView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LdapIdMapView, raw=raw)

    def create(self, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapIdMapView], gen.LdapIdMapView, Any]:
        'Create LDAP ID map'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/domain-idmaps',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LdapIdMapView,
            raw=raw,
        )

    def decommission(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Reload domain mapping rules'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/domain-idmaps/reload',
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapIdMapView], gen.LdapIdMapView, Any]:
        'Delete LDAP ID map'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/domain-idmaps/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LdapIdMapView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapIdMapView], gen.LdapIdMapView, Any]:
        'Get LDAP ID map by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/domain-idmaps/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.LdapIdMapView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LdapIdMapView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.LdapIdMapView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapIdMapView], gen.LdapIdMapView, Any]:
        'Update LDAP ID map'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/domain-idmaps/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LdapIdMapView,
            raw=raw,
        )
