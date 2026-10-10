"""Spec-generated client for the "backup" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedBackupClient:
    """Typed coverage for all 8 "backup" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BackupView], gen.BackupView, Any]:
        'Get Backup configuration'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/backup', method="GET", query_params=query_params, model=gen.BackupView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.BackupView, raw=raw)

    def configure(self, body: Optional[gen.BackupView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BackupView], gen.BackupView, Any]:
        'Create a backup schedule'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/backup',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.BackupView,
            raw=raw,
        )

    def backup_create(self, volume_ip: str, export_path: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create immediate backup'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/backup/backup-create/{_urlquote(volume_ip, safe='')}/{_urlquote(export_path, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def backuplist(self, volume_ip: str, export_path: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'List all backups'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/backup/backup-list/{_urlquote(volume_ip, safe='')}/{_urlquote(export_path, safe='')}", method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def create(self, volume_ip: str, export_path: str, cluster_uuid: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Restore latest backup from storage volume'
        query_params = {}
        if cluster_uuid is not None: query_params['cluster-uuid'] = cluster_uuid
        return self.api_client.execute_and_monitor_task(
            path=f"/backup/backup-restore/{_urlquote(volume_ip, safe='')}/{_urlquote(export_path, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def create_backup_restore(self, volume_ip: str, export_path: str, backup_name: str, cluster_uuid: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Restore backup from storage volume'
        query_params = {}
        if cluster_uuid is not None: query_params['cluster-uuid'] = cluster_uuid
        return self.api_client.execute_and_monitor_task(
            path=f"/backup/backup-restore/{_urlquote(volume_ip, safe='')}/{_urlquote(export_path, safe='')}/{_urlquote(backup_name, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BackupView], gen.BackupView, Any]:
        'Delete backup schedule'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/backup/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.BackupView,
            raw=raw,
        )

    def update(self, identifier: str, body: Optional[gen.BackupView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BackupView], gen.BackupView, Any]:
        'Update a backup schedule'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/backup/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.BackupView,
            raw=raw,
        )
