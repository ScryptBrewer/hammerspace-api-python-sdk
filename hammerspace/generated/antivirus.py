"""Spec-generated client for the "antivirus" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedAntivirusClient:
    """Typed coverage for all 5 "antivirus" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.AntivirusView], gen.AntivirusView, Any]:
        'Get all antivirus services'
        query_params = {}
        response = self.api_client.make_rest_call(path='/antivirus', method="GET", query_params=query_params, model=gen.AntivirusView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.AntivirusView, raw=raw)

    def create(self, create_placement_objectives: Optional[Any] = None, body: Optional[gen.AntivirusView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.AntivirusView], gen.AntivirusView, Any]:
        'Add an antivirus service'
        query_params = {}
        if create_placement_objectives is not None: query_params['createPlacementObjectives'] = create_placement_objectives
        return self.api_client.execute_and_monitor_task(
            path='/antivirus',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.AntivirusView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.AntivirusView], gen.AntivirusView, Any]:
        'Remove an antivirus service'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/antivirus/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.AntivirusView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.AntivirusView], gen.AntivirusView, Any]:
        'Get an antivirus service by identifier'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/antivirus/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.AntivirusView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.AntivirusView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.AntivirusView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.AntivirusView], gen.AntivirusView, Any]:
        'Update an antivirus service'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/antivirus/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.AntivirusView,
            raw=raw,
        )
