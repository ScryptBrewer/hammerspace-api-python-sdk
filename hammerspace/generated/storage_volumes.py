"""Spec-generated client for the "storage-volumes" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedStorageVolumesClient:
    """Typed coverage for all 8 "storage-volumes" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StorageVolumeView], gen.StorageVolumeView, Any]:
        'Get all storage volumes'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/storage-volumes', method="GET", query_params=query_params, model=gen.StorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StorageVolumeView, raw=raw)

    def create(self, force: Optional[Any] = None, stripe_align_to_default: Optional[Any] = None, skip_perf_test: Optional[Any] = None, skip_config_test: Optional[Any] = None, create_placement_objectives: Optional[Any] = None, body: Optional[gen.StorageVolumeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create storage volume'
        query_params = {}
        if force is not None: query_params['force'] = force
        if stripe_align_to_default is not None: query_params['stripeAlignToDefault'] = stripe_align_to_default
        if skip_perf_test is not None: query_params['skipPerfTest'] = skip_perf_test
        if skip_config_test is not None: query_params['skipConfigTest'] = skip_config_test
        if create_placement_objectives is not None: query_params['createPlacementObjectives'] = create_placement_objectives
        return self.api_client.execute_and_monitor_task(
            path='/storage-volumes',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def related_list(self, filter_uuid: Optional[Any] = None, filter_object_type: Optional[Any] = None, sort: Optional[Any] = None, terse: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StorageVolumeView], gen.StorageVolumeView, Any]:
        'Get all storage volumes filtered by relation to other entity'
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
        response = self.api_client.make_rest_call(path='/storage-volumes/related-list', method="GET", query_params=query_params, model=gen.StorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StorageVolumeView, raw=raw)

    def delete(self, identifier: str, bypass_decommission: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StorageVolumeView], gen.StorageVolumeView, Any]:
        'Delete storage volume'
        query_params = {}
        if bypass_decommission is not None: query_params['bypassDecommission'] = bypass_decommission
        return self.api_client.execute_and_monitor_task(
            path=f"/storage-volumes/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.StorageVolumeView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StorageVolumeView], gen.StorageVolumeView, Any]:
        'Get storage volume by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/storage-volumes/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.StorageVolumeView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StorageVolumeView, raw=raw)

    def update(self, identifier: str, stripe_align_to_default: Optional[Any] = None, body: Optional[gen.StorageVolumeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StorageVolumeView], gen.StorageVolumeView, Any]:
        'Update storage volume'
        query_params = {}
        if stripe_align_to_default is not None: query_params['stripeAlignToDefault'] = stripe_align_to_default
        return self.api_client.execute_and_monitor_task(
            path=f"/storage-volumes/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.StorageVolumeView,
            raw=raw,
        )

    def assimilation(self, identifier: str, body: Optional[gen.AssimilationSpecView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Assimilate existing storage volume'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/storage-volumes/{_urlquote(identifier, safe='')}/assimilation",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def replace(self, identifier: str, body: Optional[gen.LocationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StorageVolumeView], gen.StorageVolumeView, Any]:
        'Replace storage volume'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/storage-volumes/{_urlquote(identifier, safe='')}/replace",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.StorageVolumeView,
            raw=raw,
        )
