"""Spec-generated client for the "s3server" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedS3serverClient:
    """Typed coverage for all 10 "s3server" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, reference_view: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Get all S3 servers'
        query_params = {}
        if reference_view is not None: query_params['referenceView'] = reference_view
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/s3server', method="GET", query_params=query_params, model=gen.S3ServerConfigView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.S3ServerConfigView, raw=raw)

    def create(self, validate_only: Optional[Any] = None, body: Optional[gen.S3ServerConfigView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Create new S3 server configuration'
        query_params = {}
        if validate_only is not None: query_params['validate-only'] = validate_only
        return self.api_client.execute_and_monitor_task(
            path='/s3server',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Delete S3 server'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/s3server/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )

    def get(self, identifier: str, with_uncleared_event_severity: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Get S3 server by ID'
        query_params = {}
        if with_uncleared_event_severity is not None: query_params['withUnclearedEventSeverity'] = with_uncleared_event_severity
        response = self.api_client.make_rest_call(path=f"/s3server/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.S3ServerConfigView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.S3ServerConfigView, raw=raw)

    def update(self, identifier: str, validate_only: Optional[Any] = None, delete_bucket_content: Optional[Any] = None, body: Optional[gen.S3ServerConfigView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Update S3 server'
        query_params = {}
        if validate_only is not None: query_params['validate-only'] = validate_only
        if delete_bucket_content is not None: query_params['deleteBucketContent'] = delete_bucket_content
        return self.api_client.execute_and_monitor_task(
            path=f"/s3server/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )

    def delete_bucket(self, identifier: str, bucket_name: Optional[Any] = None, delete_bucket_content: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Remove an S3 bucket from an S3 server'
        query_params = {}
        if bucket_name is not None: query_params['bucketName'] = bucket_name
        if delete_bucket_content is not None: query_params['deleteBucketContent'] = delete_bucket_content
        return self.api_client.execute_and_monitor_task(
            path=f"/s3server/{_urlquote(identifier, safe='')}/bucket",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )

    def bucket(self, identifier: str, body: Optional[gen.S3BucketDescriptorBaseView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Add a bucket or bucket container to an existing S3 server'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/s3server/{_urlquote(identifier, safe='')}/bucket",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )

    def list_buckets(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'GET /s3server/{identifier}/listBuckets'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/s3server/{_urlquote(identifier, safe='')}/listBuckets", method="GET", query_params=query_params, model=gen.S3ServerConfigView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.S3ServerConfigView, raw=raw)

    def delete_s3_user(self, identifier: str, user_name: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Remove an S3 user from an S3 server'
        query_params = {}
        if user_name is not None: query_params['userName'] = user_name
        return self.api_client.execute_and_monitor_task(
            path=f"/s3server/{_urlquote(identifier, safe='')}/user",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )

    def post_user_add(self, identifier: str, body: Optional[gen.S3UserView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.S3ServerConfigView], gen.S3ServerConfigView, Any]:
        'Add an S3 user to an existing S3 server'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/s3server/{_urlquote(identifier, safe='')}/user",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.S3ServerConfigView,
            raw=raw,
        )
