"""Spec-generated client for the "object-storage-volumes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedObjectStorageVolumesClient:
    """Typed coverage for all 10 "object-storage-volumes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStorageVolumeView], gen.ObjectStorageVolumeView, Any]:
        'Get all object storage volumes'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/object-storage-volumes', method="GET", query_params=query_params, model=gen.ObjectStorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectStorageVolumeView, raw=raw)

    def create(self, create_placement_objectives: Optional[Any] = None, body: Optional[gen.ObjectStorageVolumeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStorageVolumeView], gen.ObjectStorageVolumeView, Any]:
        'Create object storage volume'
        query_params = {}
        if create_placement_objectives is not None: query_params['createPlacementObjectives'] = create_placement_objectives
        return self.api_client.execute_and_monitor_task(
            path='/object-storage-volumes',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectStorageVolumeView,
            raw=raw,
        )

    def related_list(self, filter_uuid: Optional[Any] = None, filter_object_type: Optional[Any] = None, sort: Optional[Any] = None, terse: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStorageVolumeView], gen.ObjectStorageVolumeView, Any]:
        'Get all object storage volumes filtered by relation to other entity'
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
        response = self.api_client.make_rest_call(path='/object-storage-volumes/related-list', method="GET", query_params=query_params, model=gen.ObjectStorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectStorageVolumeView, raw=raw)

    def delete(self, identifier: str, skip_gfs_validation: Optional[Any] = None, bypass_decommission: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Delete object storage volume'
        query_params = {}
        if skip_gfs_validation is not None: query_params['skipGfsValidation'] = skip_gfs_validation
        if bypass_decommission is not None: query_params['bypassDecommission'] = bypass_decommission
        return self.api_client.execute_and_monitor_task(
            path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStorageVolumeView], gen.ObjectStorageVolumeView, Any]:
        'Get object storage volume by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ObjectStorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectStorageVolumeView, raw=raw)

    def update(self, identifier: str, force: Optional[Any] = None, body: Optional[gen.ObjectStorageVolumeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStorageVolumeView], gen.ObjectStorageVolumeView, Any]:
        'Update object storage volume'
        query_params = {}
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectStorageVolumeView,
            raw=raw,
        )

    def stop_garbage_collection(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Stop garbage collection on an object storage volume'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}/garbage-collect",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def start_garbage_collection(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Start garbage collection on an object storage volume'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}/garbage-collect",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete_reservation(self, identifier: str, site_identifier: str, force: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectStorageVolumeView], gen.ObjectStorageVolumeView, Any]:
        "Delete a site's reservation from an object storage volume"
        query_params = {}
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}/remote-reservation/{_urlquote(site_identifier, safe='')}",
            method="PUT",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectStorageVolumeView,
            raw=raw,
        )

    def replace(self, identifier: str, body: Optional[gen.LocationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Replace object storage volume'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/object-storage-volumes/{_urlquote(identifier, safe='')}/replace",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
