# hammerspace/client.py
import requests
import time
import logging
import threading # Added for lock
from typing import Optional, Dict, Any, Union, List, IO

from .ad import AdClient
from .antivirus import AntivirusClient
from .backup import BackupClient
from .base_storage_volumes import BaseStorageVolumesClient
from .cntl import CntlClient
from .data_analytics import DataAnalyticsClient
from .data_copy_to_object import DataCopyToObjectClient
from .data_portals import DataPortalsClient
from .disk_drives import DiskDrivesClient
from .dnss import DnssClient
from .domain_idmaps import DomainIdmapsClient
from .events import EventsClient
from .file_snapshots import FileSnapshotsClient
from .files import FilesClient
from .gateways import GatewaysClient
from .heartbeat import HeartbeatClient
from .i18n import I18nClient
from .identity_group_mappings import IdentityGroupMappingsClient
from .identity import IdentityClient
from .idp import IdpClient
from .kmses import KmsesClient
from .labels import LabelsClient
from .ldaps import LdapsClient
from .license_server import LicenseServerClient
from .licenses import LicensesClient
from .logical_volumes import LogicalVolumesClient
from .login_policy import LoginPolicyClient
from .login import LoginClient # Crucial for login mechanism
from .mailsmtp import MailsmtpClient
from .metrics import MetricsClient
from .modeler import ModelerClient
from .network_interfaces import NetworkInterfacesClient
from .nis import NisClient
from .nodes import NodesClient
from .notification_rules import NotificationRulesClient
from .ntps import NtpsClient
from .object_storage_volumes import ObjectStorageVolumesClient
from .object_store_logical_volumes import ObjectStoreLogicalVolumesClient
from .object_stores import ObjectStoresClient
from .objectives import ObjectivesClient
from .pd_node_cntl import PdNodeCntlClient
from .pd_support import PdSupportClient
from .processor import ProcessorClient
from .reports import ReportsClient
from .roles import RolesClient
from .s3server import S3ServerClient
from .schedules import SchedulesClient
from .share_participants import ShareParticipantsClient
from .share_replications import ShareReplicationsClient
from .share_snapshots import ShareSnapshotsClient
from .shares import SharesClient
from .sites import SitesClient
from .snapshot_retentions import SnapshotRetentionsClient
from .snmp import SnmpClient
from .static_routes import StaticRoutesClient
from .storage_volumes import StorageVolumesClient # File storage volumes
from .subnet_gateways import SubnetGatewaysClient
from .sw_update import SwUpdateClient
from .syslog import SyslogClient
from .system_info import SystemInfoClient
from .system import SystemClient
from .tasks import TasksClient
from .user_groups import UserGroupsClient
from .users import UsersClient
from .versions import VersionsClient
from .volume_groups import VolumeGroupsClient

logger = logging.getLogger(__name__)

class HammerspaceApiClient:
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 60,
        verify_ssl: bool = True
    ):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self._lock = threading.Lock() # For thread-safe re-authentication
        self.is_logged_in_via_cookie = False # Our belief about the session state
        self.auth = None # We will rely on cookies, not basic auth for general calls

        if not verify_ssl:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Initialize all specific resource clients
        self.ad = AdClient(self)
        self.antivirus = AntivirusClient(self)
        self.backup = BackupClient(self)
        self.base_storage_volumes = BaseStorageVolumesClient(self)
        self.cntl = CntlClient(self)
        self.data_analytics = DataAnalyticsClient(self)
        self.data_copy_to_object = DataCopyToObjectClient(self)
        self.data_portals = DataPortalsClient(self)
        self.disk_drives = DiskDrivesClient(self)
        self.dnss = DnssClient(self)
        self.domain_idmaps = DomainIdmapsClient(self)
        self.events = EventsClient(self)
        self.file_snapshots = FileSnapshotsClient(self)
        self.files = FilesClient(self)
        self.gateways = GatewaysClient(self)
        self.heartbeat = HeartbeatClient(self)
        self.i18n = I18nClient(self)
        self.identity_group_mappings = IdentityGroupMappingsClient(self)
        self.identity = IdentityClient(self)
        self.idp = IdpClient(self)
        self.kmses = KmsesClient(self)
        self.labels = LabelsClient(self)
        self.ldaps = LdapsClient(self)
        self.license_server = LicenseServerClient(self)
        self.licenses = LicensesClient(self)
        self.logical_volumes = LogicalVolumesClient(self)
        self.login_policy = LoginPolicyClient(self)
        self.login = LoginClient(self) # LoginClient gets this API client instance
        self.mailsmtp = MailsmtpClient(self)
        self.metrics = MetricsClient(self)
        self.modeler = ModelerClient(self)
        self.network_interfaces = NetworkInterfacesClient(self)
        self.nis = NisClient(self)
        self.nodes = NodesClient(self)
        self.notification_rules = NotificationRulesClient(self)
        self.ntps = NtpsClient(self)
        self.object_storage_volumes = ObjectStorageVolumesClient(self)
        self.object_store_logical_volumes = ObjectStoreLogicalVolumesClient(self)
        self.object_stores = ObjectStoresClient(self)
        self.objectives = ObjectivesClient(self)
        self.pd_node_cntl = PdNodeCntlClient(self)
        self.pd_support = PdSupportClient(self)
        self.processor = ProcessorClient(self)
        self.reports = ReportsClient(self)
        self.roles = RolesClient(self)
        self.s3server = S3ServerClient(self)
        self.schedules = SchedulesClient(self)
        self.share_participants = ShareParticipantsClient(self)
        self.share_replications = ShareReplicationsClient(self)
        self.share_snapshots = ShareSnapshotsClient(self)
        self.shares = SharesClient(self)
        self.sites = SitesClient(self)
        self.snapshot_retentions = SnapshotRetentionsClient(self)
        self.snmp = SnmpClient(self)
        self.static_routes = StaticRoutesClient(self)
        self.storage_volumes = StorageVolumesClient(self)
        self.subnet_gateways = SubnetGatewaysClient(self)
        self.sw_update = SwUpdateClient(self)
        self.syslog = SyslogClient(self)
        self.system_info = SystemInfoClient(self)
        self.system = SystemClient(self)
        self.tasks = TasksClient(self)
        self.user_groups = UserGroupsClient(self)
        self.users = UsersClient(self)
        self.versions = VersionsClient(self)
        self.volume_groups = VolumeGroupsClient(self)

        # Attempt initial login if credentials are provided
        if self.username and self.password:
            try:
                self._perform_login_action()
            except Exception as e:
                logger.warning(
                    f"Initial login attempt during client init failed: {e}. "
                    "Will attempt lazily if needed."
                )
        logger.info(f"HammerspaceApiClient initialized for {self.base_url} with all clients.")

    def _perform_login_action(self):
        """
        Performs the login action using the LoginClient.
        This method is synchronized with a lock.
        It updates self.is_logged_in_via_cookie and raises exceptions on failure.
        """
        if not (self.username and self.password):
            logger.debug("Login action skipped: username or password not configured.")
            return

        with self._lock: # Ensure only one thread attempts login at a time
            # Check again inside the lock in case another thread just logged in
            if self.is_logged_in_via_cookie:
                logger.debug("Already logged in (checked within lock). Skipping login action.")
                return

            logger.info(f"Attempting login for user '{self.username}'...")
            try:
                # LoginClient.login_user is responsible for making the actual /login API call.
                # It MUST pass is_login=True to its internal call to self.make_rest_call.
                # Assumes LoginClient has a method like:
                # def login_user(self, username, password):
                #    payload = {"username": username, "password": password}
                #    self.client.make_rest_call("login", method="POST", json_data=payload, is_login=True)
                self.login.login_user(self.username, self.password)
                self.is_logged_in_via_cookie = True
                logger.info("Login action successful. Session cookie should be active.")
            except Exception as e: # Catch whatever self.login.login_user might raise
                self.is_logged_in_via_cookie = False
                logger.error(f"Login action failed: {e}")
                raise # Re-raise the original exception from login_user

    def make_rest_call(
        self,
        path: str,
        method: str = "GET",
        json_data: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, IO]] = None,
        stream: bool = False,
        data: Optional[Dict[str, Any]] = None,
        is_login: bool = False, # True if this call IS the login attempt
        is_absolute_url: bool = False,
        custom_headers: Optional[Dict[str, str]] = None,
        _is_retry_after_relogin: bool = False # Internal flag
    ) -> requests.Response:
        """
        Makes a REST API call. Handles session expiration and re-login.
        'path' can be a relative path or a full URL if is_absolute_url is True.
        """
        # Lazy login: if credentials exist, not a login call itself, not a retry, and we don't think we're logged in
        if self.username and self.password and \
           not is_login and \
           not _is_retry_after_relogin and \
           not self.is_logged_in_via_cookie:
            logger.info("Not logged in (or session assumed invalid) and credentials available. Attempting login before API call.")
            try:
                self._perform_login_action()
            except Exception as login_err:
                logger.error(f"Pre-call login attempt failed: {login_err}. Cannot proceed with the original request {method} {path}.")
                raise login_err

        if is_absolute_url:
            url = path
        else:
            url = f"{self.base_url}{path.lstrip('/')}"
        
        request_headers = {}
        request_headers["Accept"] = "application/json"
        if json_data and not files and not data:
            request_headers["Content-Type"] = "application/json"
        
        if custom_headers:
            request_headers.update(custom_headers)

        logger.debug(
            f"Request: {method} {url} Params: {query_params} JSON: {json_data is not None} "
            f"Data: {data is not None} Files: {files is not None} Headers: {request_headers} "
            f"IsLoginCall: {is_login} IsRetry: {_is_retry_after_relogin}"
        )

        try:
            response = self.session.request(
                method, url,
                json=json_data if not files and not data else None,
                data=data if not files and not json_data else None,
                params=query_params, 
                auth=None, # We rely on session cookies
                timeout=self.timeout,
                verify=self.verify_ssl, headers=request_headers, files=files, stream=stream
            )

            log_msg_prefix = f"Response: {method} {url} - Status: {response.status_code}"
            if not stream and response.content:
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith(('application/json', 'text/')):
                    body_preview = response.text[:500] + ('...' if len(response.text) > 500 else '')
                    logger.debug(f"{log_msg_prefix} - Body: {body_preview}")
                elif content_type:
                    logger.debug(f"{log_msg_prefix} - Body: Non-text content type '{content_type}', Length: {len(response.content)}")
                else: # No content-type or binary
                    logger.debug(f"{log_msg_prefix} - Body: Binary content, Length: {len(response.content)}")

            else: # Stream or no content
                logger.debug(log_msg_prefix)

            response.raise_for_status()
            # If the call succeeded, and we are managing auth, update our belief
            if self.username and self.password and not is_login:
                 self.is_logged_in_via_cookie = True
            return response
        except requests.exceptions.HTTPError as e:
            if (e.response.status_code == 401 and
                    not is_login and
                    not _is_retry_after_relogin and
                    self.username and self.password):
                
                logger.warning(
                    f"HTTP 401 on {method} {url}. Session likely expired or invalid. "
                    "Attempting re-login."
                )
                self.is_logged_in_via_cookie = False 
                try:
                    self._perform_login_action() 
                    logger.info("Re-login successful. Retrying original request.")
                    return self.make_rest_call(
                        path, method, json_data, query_params, files, stream, data,
                        is_login=False, 
                        is_absolute_url=is_absolute_url,
                        custom_headers=custom_headers,
                        _is_retry_after_relogin=True
                    )
                except Exception as relogin_exc: 
                    logger.error(
                        f"Re-login attempt failed: {relogin_exc}. "
                        "The original request will fail with the 401 error."
                    )
            
            # --- REFINED ERROR LOGGING STARTS HERE ---
            err_status = e.response.status_code
            err_reason = e.response.reason
            concise_err_msg = f"HTTP error: {err_status} {err_reason} for {method} {url}."
            
            # Attempt to parse more specific details if available
            try:
                if e.response.headers.get('Content-Type', '').startswith('application/json'):
                    err_details_list = e.response.json()
                    # Assuming the error details are a list of dicts as per your example
                    if isinstance(err_details_list, list) and err_details_list:
                        first_error = err_details_list[0]
                        error_code = first_error.get('errorCode')
                        error_args = first_error.get('args')
                        error_message_key = first_error.get('message') # e.g., VALIDATION_VIOLATION

                        if error_code is not None: # Check if error_code was found
                            concise_err_msg += (
                                f" API Error Code: {error_code}."
                            )
                        if error_message_key:
                             concise_err_msg += (
                                f" Message: '{error_message_key}'."
                             )
                        if error_args:
                            concise_err_msg += (
                                f" Args: {error_args}."
                            )
                        
                        # For DEBUG level, log the full details including stack
                        logger.debug(
                            f"Full HTTP error details for {method} {url}: {err_details_list}"
                        )
                    else: # JSON, but not the expected list structure
                        logger.debug(
                            f"Unexpected JSON error structure for {method} {url}: {err_details_list}"
                        )
                        concise_err_msg += f" Details: {str(err_details_list)[:200]}"
                else: # Not JSON
                    response_text_preview = e.response.text[:200]
                    concise_err_msg += f" Response: {response_text_preview}"
                    logger.debug(
                        f"Full non-JSON error response for {method} {url}: {e.response.text[:1000]}"
                    )
            except ValueError: # JSONDecodeError
                response_text_preview = e.response.text[:200]
                concise_err_msg += f" Response (not valid JSON): {response_text_preview}"
                logger.debug(
                    f"Full invalid JSON error response for {method} {url}: {e.response.text[:1000]}"
                )
            except Exception as parse_exc: # Catch any other parsing error
                logger.debug(f"Error parsing error response details: {parse_exc}")
                concise_err_msg += " Could not parse detailed error response."

            # Log the concise message at ERROR level
            logger.error(concise_err_msg)
            # --- REFINED ERROR LOGGING ENDS HERE ---
            
            if e.response.status_code == 401:
                self.is_logged_in_via_cookie = False
            
            raise # Re-raise the original requests.exceptions.HTTPError
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {method} {url}: {e}")
  

    def read_and_parse_json_body(self, response: requests.Response) -> Optional[Union[Dict[str, Any], List[Any]]]:
        if response.status_code == 204: return None
        if not response.content: return None # No content to parse
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('application/json'):
            logger.warning(f"Response content type is '{content_type}', not 'application/json'. Body: {response.text[:200]}")
            # Depending on strictness, you might want to return None or raise an error here
            # For now, we'll still try to parse, as some APIs might not set content-type correctly.
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e: # More specific exception
            logger.error(f"Failed to parse JSON response: {e} - Response text: {response.text[:500]}")
            return None # Or raise an error if strict parsing is required

    def execute_and_monitor_task(
        self,
        path: str,
        method: str = "POST",
        initial_json_data: Optional[Dict[str, Any]] = None,
        initial_query_params: Optional[Dict[str, Any]] = None,
        initial_headers: Optional[Dict[str, str]] = None,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        poll_interval_seconds: int = 5
    ) -> Union[Optional[str], Optional[Dict[str, Any]], Optional[List[Any]]]:
        """
        Executes an API call. If a 202 Accepted is received with a Location header,
        it monitors the task at that Location. Otherwise, handles synchronous responses.
        """
        try:
            initial_response = self.make_rest_call(
                path,
                method=method,
                json_data=initial_json_data,
                query_params=initial_query_params,
                custom_headers=initial_headers # Pass through custom headers
            )
        except requests.exceptions.RequestException as e: # Catch potential login or other request errors
            logger.error(f"Initial API call failed for {method} {path} during task execution: {e}. Cannot monitor task.")
            # Let the user know by re-raising or returning a specific failure indicator
            raise # Or return a dict like {"error": str(e), "status": "initial_call_failed"}

        initial_response_data = self.read_and_parse_json_body(initial_response)

        if not monitor_task:
            logger.debug("Task monitoring disabled. Returning initial response data.")
            return initial_response_data

        if initial_response.status_code in [200, 201]: # Synchronous success
            logger.info(f"Synchronous success ({initial_response.status_code}). Returning initial response data.")
            return initial_response_data

        if initial_response.status_code == 202: # Task initiated
            location_url = initial_response.headers.get('Location')
            if not location_url:
                logger.warning("Received 202 Accepted, but no 'Location' header found. Cannot monitor task.")
                logger.debug(f"Initial response headers: {initial_response.headers}")
                return initial_response_data if initial_response_data else {"status": "accepted_no_location"}

            logger.info(f"Task initiated (202 Accepted). Monitoring Location URL: {location_url}")
            start_time = time.time()
            last_known_status_data = None # To store the last successfully fetched task status

            while (time.time() - start_time) < task_timeout_seconds:
                logger.debug(f"Polling task status at: {location_url}")
                try:
                    # Polling calls will also benefit from re-authentication if session expires
                    task_status_response = self.make_rest_call(
                        path=location_url,
                        method="GET",
                        is_absolute_url=True
                    )
                    current_task_data = self.read_and_parse_json_body(task_status_response)
                    last_known_status_data = current_task_data # Update last known status
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Polling request failed for {location_url}: {e}. Retrying in {poll_interval_seconds}s...")
                    time.sleep(poll_interval_seconds)
                    continue # Retry polling

                if current_task_data and isinstance(current_task_data, dict):
                    task_state = current_task_data.get('state', current_task_data.get('status', '')).upper()
                    if not task_state: # Fallback for different status key names
                        task_state = current_task_data.get('statusMessage', '').upper()
                    
                    progress = current_task_data.get("progressPercent", "N/A")
                    logger.info(f"Task at {location_url} - State: {task_state}, Progress: {progress}%")

                    if task_state == "COMPLETED":
                        logger.info(f"Task at {location_url} completed successfully.")
                        # Extract result, potentially nested
                        result_data = current_task_data.get("result", current_task_data)
                        if isinstance(result_data, dict):
                            entity_uuid = result_data.get('uuid')
                            # Attempt to find UUID in ctxMap if not directly in result
                            if not entity_uuid and result_data.get('ctxMap') and isinstance(result_data['ctxMap'], dict):
                                entity_uoid_val = result_data['ctxMap'].get('entity-uoid')
                                if isinstance(entity_uoid_val, dict) and entity_uoid_val.get('uuid'):
                                    entity_uuid = entity_uoid_val['uuid']
                                elif isinstance(entity_uoid_val, str) and "uuid=" in entity_uoid_val:
                                    try: # Robust parsing for "uuid=value" format
                                        entity_uuid = entity_uoid_val.split("uuid=")[1].split(",")[0].split("]")[0].strip()
                                    except IndexError: pass # Parsing failed, uuid remains None
                            
                            if entity_uuid:
                                logger.info(f"Task completed, extracted entity UUID: {entity_uuid}")
                        return result_data # Return the result part or the whole task data
                    
                    elif task_state in ["FAILED", "CANCELLED", "TIMED_OUT"]:
                        error_message = current_task_data.get("errorMessage", "Task failed, was cancelled, or timed out.")
                        logger.error(f"Task at {location_url} ended. State: {task_state}. Message: {error_message}")
                        return current_task_data # Return the full task data indicating failure
                else:
                    logger.warning(f"Task data not found or not a dictionary while polling {location_url}. Retrying in {poll_interval_seconds}s...")
                
                time.sleep(poll_interval_seconds)

            logger.warning(f"Task monitoring for {location_url} timed out after {task_timeout_seconds} seconds.")
            return last_known_status_data # Return the last known status on timeout

        # Fallback for unexpected status codes from initial call
        logger.warning(f"Initial call returned status {initial_response.status_code} which is not a standard success or task initiation. Response: {initial_response_data}")
        return initial_response_data
