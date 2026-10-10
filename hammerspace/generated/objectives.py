"""Spec-generated client for the "objectives" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedObjectivesClient:
    """Typed coverage for all 9 "objectives" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, hide_tech_preview: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Get all objectives'
        query_params = {}
        if hide_tech_preview is not None: query_params['hideTechPreview'] = hide_tech_preview
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/objectives', method="GET", query_params=query_params, model=gen.ObjectiveView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectiveView, raw=raw)

    def create(self, body: Optional[gen.ObjectiveView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Create objective'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/objectives',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectiveView,
            raw=raw,
        )

    def export_objectives(self, uuid: Optional[Any] = None, name: Optional[Any] = None, target: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Export objectives'
        query_params = {}
        if uuid is not None: query_params['uuid'] = uuid
        if name is not None: query_params['name'] = name
        if target is not None: query_params['target'] = target
        return self.api_client.execute_and_monitor_task(
            path='/objectives/export',
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectiveView,
            raw=raw,
        )

    def find_matching_volumes(self, body: Optional[gen.ObjectiveView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Find matching volumes'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/objectives/findMatchingVolumes',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectiveView,
            raw=raw,
        )

    def import_objectives(self, source: Optional[Any] = None, name: Optional[Any] = None, prefix: Optional[Any] = None, merge: Optional[Any] = None, insecure: Optional[Any] = None, body: Optional[gen.ObjectiveView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Import objectives'
        query_params = {}
        if source is not None: query_params['source'] = source
        if name is not None: query_params['name'] = name
        if prefix is not None: query_params['prefix'] = prefix
        if merge is not None: query_params['merge'] = merge
        if insecure is not None: query_params['insecure'] = insecure
        return self.api_client.execute_and_monitor_task(
            path='/objectives/import',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def validate(self, exp: str, hide_tech_preview: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.HammerscriptResponseView], gen.HammerscriptResponseView, Any]:
        'Validate expression'
        query_params = {}
        if hide_tech_preview is not None: query_params['hideTechPreview'] = hide_tech_preview
        response = self.api_client.make_rest_call(path=f"/objectives/validate/{_urlquote(exp, safe='')}", method="GET", query_params=query_params, model=gen.HammerscriptResponseView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.HammerscriptResponseView, raw=raw)

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Delete objective'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/objectives/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectiveView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Get objective by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/objectives/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ObjectiveView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectiveView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectiveView], gen.ObjectiveView, Any]:
        'Update objective'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/objectives/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ObjectiveView,
            raw=raw,
        )
