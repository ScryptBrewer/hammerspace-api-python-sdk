"""Spec-generated client for the "data-portals" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedDataPortalsClient:
    """Typed coverage for all 3 "data-portals" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.DataPortalView], gen.DataPortalView, Any]:
        'Get all Data Portals'
        query_params = {}
        response = self.api_client.make_rest_call(path='/data-portals', method="GET", query_params=query_params, model=gen.DataPortalView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.DataPortalView, raw=raw)

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.DataPortalView], gen.DataPortalView, Any]:
        'Get a Data Portal'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/data-portals/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.DataPortalView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.DataPortalView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.DataPortalView], gen.DataPortalView, Any]:
        'Update data portal'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/data-portals/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.DataPortalView,
            raw=raw,
        )
