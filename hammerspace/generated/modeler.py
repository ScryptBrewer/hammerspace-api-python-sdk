"""Spec-generated client for the "modeler" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedModelerClient:
    """Typed coverage for all 2 "modeler" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def create_tree_stats(self, share: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Query pdfs for tree stats'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/modeler/tree-stats/trigger-sweep/{_urlquote(share, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get_tree_stats(self, share: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Get latest tree stats of share'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/modeler/tree-stats/{_urlquote(share, safe='')}", method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)
