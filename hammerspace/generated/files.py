"""Spec-generated client for the "files" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedFilesClient:
    """Typed coverage for all 5 "files" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, path_param: Optional[Any] = None, include_replication_details: Optional[Any] = None, get_parent_dir_size: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FsNodeView], gen.FsNodeView, Any]:
        'Get file details'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        if include_replication_details is not None: query_params['includeReplicationDetails'] = include_replication_details
        if get_parent_dir_size is not None: query_params['getParentDirSize'] = get_parent_dir_size
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/files', method="GET", query_params=query_params, model=gen.FsNodeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.FsNodeView, raw=raw)

    def get_file_owner(self, path_param: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        "Query a DP for file info (prepends '/mnt/data-portal' to provided path)"
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        response = self.api_client.make_rest_call(path='/files/file_exists_dp', method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def get_used_capacity(self, path_param: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Get used capacity'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        response = self.api_client.make_rest_call(path='/files/used_capacity', method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def worm_delete(self, share_identifier: str, path_param: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Perform a privileged delete on a WORM file or empty dir'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/files/worm/{_urlquote(share_identifier, safe='')}/{_urlquote(path_param, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, path_param: str, pattern: Optional[Any] = None, dalil: Optional[Any] = None, itself: Optional[Any] = None, include_replication_details: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.FsNodeView], gen.FsNodeView, Any]:
        'Get file details'
        query_params = {}
        if pattern is not None: query_params['pattern'] = pattern
        if dalil is not None: query_params['dalil'] = dalil
        if itself is not None: query_params['itself'] = itself
        if include_replication_details is not None: query_params['includeReplicationDetails'] = include_replication_details
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path=f"/files/{_urlquote(path_param, safe='')}", method="GET", query_params=query_params, model=gen.FsNodeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.FsNodeView, raw=raw)
