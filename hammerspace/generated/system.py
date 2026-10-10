"""Spec-generated client for the "system" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Union

from hammerspace.models import generated as gen


class GeneratedSystemClient:
    """Typed coverage for all 3 "system" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get_counts(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdClusterView], gen.PdClusterView, Any]:
        'Get storage-related counts (systems, volumes, shares, files)'
        query_params = {}
        response = self.api_client.make_rest_call(path='/system/counts', method="GET", query_params=query_params, model=gen.PdClusterView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PdClusterView, raw=raw)

    def get_health(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SystemHealthView], gen.SystemHealthView, Any]:
        'Get a summary of system health'
        query_params = {}
        response = self.api_client.make_rest_call(path='/system/health', method="GET", query_params=query_params, model=gen.SystemHealthView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SystemHealthView, raw=raw)

    def ping(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdClusterView], gen.PdClusterView, Any]:
        'responds with empty body'
        query_params = {}
        response = self.api_client.make_rest_call(path='/system/ping', method="GET", query_params=query_params, model=gen.PdClusterView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PdClusterView, raw=raw)
