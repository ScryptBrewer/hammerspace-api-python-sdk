"""Spec-generated client for the "static-routes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedStaticRoutesClient:
    """Typed coverage for all 3 "static-routes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StaticRouteView], gen.StaticRouteView, Any]:
        'List the configured static routes'
        query_params = {}
        response = self.api_client.make_rest_call(path='/static-routes', method="GET", query_params=query_params, model=gen.StaticRouteView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StaticRouteView, raw=raw)

    def create(self, body: Optional[gen.StaticRouteView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StaticRouteView], gen.StaticRouteView, Any]:
        'Add a new static route'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/static-routes',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.StaticRouteView,
            raw=raw,
        )

    def delete(self, identifier: str, next_hop: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Delete a static route'
        query_params = {}
        if next_hop is not None: query_params['next-hop'] = next_hop
        return self.api_client.execute_and_monitor_task(
            path=f"/static-routes/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
