"""Spec-generated client for the "users" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedUsersClient:
    """Typed coverage for all 18 "users" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'List all (non hidden) users'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/users', method="GET", query_params=query_params, model=gen.UserView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.UserView, raw=raw)

    def create(self, body: Optional[gen.UserView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Create new user'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/users',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.UserView,
            raw=raw,
        )

    def get_current(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.BaseUserView], gen.BaseUserView, Any]:
        'Get currently authenticated user'
        query_params = {}
        response = self.api_client.make_rest_call(path='/users/_current', method="GET", query_params=query_params, model=gen.BaseUserView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.BaseUserView, raw=raw)

    def get_permitted_operation(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ApiResourceView], gen.ApiResourceView, Any]:
        'Get permitted operations'
        query_params = {}
        response = self.api_client.make_rest_call(path='/users/_current/permitted-operations', method="GET", query_params=query_params, model=gen.ApiResourceView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ApiResourceView, raw=raw)

    def builtin_group_user_add(self, groupname: str, username: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Add user to a builtin group'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/builtin/user-add/{_urlquote(groupname, safe='')}/{_urlquote(username, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def builtin_group_user_list(self, groupname: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Get list of users of builtin group'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/users/builtin/user-list/{_urlquote(groupname, safe='')}", method="GET", query_params=query_params, raw=raw)
        return self.api_client.read_and_parse_json_body(response, raw=raw)

    def builtin_group_user_remove(self, groupname: str, username: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove user from a builtin group'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/builtin/user-remove/{_urlquote(groupname, safe='')}/{_urlquote(username, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def import_users(self, body: Optional[gen.InputStream] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Import users'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/users/import',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def import_users_import_(self, path_param: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Import users'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/import/{_urlquote(path_param, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Delete user by identifier'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/{_urlquote(identifier, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.UserView,
            raw=raw,
        )

    def get(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Get user by identifier'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/users/{_urlquote(identifier, safe='')}", method="GET", query_params=query_params, model=gen.UserView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.UserView, raw=raw)

    def update(self, identifier: str, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Update user'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/{_urlquote(identifier, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.UserView,
            raw=raw,
        )

    def update_password(self, identifier: str, body: Optional[gen.PasswordView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Update password'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/{_urlquote(identifier, safe='')}/password",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.UserView,
            raw=raw,
        )

    def get_preferences(self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PreferencesView], gen.PreferencesView, Any]:
        'Get user preferences by identifier'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/users/{_urlquote(identifier, safe='')}/preferences", method="GET", query_params=query_params, model=gen.PreferencesView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PreferencesView, raw=raw)

    def delete_preferences(self, identifier: str, preference_key: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Delete user preferences'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/{_urlquote(identifier, safe='')}/preferences/{_urlquote(preference_key, safe='')}",
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get_preferences_preferences(self, identifier: str, preference_key: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.PreferencesView], gen.PreferencesView, Any]:
        'Get user preferences by identifier and preference key'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/users/{_urlquote(identifier, safe='')}/preferences/{_urlquote(preference_key, safe='')}", method="GET", query_params=query_params, model=gen.PreferencesView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.PreferencesView, raw=raw)

    def put_preferences(self, identifier: str, preference_key: str, body: Optional[gen.PreferencesView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Update user preferences'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/{_urlquote(identifier, safe='')}/preferences/{_urlquote(preference_key, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def reset_password(self, identifier: str, body: Optional[gen.PasswordView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.UserView], gen.UserView, Any]:
        'Reset password'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/users/{_urlquote(identifier, safe='')}/reset-password",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else gen.UserView,
            raw=raw,
        )
