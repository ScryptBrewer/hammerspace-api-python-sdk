# hammerspace/client.py
import requests
import time
import logging
import threading
from typing import Optional, Dict, Any, Union, List, IO
from contextlib import contextmanager
from collections import defaultdict
from .exceptions import (
    HammerspaceApiError, AuthenticationError, AuthorizationError, 
    ResourceNotFoundError, ValidationError, RateLimitError, ServerError,
    ConnectionError, ConfigurationError, RetryExhaustedError
)
from .logging_config import MetricsCollector

logger = logging.getLogger(__name__)

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
from .login import LoginClient
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
from .storage_volumes import StorageVolumesClient
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
        verify_ssl: bool = True,
        max_retries: int = 3,
        retry_backoff_factor: float = 0.5,
        max_connections: int = 10,
        rate_limit_per_second: int = 100,
        enable_caching: bool = True,
        cache_ttl: int = 300
    ):
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.max_retries = max_retries
        self.retry_backoff_factor = retry_backoff_factor
        
        # Connection pooling configuration
        self.max_connections = max_connections
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=max_connections,
            pool_maxsize=max_connections,
            max_retries=0  # We handle retries ourselves
        )
        self.session = requests.Session()
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # Rate limiting
        self.rate_limit_per_second = rate_limit_per_second
        self._rate_limit_lock = threading.Lock()
        self._request_times = []
        
        # Simple caching
        self.enable_caching = enable_caching
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_lock = threading.Lock()
        
        # Metrics collection
        self.metrics = MetricsCollector()
        
        # Authentication state
        self._lock = threading.Lock()
        self.is_logged_in_via_cookie = False
        self.auth = None

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
        self.login = LoginClient(self)
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

    def _check_rate_limit(self):
        """Check and enforce rate limiting."""
        if self.rate_limit_per_second <= 0:
            return  # No rate limiting
            
        current_time = time.time()
        with self._rate_limit_lock:
            # Remove requests older than 1 second
            self._request_times = [req_time for req_time in self._request_times 
                                   if current_time - req_time < 1.0]
            
            # Check if we need to wait
            if len(self._request_times) >= self.rate_limit_per_second:
                sleep_time = 1.0 - (current_time - self._request_times[0])
                if sleep_time > 0:
                    logger.debug(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                    # Clean up after sleep
                    self._request_times = [req_time for req_time in self._request_times 
                                           if time.time() - req_time < 1.0]
            
            # Record this request
            self._request_times.append(time.time())

    def _get_cache_key(self, path: str, method: str, params: Optional[Dict] = None) -> str:
        """Generate a cache key for the request."""
        key = f"{method}:{path}"
        if params:
            # Sort params for consistent keys
            sorted_params = sorted(params.items())
            key += f":{sorted_params}"
        return key

    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get response from cache if available and not expired."""
        if not self.enable_caching:
            return None
            
        with self._cache_lock:
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self.cache_ttl:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_data
                else:
                    logger.debug(f"Cache expired for {cache_key}")
                    del self._cache[cache_key]
        return None

    def _set_cache(self, cache_key: str, data: Any):
        """Store data in cache."""
        if not self.enable_caching:
            return
            
        with self._cache_lock:
            self._cache[cache_key] = (data, time.time())
            logger.debug(f"Cached response for {cache_key}")

    def clear_cache(self):
        """Clear the entire cache."""
        with self._cache_lock:
            self._cache.clear()
        logger.info("Cache cleared")

    @contextmanager
    def session_context(self):
        """Context manager for the client session."""
        try:
            yield self.session
        finally:
            # Cleanup if needed
            pass

    def close(self):
        """Close the session and cleanup resources."""
        self.session.close()
        self.clear_cache()
        logger.info("HammerspaceApiClient closed")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current API usage metrics."""
        return self.metrics.get_metrics()
    
    def reset_metrics(self):
        """Reset all metrics."""
        self.metrics.reset_metrics()
        logger.info("Metrics reset")

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

    def make_rest_call_with_retry(
        self,
        path: str,
        method: str = "GET",
        json_data: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, IO]] = None,
        stream: bool = False,
        data: Optional[Dict[str, Any]] = None,
        is_login: bool = False,
        is_absolute_url: bool = False,
        custom_headers: Optional[Dict[str, str]] = None,
        _is_retry_after_relogin: bool = False
    ) -> requests.Response:
        """
        Makes a REST API call with retry logic for transient failures.
        """
        last_exception = None
        retryable_exceptions = (ConnectionError, requests.exceptions.Timeout, requests.exceptions.ConnectionError)
        
        for attempt in range(self.max_retries):
            try:
                return self.make_rest_call(
                    path, method, json_data, query_params, files, stream, data,
                    is_login, is_absolute_url, custom_headers, _is_retry_after_relogin
                )
            except retryable_exceptions as e:
                last_exception = e
                if attempt < self.max_retries - 1:  # Don't sleep on the last attempt
                    wait_time = self.retry_backoff_factor * (2 ** attempt)
                    logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                                 f"Retrying in {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All retry attempts exhausted for {method} {path}")
                    raise RetryExhaustedError(
                        f"Failed after {self.max_retries} attempts",
                        total_attempts=self.max_retries,
                        last_error=last_exception
                    )
            except (AuthenticationError, AuthorizationError, ValidationError, ResourceNotFoundError, ServerError):
                # Don't retry on these specific errors
                raise
            except HammerspaceApiError as e:
                last_exception = e
                if attempt < self.max_retries - 1 and e.status_code and e.status_code >= 500:
                    # Retry on server errors
                    wait_time = self.retry_backoff_factor * (2 ** attempt)
                    logger.warning(f"Server error (attempt {attempt + 1}/{self.max_retries}): {e}. "
                                 f"Retrying in {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                else:
                    raise

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
        # Apply rate limiting
        self._check_rate_limit()
        
        # Check cache for GET requests
        if method == "GET" and not is_login and not _is_retry_after_relogin:
            cache_key = self._get_cache_key(path, method, query_params)
            cached_response = self._get_from_cache(cache_key)
            if cached_response is not None:
                return cached_response
        
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
            
            # Cache successful GET requests
            if method == "GET" and not is_login and not _is_retry_after_relogin:
                cache_key = self._get_cache_key(path, method, query_params)
                response_data = self.read_and_parse_json_body(response)
                if response_data is not None:
                    self._set_cache(cache_key, response_data)
                return response  # Return original response
            
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
            
            # --- IMPROVED ERROR HANDLING WITH SPECIFIC EXCEPTIONS ---
            err_status = e.response.status_code
            err_reason = e.response.reason
            err_message = f"HTTP error: {err_status} {err_reason} for {method} {url}."
            
            # Parse error details for more context
            error_code = None
            error_message_key = None
            error_args = None
            validation_errors = []
            
            try:
                if e.response.headers.get('Content-Type', '').startswith('application/json'):
                    err_details_list = e.response.json()
                    if isinstance(err_details_list, list) and err_details_list:
                        first_error = err_details_list[0]
                        error_code = first_error.get('errorCode')
                        error_args = first_error.get('args')
                        error_message_key = first_error.get('message')
                        
                        if error_code:
                            err_message += f" API Error Code: {error_code}."
                        if error_message_key:
                            err_message += f" Message: '{error_message_key}'."
                        if error_args:
                            err_message += f" Args: {error_args}."
                        if error_code == "VALIDATION_VIOLATION":
                            validation_errors = err_details_list
                            
                        logger.debug(f"Full HTTP error details for {method} {url}: {err_details_list}")
                    else:
                        logger.debug(f"Unexpected JSON error structure for {method} {url}: {err_details_list}")
                        err_message += f" Details: {str(err_details_list)[:200]}"
                else:
                    response_text_preview = e.response.text[:200]
                    err_message += f" Response: {response_text_preview}"
                    logger.debug(f"Full non-JSON error response for {method} {url}: {e.response.text[:1000]}")
            except (ValueError, Exception) as parse_exc:
                logger.debug(f"Error parsing error response details: {parse_exc}")
                err_message += " Could not parse detailed error response."

            # Log the error
            logger.error(err_message)
            
            # Update authentication state
            if err_status == 401:
                self.is_logged_in_via_cookie = False
            
            # Raise specific exceptions based on status code
            if err_status == 401:
                raise AuthenticationError(err_message, err_status, e.response.text, error_code)
            elif err_status == 403:
                raise AuthorizationError(err_message, err_status, e.response.text, error_code)
            elif err_status == 404:
                raise ResourceNotFoundError(err_message, err_status, e.response.text, error_code)
            elif err_status == 400:
                raise ValidationError(err_message, err_status, e.response.text, error_code, validation_errors)
            elif err_status == 429:
                retry_after = e.response.headers.get('Retry-After')
                retry_after_seconds = int(retry_after) if retry_after else None
                raise RateLimitError(err_message, err_status, e.response.text, retry_after_seconds)
            elif err_status >= 500:
                raise ServerError(err_message, err_status, e.response.text, error_code)
            else:
                raise HammerspaceApiError(err_message, err_status, e.response.text, error_code)
        
        except requests.exceptions.RequestException as e:
            error_message = f"Request failed for {method} {url}: {e}"
            logger.error(error_message)
            
            # Handle specific request exceptions
            if isinstance(e, requests.exceptions.ConnectionError):
                raise ConnectionError(f"Failed to connect to {url}: {e}", e)
            elif isinstance(e, requests.exceptions.Timeout):
                raise HammerspaceApiError(f"Request timed out for {method} {url}: {e}", status_code=None, error_code="TIMEOUT_ERROR")
            elif isinstance(e, requests.exceptions.SSLError):
                raise HammerspaceApiError(f"SSL error for {method} {url}: {e}", status_code=None, error_code="SSL_ERROR")
            else:
                raise ConnectionError(f"Request exception for {method} {url}: {e}", e)
  

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
            initial_response = self.make_rest_call_with_retry(
                path,
                method=method,
                json_data=initial_json_data,
                query_params=initial_query_params,
                custom_headers=initial_headers
            )
        except (HammerspaceApiError, requests.exceptions.RequestException) as e:
            logger.error(f"Initial API call failed for {method} {path} during task execution: {e}. Cannot monitor task.")
            raise HammerspaceApiError(f"Task initialization failed: {e}", status_code=getattr(e, 'status_code', None))

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
                        
                        # Import TaskFailedError to raise specific exception
                        from .exceptions import TaskFailedError
                        raise TaskFailedError(
                            f"Task failed with state {task_state}: {error_message}",
                            task_details=current_task_data,
                            status_code=500
                        )
                else:
                    logger.warning(f"Task data not found or not a dictionary while polling {location_url}. Retrying in {poll_interval_seconds}s...")
                
                time.sleep(poll_interval_seconds)

            logger.warning(f"Task monitoring for {location_url} timed out after {task_timeout_seconds} seconds.")
            
            # Import TaskTimeoutError to raise specific exception
            from .exceptions import TaskTimeoutError
            raise TaskTimeoutError(
                f"Task monitoring timed out after {task_timeout_seconds} seconds",
                task_id=location_url,
                timeout_seconds=task_timeout_seconds
            )

        # Fallback for unexpected status codes from initial call
        logger.warning(f"Initial call returned status {initial_response.status_code} which is not a standard success or task initiation. Response: {initial_response_data}")
        return initial_response_data
