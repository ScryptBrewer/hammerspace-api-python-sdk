"""Spec-generated client for the "login" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any

from hammerspace.models import generated as gen


class GeneratedLoginClient:
    """Typed coverage for all 1 "login" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def login(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Login'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/login',
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
