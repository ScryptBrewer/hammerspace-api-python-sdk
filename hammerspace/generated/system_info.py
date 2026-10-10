"""Spec-generated client for the "system-info" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union

from hammerspace.models import generated as gen


class GeneratedSystemInfoClient:
    """Typed coverage for all 1 "system-info" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, timeout_sec: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SystemInfoView], gen.SystemInfoView, Any]:
        'Get system information'
        query_params = {}
        if timeout_sec is not None: query_params['timeoutSec'] = timeout_sec
        response = self.api_client.make_rest_call(path='/system-info', method="GET", query_params=query_params, model=gen.SystemInfoView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SystemInfoView, raw=raw)
