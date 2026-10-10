"""Spec-generated client for the "tasks" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedTasksClient:
    """Typed coverage for all 3 "tasks" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.TaskView], gen.TaskView, Any]:
        'Get all tasks'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/tasks', method="GET", query_params=query_params, model=gen.TaskView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.TaskView, raw=raw)

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.TaskView], gen.TaskView, Any]:
        'Get a task'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/tasks/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.TaskView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.TaskView, raw=raw)

    def update(self, task_id: str, body: Optional[gen.TaskView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.TaskView], gen.TaskView, Any]:
        "Modify a task's status in order to manipulate its lifecycle"
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/tasks/{_urlquote(task_id, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.TaskView,
            raw=raw,
        )
