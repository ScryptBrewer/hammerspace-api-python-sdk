"""Spec-generated client for the "share-snapshots" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedShareSnapshotsClient:
    """Typed coverage for all 10 "share-snapshots" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareSnapshotView], gen.ShareSnapshotView, Any]:
        'List all share scheduled snapshots'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/share-snapshots', method="GET", query_params=query_params, model=gen.ShareSnapshotView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareSnapshotView, raw=raw)

    def create(self, body: Optional[gen.ShareSnapshotView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareSnapshotView], gen.ShareSnapshotView, Any]:
        'Create share snapshot schedule'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/share-snapshots',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareSnapshotView,
            raw=raw,
        )

    def clone_create(self, share_identifier: str, snapshot_name: Optional[Any] = None, destination_path: Optional[Any] = None, overwrite_destination: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Clone share snapshot'
        query_params = {}
        if snapshot_name is not None: query_params['snapshot-name'] = snapshot_name
        if destination_path is not None: query_params['destination-path'] = destination_path
        if overwrite_destination is not None: query_params['overwrite-destination'] = overwrite_destination
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/clone-create/{_urlquote(share_identifier, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def snapshot_create(self, share_identifier: str, snapshot_name: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create immediate share snapshot'
        query_params = {}
        if snapshot_name is not None: query_params['snapshot-name'] = snapshot_name
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/snapshot-create/{_urlquote(share_identifier, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def snapshot_delete(self, share_identifier: str, snapshot_name: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.CommandResultView], gen.CommandResultView, Any]:
        'Delete share snapshot'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/snapshot-delete/{_urlquote(share_identifier, safe='')}/{_urlquote(snapshot_name, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.CommandResultView,
            raw=raw,
        )

    def snapshot_list(self, share_identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'List share snapshots'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/share-snapshots/snapshot-list/{_urlquote(share_identifier, safe='')}", method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def snapshot_restore(self, share_identifier: str, snapshot_name: str, filename: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.CommandResultView], gen.CommandResultView, Any]:
        'Restore files from share snapshot'
        query_params = {}
        if filename is not None: query_params['filename'] = filename
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/snapshot-restore-files/{_urlquote(share_identifier, safe='')}/{_urlquote(snapshot_name, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.CommandResultView,
            raw=raw,
        )

    def share_restore(self, share_identifier: str, snapshot_name: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Restore entire share from a snapshot'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/snapshot-restore/{_urlquote(share_identifier, safe='')}/{_urlquote(snapshot_name, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, clear_snapshots: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareSnapshotView], gen.ShareSnapshotView, Any]:
        'Delete share snapshot schedule'
        query_params = {}
        if clear_snapshots is not None: query_params['clear-snapshots'] = clear_snapshots
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareSnapshotView,
            raw=raw,
        )

    def update(self, identifier: str, body: Optional[gen.ShareSnapshotView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareSnapshotView], gen.ShareSnapshotView, Any]:
        'Update share snapshot schedule'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/share-snapshots/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareSnapshotView,
            raw=raw,
        )
