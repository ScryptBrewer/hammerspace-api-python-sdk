"""Spec-generated client for the "identity" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedIdentityClient:
    """Typed coverage for all 1 "identity" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Get identity'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/identity/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.UserView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.UserView, raw=raw)
