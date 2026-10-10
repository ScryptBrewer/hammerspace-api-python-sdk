"""Spec-generated client for the "reports" API tag. Do not edit.

Regenerate with: python tools/generate_clients.py
"""
from typing import Any, List, Optional, Union
from urllib.parse import quote as _urlquote

from hammerspace.models import generated as gen


class GeneratedReportsClient:
    """Typed coverage for all 21 "reports" operations."""

    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get_active_files(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, share: Optional[Any] = None, sv: Optional[Any] = None, limit: Optional[Any] = None, offset: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for active files reports'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        if share is not None: query_params['share'] = share
        if sv is not None: query_params['sv'] = sv
        if limit is not None: query_params['limit'] = limit
        if offset is not None: query_params['offset'] = offset
        response = self.api_client.make_rest_call(path='/reports/active-files', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_activity_analytics(self, share: Optional[Any] = None, sv: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for active clients reports'
        query_params = {}
        if share is not None: query_params['share'] = share
        if sv is not None: query_params['sv'] = sv
        response = self.api_client.make_rest_call(path='/reports/activity-analytics', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_activity_analytics_summary(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, share: Optional[Any] = None, sv: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for active clients reports'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        if share is not None: query_params['share'] = share
        if sv is not None: query_params['sv'] = sv
        response = self.api_client.make_rest_call(path='/reports/activity-analytics/stats', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_usage(self, activationid: str, preceding_duration_millis: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ClusterUsageStatsView], gen.ClusterUsageStatsView, Any]:
        'Get the usage associated with a metered client license'
        query_params = {}
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        response = self.api_client.make_rest_call(path=f"/reports/licensed-usage/{_urlquote(activationid, safe='')}", method="GET", query_params=query_params, model=gen.ClusterUsageStatsView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ClusterUsageStatsView, raw=raw)

    def get_mobility(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, share: Optional[Any] = None, from_: Optional[Any] = None, to: Optional[Any] = None, volume_group_id: Optional[Any] = None, reasons: Optional[Any] = None, statuses: Optional[Any] = None, page: Optional[Any] = None, page_size: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for mobility reports'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        if share is not None: query_params['share'] = share
        if from_ is not None: query_params['from'] = from_
        if to is not None: query_params['to'] = to
        if volume_group_id is not None: query_params['volumeGroupId'] = volume_group_id
        if reasons is not None: query_params['reasons'] = reasons
        if statuses is not None: query_params['statuses'] = statuses
        if page is not None: query_params['page'] = page
        if page_size is not None: query_params['page.size'] = page_size
        response = self.api_client.make_rest_call(path='/reports/mobility', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_shared_osv_replication_mobility_intervals_by_range(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, intervals: Optional[Any] = None, alignment: Optional[Any] = None, share: Optional[Any] = None, replicating_shares: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for completed replication mobilities involving shared object storage grouped by time intervals in some period specified by a range'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        if intervals is not None: query_params['intervals'] = intervals
        if alignment is not None: query_params['alignment'] = alignment
        if share is not None: query_params['share'] = share
        if replicating_shares is not None: query_params['replicatingShares'] = replicating_shares
        response = self.api_client.make_rest_call(path='/reports/mobility/replications', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_shared_osv_replication_mobility_intervals_by_duration(self, preceding_duration_millis: str, intervals: str, share: Optional[Any] = None, replicating_shares: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for completed replication mobilities involving shared object storage grouped by time intervals in some period preceding current time'
        query_params = {}
        if share is not None: query_params['share'] = share
        if replicating_shares is not None: query_params['replicatingShares'] = replicating_shares
        response = self.api_client.make_rest_call(path=f"/reports/mobility/replications/{_urlquote(preceding_duration_millis, safe='')}/{_urlquote(intervals, safe='')}", method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_share_mobility_intervals_by_duration(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, intervals: Optional[Any] = None, alignment: Optional[Any] = None, share: Optional[Any] = None, statuses: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.MobilityCompletedIntervalView], gen.MobilityCompletedIntervalView, Any]:
        'Query influxDB for completed mobilities for share grouped by time intervals in some period specified by a duration'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        if intervals is not None: query_params['intervals'] = intervals
        if alignment is not None: query_params['alignment'] = alignment
        if share is not None: query_params['share'] = share
        if statuses is not None: query_params['statuses'] = statuses
        response = self.api_client.make_rest_call(path='/reports/mobility/share', method="GET", query_params=query_params, model=gen.MobilityCompletedIntervalView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.MobilityCompletedIntervalView, raw=raw)

    def get_mobility_summary(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, share: Optional[Any] = None, from_: Optional[Any] = None, to: Optional[Any] = None, volume_group_id: Optional[Any] = None, reasons: Optional[Any] = None, statuses: Optional[Any] = None, failed_statuses_only: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for mobility reports summary. At least one of to, from or volumeGroupId must be omitted'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        if share is not None: query_params['share'] = share
        if from_ is not None: query_params['from'] = from_
        if to is not None: query_params['to'] = to
        if volume_group_id is not None: query_params['volumeGroupId'] = volume_group_id
        if reasons is not None: query_params['reasons'] = reasons
        if statuses is not None: query_params['statuses'] = statuses
        if failed_statuses_only is not None: query_params['failed-statuses-only'] = failed_statuses_only
        response = self.api_client.make_rest_call(path='/reports/mobility/summary', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_moe_compliance_stats(self, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectExplorerView], gen.ObjectExplorerView, Any]:
        'Query influxDB for compliance reports'
        query_params = {}
        response = self.api_client.make_rest_call(path='/reports/moe/all-compliance', method="GET", query_params=query_params, model=gen.ObjectExplorerView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectExplorerView, raw=raw)

    def get_moe_compliance_stats_moe(self, share: Optional[Any] = None, storage_container_uuid: Optional[Any] = None, storage_container_type: Optional[Any] = None, breakdown: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectExplorerView], gen.ObjectExplorerView, Any]:
        'Query influxDB for compliance reports'
        query_params = {}
        if share is not None: query_params['share'] = share
        if storage_container_uuid is not None: query_params['storageContainerUuid'] = storage_container_uuid
        if storage_container_type is not None: query_params['storageContainerType'] = storage_container_type
        if breakdown is not None: query_params['breakdown'] = breakdown
        response = self.api_client.make_rest_call(path='/reports/moe/compliance', method="GET", query_params=query_params, model=gen.ObjectExplorerView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectExplorerView, raw=raw)

    def get_moe_mobility_bandwidth(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, from_storage_container_uuid: Optional[Any] = None, from_storage_container_type: Optional[Any] = None, to_storage_container_uuid: Optional[Any] = None, to_storage_container_type: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.MobilityBandwidthStatsView], gen.MobilityBandwidthStatsView, Any]:
        'Query influxDB for performance reports'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if from_storage_container_uuid is not None: query_params['fromStorageContainerUuid'] = from_storage_container_uuid
        if from_storage_container_type is not None: query_params['fromStorageContainerType'] = from_storage_container_type
        if to_storage_container_uuid is not None: query_params['toStorageContainerUuid'] = to_storage_container_uuid
        if to_storage_container_type is not None: query_params['toStorageContainerType'] = to_storage_container_type
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        response = self.api_client.make_rest_call(path='/reports/moe/mobility-bandwidth', method="GET", query_params=query_params, model=gen.MobilityBandwidthStatsView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.MobilityBandwidthStatsView, raw=raw)

    def get_moe_performance(self, share: Optional[Any] = None, storage_container_uuid: Optional[Any] = None, storage_container_type: Optional[Any] = None, breakdown: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.ObjectExplorerView], gen.ObjectExplorerView, Any]:
        'Query influxDB for performance reports'
        query_params = {}
        if share is not None: query_params['share'] = share
        if storage_container_uuid is not None: query_params['storageContainerUuid'] = storage_container_uuid
        if storage_container_type is not None: query_params['storageContainerType'] = storage_container_type
        if breakdown is not None: query_params['breakdown'] = breakdown
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        response = self.api_client.make_rest_call(path='/reports/moe/performance', method="GET", query_params=query_params, model=gen.ObjectExplorerView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.ObjectExplorerView, raw=raw)

    def get_usage_stats(self, preceding_duration_millis: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Get the usage for all clusters known to be subject to metered usage'
        query_params = {}
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        response = self.api_client.make_rest_call(path='/reports/proxy-usage', method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_replication_latencies(self, uuid: str, participant_id: Optional[Any] = None, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.Serie], gen.Serie, Any]:
        'Query influxDB for replication latencies'
        query_params = {}
        if participant_id is not None: query_params['participantId'] = participant_id
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        response = self.api_client.make_rest_call(path=f"/reports/replication/share-latencies/{_urlquote(uuid, safe='')}", method="GET", query_params=query_params, model=gen.Serie, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.Serie, raw=raw)

    def get_alignment_stats(self, object_type: str, object_uuid: str, preceding_duration: Optional[Any] = None, interval_duration: Optional[Any] = None, breakdown: Optional[Any] = None, share_uuid: Optional[Any] = None, volume_uuid: Optional[Any] = None, fill_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StatsResultView], gen.StatsResultView, Any]:
        'Query influxDB for alignment stats data'
        query_params = {}
        if preceding_duration is not None: query_params['precedingDuration'] = preceding_duration
        if interval_duration is not None: query_params['intervalDuration'] = interval_duration
        if breakdown is not None: query_params['breakdown'] = breakdown
        if share_uuid is not None: query_params['shareUuid'] = share_uuid
        if volume_uuid is not None: query_params['volumeUuid'] = volume_uuid
        if fill_type is not None: query_params['fillType'] = fill_type
        response = self.api_client.make_rest_call(path=f"/reports/stats/alignment/{_urlquote(object_type, safe='')}/{_urlquote(object_uuid, safe='')}", method="GET", query_params=query_params, model=gen.StatsResultView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StatsResultView, raw=raw)

    def get_cloud_stats(self, object_type: str, object_uuid: str, preceding_duration: Optional[Any] = None, interval_duration: Optional[Any] = None, file_stat: Optional[Any] = None, breakdown: Optional[Any] = None, volume_uuid: Optional[Any] = None, fill_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StatsResultView], gen.StatsResultView, Any]:
        'Query influxDB for cloud stats data'
        query_params = {}
        if preceding_duration is not None: query_params['precedingDuration'] = preceding_duration
        if interval_duration is not None: query_params['intervalDuration'] = interval_duration
        if file_stat is not None: query_params['fileStat'] = file_stat
        if breakdown is not None: query_params['breakdown'] = breakdown
        if volume_uuid is not None: query_params['volumeUuid'] = volume_uuid
        if fill_type is not None: query_params['fillType'] = fill_type
        response = self.api_client.make_rest_call(path=f"/reports/stats/cloud/{_urlquote(object_type, safe='')}/{_urlquote(object_uuid, safe='')}", method="GET", query_params=query_params, model=gen.StatsResultView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StatsResultView, raw=raw)

    def get_metadata_stats(self, object_type: str, object_uuid: str, preceding_duration: Optional[Any] = None, interval_duration: Optional[Any] = None, fill_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StatsResultView], gen.StatsResultView, Any]:
        'Query influxDB for metadata stats data'
        query_params = {}
        if preceding_duration is not None: query_params['precedingDuration'] = preceding_duration
        if interval_duration is not None: query_params['intervalDuration'] = interval_duration
        if fill_type is not None: query_params['fillType'] = fill_type
        response = self.api_client.make_rest_call(path=f"/reports/stats/metadata/{_urlquote(object_type, safe='')}/{_urlquote(object_uuid, safe='')}", method="GET", query_params=query_params, model=gen.StatsResultView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StatsResultView, raw=raw)

    def get_performance_stats(self, object_type: str, object_uuid: str, preceding_duration: Optional[Any] = None, interval_duration: Optional[Any] = None, breakdown: Optional[Any] = None, share_uuid: Optional[Any] = None, volume_uuid: Optional[Any] = None, fill_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StatsResultView], gen.StatsResultView, Any]:
        'Query influxDB for performance stats data'
        query_params = {}
        if preceding_duration is not None: query_params['precedingDuration'] = preceding_duration
        if interval_duration is not None: query_params['intervalDuration'] = interval_duration
        if breakdown is not None: query_params['breakdown'] = breakdown
        if share_uuid is not None: query_params['shareUuid'] = share_uuid
        if volume_uuid is not None: query_params['volumeUuid'] = volume_uuid
        if fill_type is not None: query_params['fillType'] = fill_type
        response = self.api_client.make_rest_call(path=f"/reports/stats/performance/{_urlquote(object_type, safe='')}/{_urlquote(object_uuid, safe='')}", method="GET", query_params=query_params, model=gen.StatsResultView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StatsResultView, raw=raw)

    def get_space_stats(self, object_type: str, object_uuid: str, preceding_duration: Optional[Any] = None, interval_duration: Optional[Any] = None, breakdown: Optional[Any] = None, share_uuid: Optional[Any] = None, volume_uuid: Optional[Any] = None, fill_type: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.StatsResultView], gen.StatsResultView, Any]:
        'Query influxDB for space stats data'
        query_params = {}
        if preceding_duration is not None: query_params['precedingDuration'] = preceding_duration
        if interval_duration is not None: query_params['intervalDuration'] = interval_duration
        if breakdown is not None: query_params['breakdown'] = breakdown
        if share_uuid is not None: query_params['shareUuid'] = share_uuid
        if volume_uuid is not None: query_params['volumeUuid'] = volume_uuid
        if fill_type is not None: query_params['fillType'] = fill_type
        response = self.api_client.make_rest_call(path=f"/reports/stats/space/{_urlquote(object_type, safe='')}/{_urlquote(object_uuid, safe='')}", method="GET", query_params=query_params, model=gen.StatsResultView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.StatsResultView, raw=raw)

    def get_threshold_crossing_stats(self, start_millis: Optional[Any] = None, end_millis: Optional[Any] = None, storage_container_uuid: Optional[Any] = None, storage_container_type: Optional[Any] = None, preceding_duration_millis: Optional[Any] = None, monitor_task: bool = True, task_timeout_seconds: int = 300, raw: bool = False) -> Union[List[gen.VolumesExceededThresholdReportView], gen.VolumesExceededThresholdReportView, Any]:
        'Query the influxDB for performance reports'
        query_params = {}
        if start_millis is not None: query_params['startMillis'] = start_millis
        if end_millis is not None: query_params['endMillis'] = end_millis
        if storage_container_uuid is not None: query_params['storageContainerUuid'] = storage_container_uuid
        if storage_container_type is not None: query_params['storageContainerType'] = storage_container_type
        if preceding_duration_millis is not None: query_params['precedingDurationMillis'] = preceding_duration_millis
        response = self.api_client.make_rest_call(path='/reports/volumes-exceeded-threshold', method="GET", query_params=query_params, model=gen.VolumesExceededThresholdReportView, raw=raw)
        return self.api_client.read_and_parse_json_body(response, model=gen.VolumesExceededThresholdReportView, raw=raw)
