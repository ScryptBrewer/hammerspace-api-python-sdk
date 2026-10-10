"""Spec-generated client for the "metrics" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedMetricsClient:
    """Typed coverage for all 3 "metrics" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, start: Optional[Any] = None, end: Optional[Any] = None, func: Optional[Any] = None, limit: Optional[Any] = None, group_by: Optional[Any] = None, object_type: Optional[Any] = None, name: Optional[Any] = None, uuid: Optional[Any] = None, field: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Query metrics through custom API'
        query_params = {}
        if start is not None: query_params['start'] = start
        if end is not None: query_params['end'] = end
        if func is not None: query_params['func'] = func
        if limit is not None: query_params['limit'] = limit
        if group_by is not None: query_params['groupBy'] = group_by
        if object_type is not None: query_params['objectType'] = object_type
        if name is not None: query_params['name'] = name
        if uuid is not None: query_params['uuid'] = uuid
        if field is not None: query_params['field'] = field
        response = self.api_client.make_rest_call(path='/metrics', method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def get_capacity_metrics(self, object_type: str, object_uuid: str, preceding_duration: Optional[Any] = None, interval_duration: Optional[Any] = None, include_managed_data_usage: Optional[Any] = None, fill_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StatsResultView], gen.StatsResultView, Any]:
        'Query influxDB for capacity metrics data'
        query_params = {}
        if preceding_duration is not None: query_params['precedingDuration'] = preceding_duration
        if interval_duration is not None: query_params['intervalDuration'] = interval_duration
        if include_managed_data_usage is not None: query_params['includeManagedDataUsage'] = include_managed_data_usage
        if fill_type is not None: query_params['fillType'] = fill_type
        response = self.api_client.make_rest_call(path=f"/metrics/capacity/{_urlquote(object_type, safe='')}/{_urlquote(object_uuid, safe='')}", method="GET", query_params=query_params, model=gen.StatsResultView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StatsResultView, raw=raw)

    def list_metrics(self, q: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Query metrics through native InfluxDB API'
        query_params = {}
        if q is not None: query_params['q'] = q
        response = self.api_client.make_rest_call(path='/metrics/native', method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)
