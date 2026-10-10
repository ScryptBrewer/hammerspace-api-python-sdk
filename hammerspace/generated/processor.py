"""Spec-generated client for the "processor" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedProcessorClient:
    """Typed coverage for all 5 "processor" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ProcessorView], gen.ProcessorView, Any]:
        'Get all processor services'
        query_params = {}
        response = self.api_client.make_rest_call(path='/processor', method="GET", query_params=query_params, model=gen.ProcessorView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ProcessorView, raw=raw)

    def create(self, create_placement_objectives: Optional[Any] = None, body: Optional[gen.ProcessorView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ProcessorView], gen.ProcessorView, Any]:
        'Add a processor service'
        query_params = {}
        if create_placement_objectives is not None: query_params['createPlacementObjectives'] = create_placement_objectives
        return self.api_client.execute_and_monitor_task(
            path='/processor',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ProcessorView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ProcessorView], gen.ProcessorView, Any]:
        'Remove a processor service'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/processor/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ProcessorView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ProcessorView], gen.ProcessorView, Any]:
        'Get a processor service by identifier'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/processor/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ProcessorView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ProcessorView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.ProcessorView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ProcessorView], gen.ProcessorView, Any]:
        'Update a processor service'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/processor/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ProcessorView,
            raw=raw,
        )
