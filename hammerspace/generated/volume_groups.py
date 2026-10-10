"""Spec-generated client for the "volume-groups" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedVolumeGroupsClient:
    """Typed coverage for all 7 "volume-groups" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Get all volume groups'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/volume-groups', method="GET", query_params=query_params, model=gen.VolumeGroupView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.VolumeGroupView, raw=raw)

    def create(self, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Create volume group'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/volume-groups',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.VolumeGroupView,
            raw=raw,
        )

    def find_by_location(self, uuid: Optional[Any] = None, object_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Get volume groups using given location'
        query_params = {}
        if uuid is not None: query_params['uuid'] = uuid
        if object_type is not None: query_params['objectType'] = object_type
        response = self.api_client.make_rest_call(path='/volume-groups/findByLocation', method="GET", query_params=query_params, model=gen.VolumeGroupView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.VolumeGroupView, raw=raw)

    def related_list(self, filter_uuid: Optional[Any] = None, filter_object_type: Optional[Any] = None, sort: Optional[Any] = None, terse: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Get all volume groups filtered by relation to other entity'
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
        response = self.api_client.make_rest_call(path='/volume-groups/related-list', method="GET", query_params=query_params, model=gen.VolumeGroupView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.VolumeGroupView, raw=raw)

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Delete volume group'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/volume-groups/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.VolumeGroupView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Get volume group by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/volume-groups/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.VolumeGroupView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.VolumeGroupView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.VolumeGroupView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumeGroupView], gen.VolumeGroupView, Any]:
        'Update volume group'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/volume-groups/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.VolumeGroupView,
            raw=raw,
        )
