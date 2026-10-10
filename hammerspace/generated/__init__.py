"""Registry of spec-generated API clients. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
import importlib
from typing import Any, Dict, List

TAG_MODULES: Dict[str, str] = {
    'ad': 'ad',
    'antivirus': 'antivirus',
    'backup': 'backup',
    'base-storage-volumes': 'base_storage_volumes',
    'cntl': 'cntl',
    'data-analytics': 'data_analytics',
    'data-copy-to-object': 'data_copy_to_object',
    'data-portals': 'data_portals',
    'disk-drives': 'disk_drives',
    'dnss': 'dnss',
    'domain-idmaps': 'domain_idmaps',
    'events': 'events',
    'file-snapshots': 'file_snapshots',
    'files': 'files',
    'gateways': 'gateways',
    'heartbeat': 'heartbeat',
    'i18n': 'i18n',
    'identity': 'identity',
    'identity-group-mappings': 'identity_group_mappings',
    'idp': 'idp',
    'kmses': 'kmses',
    'labels': 'labels',
    'ldaps': 'ldaps',
    'license-server': 'license_server',
    'licenses': 'licenses',
    'logical-volumes': 'logical_volumes',
    'login': 'login',
    'login-policy': 'login_policy',
    'mailsmtp': 'mailsmtp',
    'mdsis': 'mdsis',
    'metrics': 'metrics',
    'modeler': 'modeler',
    'network-interfaces': 'network_interfaces',
    'nis': 'nis',
    'nodes': 'nodes',
    'notification-rules': 'notification_rules',
    'ntps': 'ntps',
    'nvmeof-enclosures': 'nvmeof_enclosures',
    'object-storage-volumes': 'object_storage_volumes',
    'object-store-logical-volumes': 'object_store_logical_volumes',
    'object-stores': 'object_stores',
    'objectives': 'objectives',
    'pd-node-cntl': 'pd_node_cntl',
    'pd-support': 'pd_support',
    'processor': 'processor',
    'reports': 'reports',
    'roles': 'roles',
    's3server': 's3server',
    'schedules': 'schedules',
    'share-participants': 'share_participants',
    'share-replications': 'share_replications',
    'share-snapshots': 'share_snapshots',
    'shares': 'shares',
    'sites': 'sites',
    'smbautohomes': 'smbautohomes',
    'snapshot-retentions': 'snapshot_retentions',
    'snmp': 'snmp',
    'static-routes': 'static_routes',
    'storage-volumes': 'storage_volumes',
    'subnet-gateways': 'subnet_gateways',
    'sw-update': 'sw_update',
    'syslog': 'syslog',
    'system': 'system',
    'system-info': 'system_info',
    'tasks': 'tasks',
    'user-groups': 'user_groups',
    'users': 'users',
    'versions': 'versions',
    'volume-groups': 'volume_groups',
}

_CLASS_NAMES: Dict[str, str] = {
    'ad': 'GeneratedAdClient',
    'antivirus': 'GeneratedAntivirusClient',
    'backup': 'GeneratedBackupClient',
    'base-storage-volumes': 'GeneratedBaseStorageVolumesClient',
    'cntl': 'GeneratedCntlClient',
    'data-analytics': 'GeneratedDataAnalyticsClient',
    'data-copy-to-object': 'GeneratedDataCopyToObjectClient',
    'data-portals': 'GeneratedDataPortalsClient',
    'disk-drives': 'GeneratedDiskDrivesClient',
    'dnss': 'GeneratedDnssClient',
    'domain-idmaps': 'GeneratedDomainIdmapsClient',
    'events': 'GeneratedEventsClient',
    'file-snapshots': 'GeneratedFileSnapshotsClient',
    'files': 'GeneratedFilesClient',
    'gateways': 'GeneratedGatewaysClient',
    'heartbeat': 'GeneratedHeartbeatClient',
    'i18n': 'GeneratedI18nClient',
    'identity': 'GeneratedIdentityClient',
    'identity-group-mappings': 'GeneratedIdentityGroupMappingsClient',
    'idp': 'GeneratedIdpClient',
    'kmses': 'GeneratedKmsesClient',
    'labels': 'GeneratedLabelsClient',
    'ldaps': 'GeneratedLdapsClient',
    'license-server': 'GeneratedLicenseServerClient',
    'licenses': 'GeneratedLicensesClient',
    'logical-volumes': 'GeneratedLogicalVolumesClient',
    'login': 'GeneratedLoginClient',
    'login-policy': 'GeneratedLoginPolicyClient',
    'mailsmtp': 'GeneratedMailsmtpClient',
    'mdsis': 'GeneratedMdsisClient',
    'metrics': 'GeneratedMetricsClient',
    'modeler': 'GeneratedModelerClient',
    'network-interfaces': 'GeneratedNetworkInterfacesClient',
    'nis': 'GeneratedNisClient',
    'nodes': 'GeneratedNodesClient',
    'notification-rules': 'GeneratedNotificationRulesClient',
    'ntps': 'GeneratedNtpsClient',
    'nvmeof-enclosures': 'GeneratedNvmeofEnclosuresClient',
    'object-storage-volumes': 'GeneratedObjectStorageVolumesClient',
    'object-store-logical-volumes': 'GeneratedObjectStoreLogicalVolumesClient',
    'object-stores': 'GeneratedObjectStoresClient',
    'objectives': 'GeneratedObjectivesClient',
    'pd-node-cntl': 'GeneratedPdNodeCntlClient',
    'pd-support': 'GeneratedPdSupportClient',
    'processor': 'GeneratedProcessorClient',
    'reports': 'GeneratedReportsClient',
    'roles': 'GeneratedRolesClient',
    's3server': 'GeneratedS3serverClient',
    'schedules': 'GeneratedSchedulesClient',
    'share-participants': 'GeneratedShareParticipantsClient',
    'share-replications': 'GeneratedShareReplicationsClient',
    'share-snapshots': 'GeneratedShareSnapshotsClient',
    'shares': 'GeneratedSharesClient',
    'sites': 'GeneratedSitesClient',
    'smbautohomes': 'GeneratedSmbautohomesClient',
    'snapshot-retentions': 'GeneratedSnapshotRetentionsClient',
    'snmp': 'GeneratedSnmpClient',
    'static-routes': 'GeneratedStaticRoutesClient',
    'storage-volumes': 'GeneratedStorageVolumesClient',
    'subnet-gateways': 'GeneratedSubnetGatewaysClient',
    'sw-update': 'GeneratedSwUpdateClient',
    'syslog': 'GeneratedSyslogClient',
    'system': 'GeneratedSystemClient',
    'system-info': 'GeneratedSystemInfoClient',
    'tasks': 'GeneratedTasksClient',
    'user-groups': 'GeneratedUserGroupsClient',
    'users': 'GeneratedUsersClient',
    'versions': 'GeneratedVersionsClient',
    'volume-groups': 'GeneratedVolumeGroupsClient',
}


def get_client_class(tag: str) -> type:
    """Import and return the generated client class for ``tag`` (lazily)."""
    module_name = TAG_MODULES.get(tag)
    if module_name is None:
        raise KeyError(
            f'No generated client for {tag!r}; known tags: {sorted(TAG_MODULES)}'
        )
    module = importlib.import_module('hammerspace.generated.' + module_name)
    return getattr(module, _CLASS_NAMES[tag])


class GeneratedApiNamespace:
    """Lazy namespace: ``client.generated.<tag>`` -> typed client.

    Each tag module is imported on first access, so touching one tag
    does not pay the import cost of the other 68.
    """

    def __init__(self, api_client: Any):
        self._api_client = api_client

    def __getattr__(self, name: str) -> Any:
        if name not in TAG_MODULES:
            raise AttributeError(
                f'No generated client for {name!r}; known tags: {sorted(TAG_MODULES)}'
            ) from None
        instance = get_client_class(name)(self._api_client)
        setattr(self, name, instance)
        return instance

    def __dir__(self) -> List[str]:
        return sorted(set(super().__dir__()) | set(TAG_MODULES))


__all__ = ["TAG_MODULES", "get_client_class", "GeneratedApiNamespace"]
