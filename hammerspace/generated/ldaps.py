"""Spec-generated client for the "ldaps" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedLdapsClient:
    """Typed coverage for all 5 "ldaps" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapView], gen.LdapView, Any]:
        'Get LDAP'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/ldaps', method="GET", query_params=query_params, model=gen.LdapView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LdapView, raw=raw)

    def create(self, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapView], gen.LdapView, Any]:
        'Configure LDAP'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/ldaps',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LdapView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapView], gen.LdapView, Any]:
        'Delete LDAP'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/ldaps/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LdapView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapView], gen.LdapView, Any]:
        'Get LDAP'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/ldaps/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.LdapView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LdapView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.LdapView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LdapView], gen.LdapView, Any]:
        'Update LDAP'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/ldaps/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.LdapView,
            raw=raw,
        )
