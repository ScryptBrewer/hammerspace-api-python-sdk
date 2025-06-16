# hammerspace/licenses.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class LicensesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        activation_id: Optional[str] = None, # Path parameter for specific get
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all licenses or a specific one by its activation ID.

        If 'activation_id' is provided, fetches a single license.
        (Corresponds to GET /licenses/{activation-id} - OpId: getLicenseByActivationId)

        Otherwise, lists all licenses.
        (Corresponds to GET /licenses - OpId: listLicenses)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /licenses/{activation-id} has no query params in spec
        if activation_id:
            path = f"/licenses/{activation_id}"
            logger.info(f"Getting license by activation ID: {activation_id}")
        else:
            path = "/licenses"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all licenses with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_license(
        self, license_data: Dict[str, Any], # requestBody
        monitor_task: bool = True, task_timeout_seconds: int = 180,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add a license. (POST /licenses) - OpId: createLicense
        license_data: The main request body.
        Optional kwargs:
            license_server_username (str): (API query param: license-server-username)
            license_server_password (str): (API query param: license-server-password)
        """
        path = "/licenses"
        query_params = {}
        if "license_server_username" in kwargs:
            query_params["license-server-username"] = kwargs["license_server_username"]
        if "license_server_password" in kwargs:
            query_params["license-server-password"] = kwargs["license_server_password"]
        
        logger.info(f"Creating license. Body: {license_data}, Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=license_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    # --- Offline License Operations ---
    # These will need careful implementation of kwargs if they have optional query params.
    # Also, consider how to handle file uploads/downloads if not just async tasks.
    # Example for one, apply pattern to others:
    def download_licenses_offline_add_request(
        self, license_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 180, **kwargs
    ) -> Union[Optional[str], Any]:
        """
        Create a request file for adding a license offline and return it.
        (POST /licenses/offline-add-request-download) - OpId: downloadLicensesOfflineAddRequest
        license_data: The main request body.
        **kwargs: Any optional query parameters for this endpoint (if any).
        """
        path = "/licenses/offline-add-request-download"
        query_params = {} # Check spec for actual query params
        # if "some_query_param" in kwargs: query_params["someQueryParam"] = kwargs["some_query_param"]
        logger.warning(f"Downloading offline add request. Body: {license_data}, Query: {query_params}. Response may be a file stream.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=license_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
    # ... (Implement other offline methods: export_*, import_*, upload_*, cancel_*, etc.)
    # For upload methods (multipart/form-data), you'll need to adapt make_rest_call or call requests.request directly.

    def update_license_by_activation_id(
        self, activation_id: str, license_update_data: Dict[str, Any],
        monitor_task: bool = True, task_timeout_seconds: int = 180
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update a license. (PUT /licenses/{activation-id}) - OpId: updateLicenseByActivationId"""
        path = f"/licenses/{activation_id}"
        logger.info(f"Updating license '{activation_id}'. Body: {license_update_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=license_update_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_license_by_activation_id(
        self, activation_id: str, monitor_task: bool = True, task_timeout_seconds: int = 180, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Remove a license. (DELETE /licenses/{activation-id}) - OpId: deleteLicenseByActivationId
        Optional kwargs:
            force (bool): (API query param: force)
        """
        path = f"/licenses/{activation_id}"
        query_params = {}
        if "force" in kwargs:
            query_params["force"] = str(kwargs["force"]).lower()
        logger.info(f"Deleting license '{activation_id}'. Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )