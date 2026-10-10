"""Spec-generated client for the "data-copy-to-object" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, Optional

from hammerspace.models import generated as gen


class GeneratedDataCopyToObjectClient:
    """Typed coverage for all 2 "data-copy-to-object" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def create(self, bucket: Optional[Any] = None, share: Optional[Any] = None, source_path: Optional[Any] = None, dest_path: Optional[Any] = None, body: Optional[gen.NodeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Start a data copy to object task'
        query_params = {}
        if bucket is not None: query_params['bucket'] = bucket
        if share is not None: query_params['share'] = share
        if source_path is not None: query_params['sourcePath'] = source_path
        if dest_path is not None: query_params['destPath'] = dest_path
        return self.api_client.execute_and_monitor_task(
            path='/data-copy-to-object',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def list_buckets(self, body: Optional[gen.NodeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Return a listing of buckets from the specified object storage'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/data-copy-to-object/list-buckets',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
