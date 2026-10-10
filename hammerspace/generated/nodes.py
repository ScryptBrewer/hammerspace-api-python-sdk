"""Spec-generated client for the "nodes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedNodesClient:
    """Typed coverage for all 9 "nodes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NodeView], gen.NodeView, Any]:
        'Get all nodes'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/nodes', method="GET", query_params=query_params, model=gen.NodeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NodeView, raw=raw)

    def create(self, create_placement_objectives: Optional[Any] = None, ignore_ip_conflicts: Optional[Any] = None, body: Optional[gen.NodeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create node'
        query_params = {}
        if create_placement_objectives is not None: query_params['createPlacementObjectives'] = create_placement_objectives
        if ignore_ip_conflicts is not None: query_params['ignoreIpConflicts'] = ignore_ip_conflicts
        return self.api_client.execute_and_monitor_task(
            path='/nodes',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def related_list(self, filter_uuid: Optional[Any] = None, filter_object_type: Optional[Any] = None, sort: Optional[Any] = None, terse: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NodeView], gen.NodeView, Any]:
        'Get all nodes filtered by relation to other entity'
        query_params = {}
        if filter_uuid is not None: query_params['filterUuid'] = filter_uuid
        if filter_object_type is not None: query_params['filterObjectType'] = filter_object_type
        if sort is not None: query_params['sort'] = sort
        if terse is not None: query_params['terse'] = terse
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/nodes/related-list', method="GET", query_params=query_params, model=gen.NodeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NodeView, raw=raw)

    def list_unauthenticated(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NodeView], gen.NodeView, Any]:
        'Get unauthenticated nodes'
        query_params = {}
        response = self.api_client.make_rest_call(path='/nodes/unauthenticated', method="GET", query_params=query_params, model=gen.NodeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NodeView, raw=raw)

    def delete(self, identifier: str, force: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Delete node'
        query_params = {}
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path=f"/nodes/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, block_device_info: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NodeView], gen.NodeView, Any]:
        'Get node by ID'
        query_params = {}
        if block_device_info is not None: query_params['blockDeviceInfo'] = block_device_info
        response = self.api_client.make_rest_call(path=f"/nodes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.NodeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NodeView, raw=raw)

    def update(self, identifier: str, skip_object_volume_validations: Optional[Any] = None, body: Optional[gen.NodeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Update node'
        query_params = {}
        if skip_object_volume_validations is not None: query_params['skipObjectVolumeValidations'] = skip_object_volume_validations
        return self.api_client.execute_and_monitor_task(
            path=f"/nodes/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def refresh(self, identifier: str, rescan: Optional[Any] = None, reconcile_components: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Refresh node'
        query_params = {}
        if rescan is not None: query_params['rescan'] = rescan
        if reconcile_components is not None: query_params['reconcileComponents'] = reconcile_components
        return self.api_client.execute_and_monitor_task(
            path=f"/nodes/{_urlquote(identifier, safe='')}/refresh",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def change_mode(self, identifier: str, mode: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NodeView], gen.NodeView, Any]:
        'Change node mode'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/nodes/{_urlquote(identifier, safe='')}/set-mode/{_urlquote(mode, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NodeView,
            raw=raw,
        )
