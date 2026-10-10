"""Spec-generated client for the "i18n" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedI18nClient:
    """Typed coverage for all 2 "i18n" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'List messages in resource bundle'
        query_params = {}
        response = self.api_client.make_rest_call(path='/i18n', method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def get(self, locale_name: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'List messages in resource bundle by locale'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/i18n/{_urlquote(locale_name, safe='')}", method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)
