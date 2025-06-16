# hammerspace/__init__.py
"""
Hammerspace API Client Library
"""

__version__ = "0.1.0" # Example version, update as you see fit

# Import the main API client first, as other clients might depend on its types for hinting
from .client import HammerspaceApiClient

# Import all specific resource client classes
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
from .login import LoginClient # Assuming LoginClient exists for /login endpoint
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

__all__ = [
    "HammerspaceApiClient",
    "AdClient",
    "AntivirusClient",
    "BackupClient",
    "BaseStorageVolumesClient",
    "CntlClient",
    "DataAnalyticsClient",
    "DataCopyToObjectClient",
    "DataPortalsClient",
    "DiskDrivesClient",
    "DnssClient",
    "DomainIdmapsClient",
    "EventsClient",
    "FileSnapshotsClient",
    "FilesClient",
    "GatewaysClient",
    "HeartbeatClient",
    "I18nClient",
    "IdentityGroupMappingsClient",
    "IdentityClient",
    "IdpClient",
    "KmsesClient",
    "LabelsClient",
    "LdapsClient",
    "LicenseServerClient",
    "LicensesClient",
    "LogicalVolumesClient",
    "LoginPolicyClient",
    "LoginClient",
    "MailsmtpClient",
    "MetricsClient",
    "ModelerClient",
    "NetworkInterfacesClient",
    "NisClient",
    "NodesClient",
    "NotificationRulesClient",
    "NtpsClient",
    "ObjectStorageVolumesClient",
    "ObjectStoreLogicalVolumesClient",
    "ObjectStoresClient",
    "ObjectivesClient",
    "PdNodeCntlClient",
    "PdSupportClient",
    "ProcessorClient",
    "ReportsClient",
    "RolesClient",
    "S3ServerClient",
    "SchedulesClient",
    "ShareParticipantsClient",
    "ShareReplicationsClient",
    "ShareSnapshotsClient",
    "SharesClient",
    "SitesClient",
    "SnapshotRetentionsClient",
    "SnmpClient",
    "StaticRoutesClient",
    "StorageVolumesClient",
    "SubnetGatewaysClient",
    "SwUpdateClient",
    "SyslogClient",
    "SystemInfoClient",
    "SystemClient",
    "TasksClient",
    "UserGroupsClient",
    "UsersClient",
    "VersionsClient",
    "VolumeGroupsClient",
]