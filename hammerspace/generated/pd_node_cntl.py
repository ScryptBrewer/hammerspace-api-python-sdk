"""Spec-generated client for the "pd-node-cntl" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, Optional

from hammerspace.models import generated as gen


class GeneratedPdNodeCntlClient:
    """Typed coverage for all 2 "pd-node-cntl" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def add(self, ip: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Add HA node'
        query_params = {}
        if ip is not None: query_params['ip'] = ip
        return self.api_client.execute_and_monitor_task(
            path='/pd-node-cntl/add',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def repair(self, id: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Repair storage node'
        query_params = {}
        if id is not None: query_params['id'] = id
        return self.api_client.execute_and_monitor_task(
            path='/pd-node-cntl/repair',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
