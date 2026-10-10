"""Spec-generated client for the "share-replications" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, Optional
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedShareReplicationsClient:
    """Typed coverage for all 1 "share-replications" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def delete_repl(self, identifier: str, site_id: Optional[Any] = None, site_name: Optional[Any] = None, site_internal_id: Optional[Any] = None, site_address: Optional[Any] = None, site_participant_id: Optional[Any] = None, ignore_remote_failures: Optional[Any] = None, force_master_acquisition: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        "Cause the specified participant to no longer participant in the replicating share. regardless of which participant is specified, that participant's share will be stripped of all other participants, and the share at all other sites will be stripped of the specified participant."
        query_params = {}
        if site_id is not None: query_params['site-id'] = site_id
        if site_name is not None: query_params['site-name'] = site_name
        if site_internal_id is not None: query_params['site-internal-id'] = site_internal_id
        if site_address is not None: query_params['site-address'] = site_address
        if site_participant_id is not None: query_params['site-participant-id'] = site_participant_id
        if ignore_remote_failures is not None: query_params['ignoreRemoteFailures'] = ignore_remote_failures
        if force_master_acquisition is not None: query_params['force-master-acquisition'] = force_master_acquisition
        return self.api_client.execute_and_monitor_task(
            path=f"/share-replications/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
