"""Spec-generated client for the "subnet-gateways" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedSubnetGatewaysClient:
    """Typed coverage for all 3 "subnet-gateways" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SubnetGatewayView], gen.SubnetGatewayView, Any]:
        'List the configured subnet gateways'
        query_params = {}
        response = self.api_client.make_rest_call(path='/subnet-gateways', method="GET", query_params=query_params, model=gen.SubnetGatewayView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SubnetGatewayView, raw=raw)

    def create(self, body: Optional[gen.SubnetGatewayView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SubnetGatewayView], gen.SubnetGatewayView, Any]:
        'Add a new subnet gateway'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/subnet-gateways',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SubnetGatewayView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Delete a subnet gateway'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/subnet-gateways/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
