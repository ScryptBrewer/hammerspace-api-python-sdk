# hammerspace/client.py
import requests
import time
import logging
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
        self.auth = (username, password) if username and password else None
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()

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
        self.login = LoginClient(self) # For /login endpoint
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
        self.storage_volumes = StorageVolumesClient(self) # File storage volumes
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

        logger.info(f"HammerspaceApiClient initialized for {self.base_url} with all clients.")


    def make_rest_call(
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
        # Add headers parameter here
        custom_headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Makes a REST API call.
        'path' can be a relative path or a full URL if is_absolute_url is True.
        """
        if is_absolute_url:
            url = path
        else:
            url = f"{self.base_url}{path.lstrip('/')}"
        
        # Start with default headers
        request_headers = {}
        if not is_login:
            request_headers["Accept"] = "application/json"
            if json_data and not files:
                 request_headers["Content-Type"] = "application/json"
        
        # Merge custom_headers if provided
        if custom_headers:
            request_headers.update(custom_headers)

        logger.debug(f"Request: {method} {url} Params: {query_params} JSON: {json_data is not None} Data: {data is not None} Files: {files is not None} Headers: {request_headers}")

        try:
            response = self.session.request(
                method, url,
                json=json_data if not files and not data else None,
                data=data if not files and not json_data else None,
                params=query_params, auth=self.auth, timeout=self.timeout,
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
                else:
                    logger.debug(f"{log_msg_prefix} - Body: Binary content (no content-type), Length: {len(response.content)}")
            else:
                logger.debug(log_msg_prefix)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            err_msg = f"HTTP error: {e.response.status_code} {e.response.reason} for {method} {url}."
            try:
                if e.response.headers.get('Content-Type', '').startswith('application/json'):
                    err_details = e.response.json()
                    err_msg += f" Details: {err_details}"
                else:
                    err_msg += f" Response: {e.response.text[:500]}"
            except ValueError: 
                err_msg += f" Response (not JSON): {e.response.text[:500]}"
            logger.error(err_msg)
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {method} {url}: {e}")
            raise

    def read_and_parse_json_body(self, response: requests.Response) -> Optional[Union[Dict[str, Any], List[Any]]]:
        if response.status_code == 204: return None
        if not response.content: return None
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('application/json'):
            logger.warning(f"Response content type is '{content_type}', not 'application/json'. Body: {response.text[:200]}")
        try:
            return response.json()
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e} - Response text: {response.text[:500]}")
            return None


    def execute_and_monitor_task(
        self,
        path: str,
        method: str = "POST",
        initial_json_data: Optional[Dict[str, Any]] = None,
        initial_query_params: Optional[Dict[str, Any]] = None,
        # Add initial_headers parameter here
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
                # Pass initial_headers to make_rest_call
                custom_headers=initial_headers
            )
        except requests.exceptions.RequestException:
            logger.error(f"Initial API call failed for {method} {path}. Cannot monitor task.")
            return None

        initial_response_data = self.read_and_parse_json_body(initial_response)

        if not monitor_task:
            logger.debug("Task monitoring disabled. Returning initial response data.")
            return initial_response_data

        if initial_response.status_code in [200, 201]:
            logger.info(f"Synchronous success ({initial_response.status_code}). Returning initial response data.")
            return initial_response_data

        if initial_response.status_code == 202:
            location_url = initial_response.headers.get('Location')
            if not location_url:
                logger.warning("Received 202 Accepted, but no 'Location' header found. Cannot monitor task.")
                logger.debug(f"Initial response headers: {initial_response.headers}")
                return initial_response_data if initial_response_data else {"status": "accepted_no_location"}

            logger.info(f"Task initiated (202 Accepted). Monitoring Location URL: {location_url}")
            start_time = time.time()
            last_known_status_data = None

            while (time.time() - start_time) < task_timeout_seconds:
                logger.debug(f"Polling task status at: {location_url}")
                try:
                    task_status_response = self.make_rest_call(
                        path=location_url,
                        method="GET",
                        is_absolute_url=True,
                        # For polling, we typically don't need custom headers unless the API specifies
                        # custom_headers=initial_headers # Or specific polling headers if needed
                    )
                    current_task_data = self.read_and_parse_json_body(task_status_response)
                    last_known_status_data = current_task_data
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Polling request failed for {location_url}: {e}. Retrying...")
                    time.sleep(poll_interval_seconds)
                    continue

                if current_task_data and isinstance(current_task_data, dict):
                    task_state = current_task_data.get('state', current_task_data.get('status', '')).upper()
                    if not task_state:
                        task_state = current_task_data.get('statusMessage', '').upper()
                    
                    progress = current_task_data.get("progressPercent", "N/A")
                    logger.info(f"Task at {location_url} - State: {task_state}, Progress: {progress}%")

                    if task_state == "COMPLETED":
                        logger.info(f"Task at {location_url} completed successfully.")
                        result_data = current_task_data.get("result", current_task_data)
                        if isinstance(result_data, dict):
                            entity_uuid = result_data.get('uuid')
                            if not entity_uuid and result_data.get('ctxMap') and isinstance(result_data['ctxMap'], dict):
                                entity_uoid_val = result_data['ctxMap'].get('entity-uoid')
                                if isinstance(entity_uoid_val, dict) and entity_uoid_val.get('uuid'):
                                    entity_uuid = entity_uoid_val['uuid']
                                elif isinstance(entity_uoid_val, str) and "uuid=" in entity_uoid_val:
                                    try:
                                        entity_uuid = entity_uoid_val.split("uuid=")[1].split(",")[0].split("]")[0]
                                    except IndexError: pass
                            
                            if entity_uuid:
                                logger.info(f"Task completed, extracted entity UUID: {entity_uuid}")
                                return result_data 
                        return result_data
                    
                    elif task_state in ["FAILED", "CANCELLED", "TIMED_OUT"]:
                        error_message = current_task_data.get("errorMessage", "Task failed, was cancelled, or timed out.")
                        logger.error(f"Task at {location_url} ended. State: {task_state}. Message: {error_message}")
                        return current_task_data
                else:
                    logger.warning(f"Task data not found or not a dictionary while polling {location_url}. Retrying...")
                
                time.sleep(poll_interval_seconds)

            logger.warning(f"Task monitoring for {location_url} timed out after {task_timeout_seconds} seconds.")
            return last_known_status_data

        logger.warning(f"Initial call returned status {initial_response.status_code} which is not a standard success or task initiation. Response: {initial_response_data}")
        return initial_response_data
