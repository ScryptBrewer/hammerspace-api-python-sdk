"""Spec-generated client for the "mailsmtp" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedMailsmtpClient:
    """Typed coverage for all 6 "mailsmtp" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmtpView], gen.SmtpView, Any]:
        'Get SMTP'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/mail/smtp', method="GET", query_params=query_params, model=gen.SmtpView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SmtpView, raw=raw)

    def smtp(self, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmtpView], gen.SmtpView, Any]:
        'Configure SMTP'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/mail/smtp',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SmtpView,
            raw=raw,
        )

    def test(self, email: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Test notification'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/mail/smtp/test/{_urlquote(email, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmtpView], gen.SmtpView, Any]:
        'Delete SMTP'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/mail/smtp/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SmtpView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmtpView], gen.SmtpView, Any]:
        'Get SMTP'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/mail/smtp/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.SmtpView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SmtpView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SmtpView], gen.SmtpView, Any]:
        'Update SMTP'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/mail/smtp/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SmtpView,
            raw=raw,
        )
