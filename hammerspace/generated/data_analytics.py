"""Spec-generated client for the "data-analytics" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union

from hammerspace.models import generated as gen


class GeneratedDataAnalyticsClient:
    """Typed coverage for all 1 "data-analytics" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, start: Optional[Any] = None, end: Optional[Any] = None, path_param: Optional[Any] = None, field: Optional[Any] = None, func: Optional[Any] = None, group_by: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query data-analytics'
        query_params = {}
        if start is not None: query_params['start'] = start
        if end is not None: query_params['end'] = end
        if path_param is not None: query_params['path'] = path_param
        if field is not None: query_params['field'] = field
        if func is not None: query_params['func'] = func
        if group_by is not None: query_params['groupBy'] = group_by
        response = self.api_client.make_rest_call(path='/data-analytics', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)
