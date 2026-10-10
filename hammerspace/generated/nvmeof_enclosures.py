"""Spec-generated client for the "nvmeof-enclosures" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedNvmeofEnclosuresClient:
    """Typed coverage for all 6 "nvmeof-enclosures" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NvmeOfEnclosureView], gen.NvmeOfEnclosureView, Any]:
        'List all NVMe-oF enclosures'
        query_params = {}
        response = self.api_client.make_rest_call(path='/nvmeof-enclosures', method="GET", query_params=query_params, model=gen.NvmeOfEnclosureView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.NvmeOfEnclosureView, raw=raw)

    def create(self, dry_run: Optional[Any] = None, connect_all: Optional[Any] = None, body: Optional[gen.NvmeOfEnclosureView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NvmeOfEnclosureView], gen.NvmeOfEnclosureView, Any]:
        "Add an NVMe-oF enclosure. Some form of the Node (DSX) identifier must be supplied in the view's node field (name, uoid, internalId). At least one nvmeOfTarget must be specified"
        query_params = {}
        if dry_run is not None: query_params['dryRun'] = dry_run
        if connect_all is not None: query_params['connectAll'] = connect_all
        return self.api_client.execute_and_monitor_task(
            path='/nvmeof-enclosures',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NvmeOfEnclosureView,
            raw=raw,
        )

    def discover(self, body: Optional[gen.NvmeOfEnclosureView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NvmeOfEnclosureView], gen.NvmeOfEnclosureView, Any]:
        "Query for information about an NVME enclosure. Some form of the Node (DSX) identifier must be supplied in the view's node field (name, uoid, internalId). At least one nvmeOfTarget must be specified"
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/nvmeof-enclosures/discover',
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NvmeOfEnclosureView,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NvmeOfEnclosure], gen.NvmeOfEnclosure, Any]:
        'Delete NVMe-oF enclosure by ID'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/nvmeof-enclosures/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NvmeOfEnclosure,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Get NVMe-oF enclosure by identifier'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/nvmeof-enclosures/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ShareView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareView, raw=raw)

    def update(self, identifier: str, dry_run: Optional[Any] = None, connect_all: Optional[Any] = None, body: Optional[gen.NvmeOfEnclosureView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.NvmeOfEnclosureView], gen.NvmeOfEnclosureView, Any]:
        'Update NvmeOf Enclosure. At least one nvmeOfTarget must be specified'
        query_params = {}
        if dry_run is not None: query_params['dryRun'] = dry_run
        if connect_all is not None: query_params['connectAll'] = connect_all
        return self.api_client.execute_and_monitor_task(
            path=f"/nvmeof-enclosures/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.NvmeOfEnclosureView,
            raw=raw,
        )
