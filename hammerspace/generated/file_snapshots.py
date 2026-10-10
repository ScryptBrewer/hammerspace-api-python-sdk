"""Spec-generated client for the "file-snapshots" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedFileSnapshotsClient:
    """Typed coverage for all 10 "file-snapshots" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FileSnapshotView], gen.FileSnapshotView, Any]:
        'List all file snapshots'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/file-snapshots', method="GET", query_params=query_params, model=gen.FileSnapshotView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.FileSnapshotView, raw=raw)

    def create(self, body: Optional[gen.FileSnapshotView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FileSnapshotView], gen.FileSnapshotView, Any]:
        'Create file snapshot'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/file-snapshots',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.FileSnapshotView,
            raw=raw,
        )

    def create_snapshot(self, filename_expression: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create file snapshot'
        query_params = {}
        if filename_expression is not None: query_params['filename-expression'] = filename_expression
        return self.api_client.execute_and_monitor_task(
            path='/file-snapshots/create',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete_snapshot(self, filename_expression: Optional[Any] = None, date_time_expression: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.CommandResultView], gen.CommandResultView, Any]:
        'Delete file snapshot'
        query_params = {}
        if filename_expression is not None: query_params['filename-expression'] = filename_expression
        if date_time_expression is not None: query_params['date-time-expression'] = date_time_expression
        return self.api_client.execute_and_monitor_task(
            path='/file-snapshots/delete',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.CommandResultView,
            raw=raw,
        )

    def list_snapshots(self, filename_expression: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FileStatView], gen.FileStatView, Any]:
        'Get all file snapshots'
        query_params = {}
        if filename_expression is not None: query_params['filename-expression'] = filename_expression
        response = self.api_client.make_rest_call(path='/file-snapshots/list', method="GET", query_params=query_params, model=gen.FileStatView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.FileStatView, raw=raw)

    def restore(self, filename_expression: Optional[Any] = None, date_time_expression: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.CommandResultView], gen.CommandResultView, Any]:
        'Restore file from snapshot'
        query_params = {}
        if filename_expression is not None: query_params['filename-expression'] = filename_expression
        if date_time_expression is not None: query_params['date-time-expression'] = date_time_expression
        return self.api_client.execute_and_monitor_task(
            path='/file-snapshots/restore',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.CommandResultView,
            raw=raw,
        )

    def clone(self, file_source: str, file_destination: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Clone file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/file-snapshots/{_urlquote(file_source, safe='')}/{_urlquote(file_destination, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FileSnapshotView], gen.FileSnapshotView, Any]:
        'Delete file snapshot'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/file-snapshots/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.FileSnapshotView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FileSnapshotView], gen.FileSnapshotView, Any]:
        'Get file snapshot by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/file-snapshots/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.FileSnapshotView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.FileSnapshotView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.FileSnapshotView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FileSnapshotView], gen.FileSnapshotView, Any]:
        'Update file snapshot'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/file-snapshots/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.FileSnapshotView,
            raw=raw,
        )
