"""Spec-generated client for the "shares" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedSharesClient:
    """Typed coverage for all 19 "shares" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Get all shares'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/shares', method="GET", query_params=query_params, model=gen.ShareView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareView, raw=raw)

    def create(self, create_path: Optional[Any] = None, override_mem_check: Optional[Any] = None, validate_only: Optional[Any] = None, body: Optional[gen.ShareView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Create share'
        query_params = {}
        if create_path is not None: query_params['create-path'] = create_path
        if override_mem_check is not None: query_params['override-mem-check'] = override_mem_check
        if validate_only is not None: query_params['validate-only'] = validate_only
        return self.api_client.execute_and_monitor_task(
            path='/shares',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareView,
            raw=raw,
        )

    def related_list(self, filter_uuid: Optional[Any] = None, filter_object_type: Optional[Any] = None, sort: Optional[Any] = None, terse: Optional[Any] = None, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Get all shares filtered by relation to other entity'
        query_params = {}
        if filter_uuid is not None: query_params['filterUuid'] = filter_uuid
        if filter_object_type is not None: query_params['filterObjectType'] = filter_object_type
        if sort is not None: query_params['sort'] = sort
        if terse is not None: query_params['terse'] = terse
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/shares/related-list', method="GET", query_params=query_params, model=gen.ShareView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareView, raw=raw)

    def list_uuids(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'List uuids for all shares'
        query_params = {}
        response = self.api_client.make_rest_call(path='/shares/uuid-list', method="GET", query_params=query_params, model=gen.ShareView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareView, raw=raw)

    def delete(self, identifier: str, delete_delay: Optional[Any] = None, delete_path: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Delete share'
        query_params = {}
        if delete_delay is not None: query_params['delete-delay'] = delete_delay
        if delete_path is not None: query_params['delete-path'] = delete_path
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareView,
            raw=raw,
        )

    def get(self, identifier: str, with_uncleared_event_severity: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Get share by ID'
        query_params = {}
        if with_uncleared_event_severity is not None: query_params['withUnclearedEventSeverity'] = with_uncleared_event_severity
        response = self.api_client.make_rest_call(path=f"/shares/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.ShareView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ShareView, raw=raw)

    def update(self, identifier: str, validate_only: Optional[Any] = None, body: Optional[gen.ShareView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Update share'
        query_params = {}
        if validate_only is not None: query_params['validate-only'] = validate_only
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareView,
            raw=raw,
        )

    def remove_item_attribute(self, identifier: str, path_param: Optional[Any] = None, name: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove attribute from share root inode, or path within share'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        if name is not None: query_params['name'] = name
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/attribute",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def list_item_attributes(self, identifier: str, path_param: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Get attributes of share root inode, or path within share'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        response = self.api_client.make_rest_call(path=f"/shares/{_urlquote(identifier, safe='')}/attribute", method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def set_item_attribute(self, identifier: str, path_param: Optional[Any] = None, body: Optional[gen.HsItemAttributeView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Set attribute share root inode, or path within share'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/attribute",
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get_collection_sum(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.JsonSerializable], gen.JsonSerializable, Any]:
        'Get collection sums json for the share'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/shares/{_urlquote(identifier, safe='')}/collection-sum", method="GET", query_params=query_params, model=gen.JsonSerializable, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.JsonSerializable, raw=raw)

    def mount_details(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.MountDetailsView], gen.MountDetailsView, Any]:
        'Provide share mounting details'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/shares/{_urlquote(identifier, safe='')}/mount-details", method="GET", query_params=query_params, model=gen.MountDetailsView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.MountDetailsView, raw=raw)

    def move(self, identifier: str, path_param: str, create_path: Optional[Any] = None, validate_only: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Move share'
        query_params = {}
        if create_path is not None: query_params['create-path'] = create_path
        if validate_only is not None: query_params['validate-only'] = validate_only
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/move/{_urlquote(path_param, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareView,
            raw=raw,
        )

    def objective_list(self, identifier: str, path_param: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SharePathObjectivesView], gen.SharePathObjectivesView, Any]:
        'Read objective(s) set on share (and optionally a path within the share)'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        response = self.api_client.make_rest_call(path=f"/shares/{_urlquote(identifier, safe='')}/objective-list", method="GET", query_params=query_params, model=gen.SharePathObjectivesView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.SharePathObjectivesView, raw=raw)

    def reset_objectives(self, identifier: str, path_param: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SharePathObjectivesView], gen.SharePathObjectivesView, Any]:
        'Reset objectives on share (when path is omitted), or path within share to their defaults'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/objective-reset",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SharePathObjectivesView,
            raw=raw,
        )

    def add_objective(self, identifier: str, path_param: Optional[Any] = None, objective_identifier: Optional[Any] = None, applicability: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SharePathObjectivesView], gen.SharePathObjectivesView, Any]:
        'Set objective on share (when path is omitted), or path within share'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        if objective_identifier is not None: query_params['objective-identifier'] = objective_identifier
        if applicability is not None: query_params['applicability'] = applicability
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/objective-set",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SharePathObjectivesView,
            raw=raw,
        )

    def remove_objective(self, identifier: str, path_param: Optional[Any] = None, objective_identifier: Optional[Any] = None, applicability: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SharePathObjectivesView], gen.SharePathObjectivesView, Any]:
        'Unset objective on share (when path is omitted), or path within share. Note that when this is called with an objective which is inherited & not applied locally, the effect will be that the objective will be added locally with an applicability that negates the inherited applicability.'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        if objective_identifier is not None: query_params['objective-identifier'] = objective_identifier
        if applicability is not None: query_params['applicability'] = applicability
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/objective-unset",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SharePathObjectivesView,
            raw=raw,
        )

    def update_objective(self, identifier: str, path_param: Optional[Any] = None, objective_identifier: Optional[Any] = None, applicability: Optional[Any] = None, new_applicability: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.SharePathObjectivesView], gen.SharePathObjectivesView, Any]:
        'Update the applicability of an objective on share (when path is omitted), or path within share'
        query_params = {}
        if path_param is not None: query_params['path'] = path_param
        if objective_identifier is not None: query_params['objective-identifier'] = objective_identifier
        if applicability is not None: query_params['applicability'] = applicability
        if new_applicability is not None: query_params['new-applicability'] = new_applicability
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/objective-update",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.SharePathObjectivesView,
            raw=raw,
        )

    def undelete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ShareView], gen.ShareView, Any]:
        'Un-delete share'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/shares/{_urlquote(identifier, safe='')}/undelete",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.ShareView,
            raw=raw,
        )
