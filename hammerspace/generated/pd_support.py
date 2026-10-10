"""Spec-generated client for the "pd-support" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union

from hammerspace.models import generated as gen


class GeneratedPdSupportClient:
    """Typed coverage for all 1 "pd-support" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def create(self, body: Optional[gen.PdSupportView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PdSupportView], gen.PdSupportView, Any]:
        'Collect logs for support'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/pd-support',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.PdSupportView,
            raw=raw,
        )
