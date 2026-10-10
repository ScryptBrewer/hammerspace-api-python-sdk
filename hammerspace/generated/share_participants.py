"""Spec-generated client for the "share-participants" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedShareParticipantsClient:
    """Typed coverage for all 7 "share-participants" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareParticipantView], gen.ShareParticipantView, Any]:
        'Get all share participants'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/share-participants', method="GET", query_params=query_params, model=gen.ShareParticipantView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareParticipantView, raw=raw)

    def create(self, body: Optional[gen.ShareParticipantView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Adds a new GFS participant to a share. This creates the share on the new participant, adds all existing participants to that newly-created share, and adds the new participant to the shares at all existing participants'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/share-participants',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def change_admin_state(self, state: Optional[Any] = None, site: Optional[Any] = None, share: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Update adminState for share participants which match criteria'
        query_params = {}
        if state is not None: query_params['state'] = state
        if site is not None: query_params['site'] = site
        if share is not None: query_params['share'] = share
        return self.api_client.execute_and_monitor_task(
            path='/share-participants/change-admin-state',
            method="PUT",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, ignore_remove_failures: Optional[Any] = None, force_master_acquisition: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        "Removes a GFS participant from a share. Regardless of which participant is specified, that participant's share will be stripped of all other participants, and the share at all other sites will be stripped of the specified participant."
        query_params = {}
        if ignore_remove_failures is not None: query_params['ignoreRemoveFailures'] = ignore_remove_failures
        if force_master_acquisition is not None: query_params['forceMasterAcquisition'] = force_master_acquisition
        return self.api_client.execute_and_monitor_task(
            path=f"/share-participants/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareParticipantView], gen.ShareParticipantView, Any]:
        'Get a share participant by ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/share-participants/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ShareParticipantView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareParticipantView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareParticipantView], gen.ShareParticipantView, Any]:
        'Update a share participant'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/share-participants/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareParticipantView,
            raw=raw,
        )

    def delete_share_participants(self, share_identifier: str, site_identifier: str, ignore_remove_failures: Optional[Any] = None, force_master_acquisition: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        "Removes a GFS participant from a share. Regardless of which participant is specified, that participant's share will be stripped of all other participants, and the share at all other sites will be stripped of the specified participant."
        query_params = {}
        if ignore_remove_failures is not None: query_params['ignoreRemoveFailures'] = ignore_remove_failures
        if force_master_acquisition is not None: query_params['forceMasterAcquisition'] = force_master_acquisition
        return self.api_client.execute_and_monitor_task(
            path=f"/share-participants/{_urlquote(share_identifier, safe='')}/{_urlquote(site_identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
