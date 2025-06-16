# hammerspace/reports.py
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class ReportsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the ReportsClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client

    def get_active_files_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for active files reports. (GET /reports/active-files)
        Operation ID: getActiveFiles

        Optional kwargs:
            start_millis (int): Start of the interval in [ms] from epoch (default: now - 24h). (API name: startMillis)
            end_millis (int): End of the interval in [ms] from epoch (default: now). (API name: endMillis)
            preceding_duration_millis (int): Preceding duration [ms], instead of start/end. (API name: precedingDurationMillis)
            share (str): Share (default - all). (API name: share)
            sv (str): Storage volume (default - all). (API name: sv)
            limit (int): Limit (default - unlimited). (API name: limit)
            offset (int): Offset (default - none). (API name: offset)
        """
        path = "/reports/active-files"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "sv" in kwargs: query_params["sv"] = kwargs["sv"]
        if "limit" in kwargs: query_params["limit"] = kwargs["limit"]
        if "offset" in kwargs: query_params["offset"] = kwargs["offset"]
        
        logger.info(f"Getting active files report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_activity_analytics_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for active clients reports. (GET /reports/activity-analytics)
        Operation ID: getActivityAnalytics

        Optional kwargs:
            share (str): Share (default - all). (API name: share)
            sv (str): Storage volume (default - all). (API name: sv)
        """
        path = "/reports/activity-analytics"
        query_params = {}
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "sv" in kwargs: query_params["sv"] = kwargs["sv"]
        
        logger.info(f"Getting activity analytics report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_activity_analytics_summary_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for active clients summary reports. (GET /reports/activity-analytics/stats)
        Operation ID: getActivityAnalyticsSummary

        Optional kwargs:
            start_millis (int): Start of interval [ms] from epoch (default: now - 24h). (API name: startMillis)
            end_millis (int): End of interval [ms] from epoch (default: now). (API name: endMillis)
            preceding_duration_millis (int): Preceding duration [ms]. (API name: precedingDurationMillis)
            share (str): Share (default - all). (API name: share)
            sv (str): Storage volume (default - all). (API name: sv)
        """
        path = "/reports/activity-analytics/stats"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "sv" in kwargs: query_params["sv"] = kwargs["sv"]

        logger.info(f"Getting activity analytics summary report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_cloud_activity_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]: # Renamed from list_reports_cloud_activity
        """
        Query influxDB for activity on cloud. (GET /reports/cloud-activity)
        Operation ID: listReportsCloudActivity

        Optional kwargs:
            start_millis (int): Start of interval [ms] from epoch (default: now - 24h). (API name: startMillis)
            end_millis (int): End of interval [ms] from epoch (default: now). (API name: endMillis)
            preceding_duration_millis (int): Preceding duration [ms]. (API name: precedingDurationMillis)
            osv (str): Object Storage Volume (mandatory). (API name: osv)
            cdm_breakdown (bool): Breakdown by CDM (default false). (API name: cdm_breakdown)
        """
        path = "/reports/cloud-activity"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "osv" in kwargs: query_params["osv"] = kwargs["osv"] # Mandatory
        if "cdm_breakdown" in kwargs: query_params["cdm_breakdown"] = str(kwargs["cdm_breakdown"]).lower()
        
        if "osv" not in query_params:
            logger.error("Mandatory parameter 'osv' (Object Storage Volume) is missing for get_cloud_activity_report.")
            return None

        logger.info(f"Getting cloud activity report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_licensed_usage_report(self, activationid: str, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Get the usage associated with a metered client license. (GET /reports/licensed-usage/{activationid})
        Operation ID: getReportsLicensedUsageByIdentifier

        Args:
            activationid (str): Activation ID of the metered usage license (path parameter).
        Optional kwargs:
            preceding_duration_millis (int): Specify reporting range as ms before current time. (API name: precedingDurationMillis)
        """
        path = f"/reports/licensed-usage/{activationid}"
        query_params = {}
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        
        logger.info(f"Getting licensed usage report for activation ID '{activationid}' with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Returns array of ClusterUsageStatsView

    def get_mobility_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for mobility reports. (GET /reports/mobility)
        Operation ID: getReportsMobility

        Optional kwargs:
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
            share (str): (API name: share)
            from_volume (str): Storage volume from (default - all). (API name: from)
            to_volume (str): Storage volume to (default - all). (API name: to)
            volume_group_id (str): UUID, name or internalId of volume group. (API name: volumeGroupId)
            reasons (List[str]): Reasons (default- all). (API name: reasons, array)
            statuses (List[str]): Statuses (default - all). (API name: statuses, array)
            page (int): (API name: page)
            page_size (int): (API name: page.size)
        """
        path = "/reports/mobility"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "from_volume" in kwargs: query_params["from"] = kwargs["from_volume"]
        if "to_volume" in kwargs: query_params["to"] = kwargs["to_volume"]
        if "volume_group_id" in kwargs: query_params["volumeGroupId"] = kwargs["volume_group_id"]
        if "reasons" in kwargs: query_params["reasons"] = kwargs["reasons"] # List of strings
        if "statuses" in kwargs: query_params["statuses"] = kwargs["statuses"] # List of strings
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        
        logger.info(f"Getting mobility report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_shared_osv_replication_mobility_intervals_by_range_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for completed replication mobilities involving shared object storage, grouped by time intervals in a specified range.
        (GET /reports/mobility/replications) - OpId: getSharedOsvReplicationMobilityIntervalsByRange

        Optional kwargs:
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
            intervals (int): Number of equal-size intervals. (API name: intervals)
            alignment (int): Align startMillis of intervals. (API name: alignment)
            share (str): Share UUID, name, or internalId. (API name: share)
            replicating_shares (bool): (API name: replicatingShares)
        """
        path = "/reports/mobility/replications"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "intervals" in kwargs: query_params["intervals"] = kwargs["intervals"]
        if "alignment" in kwargs: query_params["alignment"] = kwargs["alignment"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "replicating_shares" in kwargs: query_params["replicatingShares"] = str(kwargs["replicating_shares"]).lower()

        logger.info(f"Getting shared OSV replication mobility (range) report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_shared_osv_replication_mobility_intervals_by_duration_report(
        self, preceding_duration_millis_path: int, intervals_path: int, **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for completed replication mobilities involving shared object storage, grouped by time intervals in a period preceding current time.
        (GET /reports/mobility/replications/{precedingDurationMillis}/{intervals}) - OpId: getSharedOsvReplicationMobilityIntervalsByDuration

        Args:
            preceding_duration_millis_path (int): Period in [ms] preceding current time (path parameter).
            intervals_path (int): Number of equal-size intervals (path parameter).
        Optional kwargs:
            share (str): Share UUID, name, or internalId. (API name: share)
            replicating_shares (bool): (API name: replicatingShares)
        """
        path = f"/reports/mobility/replications/{preceding_duration_millis_path}/{intervals_path}"
        query_params = {}
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "replicating_shares" in kwargs: query_params["replicatingShares"] = str(kwargs["replicating_shares"]).lower()

        logger.info(f"Getting shared OSV replication mobility (duration) report for {preceding_duration_millis_path}/{intervals_path} with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_share_mobility_intervals_by_duration_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for completed mobilities for a share, grouped by time intervals in a specified period.
        (GET /reports/mobility/share) - OpId: getShareMobilityIntervalsByDuration

        Optional kwargs:
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
            intervals (int): (API name: intervals)
            alignment (int): (API name: alignment)
            share (str): Share UUID, name, or internalId. (API name: share)
            statuses (List[str]): Statuses (default - all). (API name: statuses, array)
        """
        path = "/reports/mobility/share"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "intervals" in kwargs: query_params["intervals"] = kwargs["intervals"]
        if "alignment" in kwargs: query_params["alignment"] = kwargs["alignment"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "statuses" in kwargs: query_params["statuses"] = kwargs["statuses"]

        logger.info(f"Getting share mobility intervals report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Returns array of MobilityCompletedIntervalView

    def get_mobility_summary_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for mobility reports summary.
        (GET /reports/mobility/summary) - OpId: getReportsMobilitySummary
        Note: At least one of 'to_volume', 'from_volume', or 'volume_group_id' should typically be provided or behavior might be broad.

        Optional kwargs:
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
            share (str): (API name: share)
            from_volume (str): Source volume UUID or name. (API name: from)
            to_volume (str): Destination volume UUID or name. (API name: to)
            volume_group_id (str): Volume group UUID, name, or internalId. (API name: volumeGroupId)
            reasons (List[str]): (API name: reasons, array)
            statuses (List[str]): (API name: statuses, array)
            failed_statuses_only (bool): (API name: failed-statuses-only)
        """
        path = "/reports/mobility/summary"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "from_volume" in kwargs: query_params["from"] = kwargs["from_volume"]
        if "to_volume" in kwargs: query_params["to"] = kwargs["to_volume"]
        if "volume_group_id" in kwargs: query_params["volumeGroupId"] = kwargs["volume_group_id"]
        if "reasons" in kwargs: query_params["reasons"] = kwargs["reasons"]
        if "statuses" in kwargs: query_params["statuses"] = kwargs["statuses"]
        if "failed_statuses_only" in kwargs: query_params["failed-statuses-only"] = str(kwargs["failed_statuses_only"]).lower()

        logger.info(f"Getting mobility summary report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_moe_all_compliance_stats_report(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns ObjectExplorerView
        """
        Query influxDB for all compliance reports. (GET /reports/moe/all-compliance)
        Operation ID: getReportsMoeAllComplianceStats
        No query parameters listed in spec, but adding **kwargs for future-proofing.
        """
        path = "/reports/moe/all-compliance"
        query_params = {} # Process kwargs if API evolves
        logger.info(f"Getting MOE all compliance stats report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_moe_compliance_stats_report(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns ObjectExplorerView
        """
        Query influxDB for compliance reports. (GET /reports/moe/compliance)
        Operation ID: getReportsMoeComplianceStats

        Optional kwargs:
            share (str): (API name: share)
            storage_container_uuid (str): (API name: storageContainerUuid)
            storage_container_type (str): (API name: storageContainerType)
            breakdown (str): (API name: breakdown)
        """
        path = "/reports/moe/compliance"
        query_params = {}
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "storage_container_uuid" in kwargs: query_params["storageContainerUuid"] = kwargs["storage_container_uuid"]
        if "storage_container_type" in kwargs: query_params["storageContainerType"] = kwargs["storage_container_type"]
        if "breakdown" in kwargs: query_params["breakdown"] = kwargs["breakdown"]
        
        logger.info(f"Getting MOE compliance stats report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_moe_mobility_bandwidth_report(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns MobilityBandwidthStatsView
        """
        Query influxDB for performance reports (mobility bandwidth). (GET /reports/moe/mobility-bandwidth)
        Operation ID: getReportsMoeMobilityBandwidth

        Optional kwargs:
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            from_storage_container_uuid (str): (API name: fromStorageContainerUuid)
            from_storage_container_type (str): (API name: fromStorageContainerType)
            to_storage_container_uuid (str): (API name: toStorageContainerUuid)
            to_storage_container_type (str): (API name: toStorageContainerType)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
        """
        path = "/reports/moe/mobility-bandwidth"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "from_storage_container_uuid" in kwargs: query_params["fromStorageContainerUuid"] = kwargs["from_storage_container_uuid"]
        if "from_storage_container_type" in kwargs: query_params["fromStorageContainerType"] = kwargs["from_storage_container_type"]
        if "to_storage_container_uuid" in kwargs: query_params["toStorageContainerUuid"] = kwargs["to_storage_container_uuid"]
        if "to_storage_container_type" in kwargs: query_params["toStorageContainerType"] = kwargs["to_storage_container_type"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]

        logger.info(f"Getting MOE mobility bandwidth report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_moe_performance_report(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns ObjectExplorerView
        """
        Query influxDB for performance reports. (GET /reports/moe/performance)
        Operation ID: getReportsMoePerformance

        Optional kwargs:
            share (str): (API name: share)
            storage_container_uuid (str): (API name: storageContainerUuid)
            storage_container_type (str): (API name: storageContainerType)
            breakdown (str): (API name: breakdown)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
        """
        path = "/reports/moe/performance"
        query_params = {}
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        if "storage_container_uuid" in kwargs: query_params["storageContainerUuid"] = kwargs["storage_container_uuid"]
        if "storage_container_type" in kwargs: query_params["storageContainerType"] = kwargs["storage_container_type"]
        if "breakdown" in kwargs: query_params["breakdown"] = kwargs["breakdown"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]

        logger.info(f"Getting MOE performance report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_proxy_usage_stats_report(self, **kwargs) -> Optional[List[Dict[str, Any]]]: # Returns array of Serie
        """
        Get the usage for all clusters known to be subject to metered usage. (GET /reports/proxy-usage)
        Operation ID: getReportsUsageStats

        Optional kwargs:
            preceding_duration_millis (int): Specify reporting range as ms before current time. (API name: precedingDurationMillis)
        """
        path = "/reports/proxy-usage"
        query_params = {}
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]
        
        logger.info(f"Getting proxy usage stats report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_replication_latencies_report(self, share_uuid_path: str, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Query influxDB for replication latencies. (GET /reports/replication/share-latencies/{uuid})
        Operation ID: getReportsReplicationLatencies

        Args:
            share_uuid_path (str): Share UUID (path parameter, API name 'uuid').
        Optional kwargs:
            participant_id (str): (API name: participantId)
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
        """
        path = f"/reports/replication/share-latencies/{share_uuid_path}"
        query_params = {}
        if "participant_id" in kwargs: query_params["participantId"] = kwargs["participant_id"]
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]

        logger.info(f"Getting replication latencies report for share '{share_uuid_path}' with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_stats_report( # Generic helper for /reports/stats/{category}/{objectType}/{objectUuid}
        self, category: str, object_type_path: str, object_uuid_path: str, **kwargs
    ) -> Optional[Dict[str, Any]]: # Returns StatsResultView
        """
        Query influxDB for various stats data (alignment, metadata, performance, space).
        Base path: /reports/stats/{category}/{objectType}/{objectUuid}

        Args:
            category (str): One of 'alignment', 'metadata', 'performance', 'space'.
            object_type_path (str): Source Object Type (e.g., CLUSTER, SHARE).
            object_uuid_path (str): Source Object UUID.
        Optional kwargs:
            preceding_duration (str): e.g., "30m". (API name: precedingDuration)
            interval_duration (str): e.g., "30s". (API name: intervalDuration)
            breakdown (List[str]): Break output by type (e.g., ["SHARE", "STORAGE_VOLUME"]). (API name: breakdown, array)
            share_uuid (List[str]): Share UUIDs to filter. (API name: shareUuid, array)
            volume_uuid (List[str]): Volume UUIDs to filter. (API name: volumeUuid, array)
        """
        if category not in ["alignment", "metadata", "performance", "space"]:
            logger.error(f"Invalid category '{category}' for get_stats_report.")
            return None
        path = f"/reports/stats/{category}/{object_type_path}/{object_uuid_path}"
        query_params = {}
        if "preceding_duration" in kwargs: query_params["precedingDuration"] = kwargs["preceding_duration"]
        if "interval_duration" in kwargs: query_params["intervalDuration"] = kwargs["interval_duration"]
        if "breakdown" in kwargs: query_params["breakdown"] = kwargs["breakdown"] # List of strings
        if "share_uuid" in kwargs: query_params["shareUuid"] = kwargs["share_uuid"] # List of strings
        if "volume_uuid" in kwargs: query_params["volumeUuid"] = kwargs["volume_uuid"] # List of strings

        logger.info(f"Getting {category} stats report for {object_type_path}/{object_uuid_path} with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_volumes_exceeded_threshold_report(self, **kwargs) -> Optional[Dict[str, Any]]: # Returns VolumesExceededThresholdReportView
        """
        Query the influxDB for performance reports (volumes exceeded threshold).
        (GET /reports/volumes-exceeded-threshold) - OpId: getReportsThresholdCrossingStats

        Optional kwargs:
            start_millis (int): (API name: startMillis)
            end_millis (int): (API name: endMillis)
            storage_container_uuid (str): (API name: storageContainerUuid)
            storage_container_type (str): (API name: storageContainerType)
            preceding_duration_millis (int): (API name: precedingDurationMillis)
        """
        path = "/reports/volumes-exceeded-threshold"
        query_params = {}
        if "start_millis" in kwargs: query_params["startMillis"] = kwargs["start_millis"]
        if "end_millis" in kwargs: query_params["endMillis"] = kwargs["end_millis"]
        if "storage_container_uuid" in kwargs: query_params["storageContainerUuid"] = kwargs["storage_container_uuid"]
        if "storage_container_type" in kwargs: query_params["storageContainerType"] = kwargs["storage_container_type"]
        if "preceding_duration_millis" in kwargs: query_params["precedingDurationMillis"] = kwargs["preceding_duration_millis"]

        logger.info(f"Getting volumes exceeded threshold report with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)
