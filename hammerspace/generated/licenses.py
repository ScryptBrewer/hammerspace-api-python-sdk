"""Spec-generated client for the "licenses" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedLicensesClient:
    """Typed coverage for all 18 "licenses" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def list(self, spec: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, page_sort: Optional[Any] = None, page_sort_dir: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LicenseActivationView], gen.LicenseActivationView, Any]:
        'Get all licenses'
        query_params = {}
        if spec is not None: query_params['spec'] = spec
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        if page_sort is not None: query_params['page.sort'] = page_sort
        if page_sort_dir is not None: query_params['page.sort.dir'] = page_sort_dir
        response = self.api_client.make_rest_call(path='/licenses', method="GET", query_params=query_params, model=gen.LicenseActivationView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LicenseActivationView, raw=raw)

    def create(self, license_server_username: Optional[Any] = None, license_server_password: Optional[Any] = None, body: Optional[gen.LicenseActivationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Add a license.'
        query_params = {}
        if license_server_username is not None: query_params['license-server-username'] = license_server_username
        if license_server_password is not None: query_params['license-server-password'] = license_server_password
        return self.api_client.execute_and_monitor_task(
            path='/licenses',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def download_offline_add_request(self, body: Optional[gen.LicenseActivationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create a request file for adding a license offline and return it'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/licenses/offline-add-request-download',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def export_offline_add_request(self, export_uri: Optional[Any] = None, body: Optional[gen.LicenseActivationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create a request file for adding a license offline and export it to a location'
        query_params = {}
        if export_uri is not None: query_params['export-uri'] = export_uri
        return self.api_client.execute_and_monitor_task(
            path='/licenses/offline-add-request-export',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def import_offline_add_request(self, activation_id: str, import_uri: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Import and process an offline license add response file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-add-response-import/{_urlquote(activation_id, safe='')}/{_urlquote(import_uri, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def upload_offline_add_request(self, activation_id: str, body: Optional[gen.InputStream] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Upload and process an offline license add response file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-add-response-upload/{_urlquote(activation_id, safe='')}",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def cancel_offline_request(self, activation_id: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Cancel a pending offline license operation'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-cancel-pending/{_urlquote(activation_id, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def download_offline_remove_request(self, activation_id: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create a request file for removing a license offline and return it'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-remove-request-download/{_urlquote(activation_id, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def export_offline_remove_request(self, activation_id: str, export_uri: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create a request file for removing a license offline and export it to a location'
        query_params = {}
        if export_uri is not None: query_params['export-uri'] = export_uri
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-remove-request-export/{_urlquote(activation_id, safe='')}",
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def import_offline_remove_response(self, activation_id: str, import_uri: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Import and process an offline license remove response file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-remove-response-import/{_urlquote(activation_id, safe='')}/{_urlquote(import_uri, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def upload_offline_remove_response(self, activation_id: str, body: Optional[gen.InputStream] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Upload and process an offline license remove response file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-remove-response-upload/{_urlquote(activation_id, safe='')}",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def download_offline_update_request(self, body: Optional[gen.LicenseActivationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create a request file for updating a license offline and return it'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path='/licenses/offline-update-request-download',
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def export_offline_update_request(self, export_uri: Optional[Any] = None, body: Optional[gen.LicenseActivationView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Create a request file for updating a license offline and export it to a location'
        query_params = {}
        if export_uri is not None: query_params['export-uri'] = export_uri
        return self.api_client.execute_and_monitor_task(
            path='/licenses/offline-update-request-export',
            method="POST",
            initial_json_data=body,
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def import_offline_update_response(self, activation_id: str, import_uri: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Import and process an offline license update response file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-update-response-import/{_urlquote(activation_id, safe='')}/{_urlquote(import_uri, safe='')}",
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def upload_offline_update_response(self, activation_id: str, body: Optional[gen.InputStream] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Upload and process an offline license update response file'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/offline-update-response-upload/{_urlquote(activation_id, safe='')}",
            method="POST",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def delete(self, activation_id: str, force: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Remove a license.'
        query_params = {}
        if force is not None: query_params['force'] = force
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/{_urlquote(activation_id, safe='')}",
            method="DELETE",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )

    def get(self, activation_id: str, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.LicenseActivationView], gen.LicenseActivationView, Any]:
        'Get a license by activation ID'
        query_params = {}
        response = self.api_client.make_rest_call(path=f"/licenses/{_urlquote(activation_id, safe='')}", method="GET", query_params=query_params, model=gen.LicenseActivationView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.LicenseActivationView, raw=raw)

    def update(self, activation_id: str, body: Optional[gen.BaseEntityView] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Any:
        'Update a license.'
        query_params = {}
        return self.api_client.execute_and_monitor_task(
            path=f"/licenses/{_urlquote(activation_id, safe='')}",
            method="PUT",
            initial_json_data=body,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds,
            result_model=None if raw else None,
            raw=raw,
        )
