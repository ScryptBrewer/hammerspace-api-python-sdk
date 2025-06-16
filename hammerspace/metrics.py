# hammerspace/metrics.py
import logging
from typing import Optional, List, Dict, Any
logger = logging.getLogger(__name__)

class MetricsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def query_metrics_custom(self, **kwargs) -> Optional[Dict[str, Any]]: # Response is 'default', likely JSON
        """
        Query metrics through custom API. (GET /metrics) - OpId: queryMetricsCustom
        Optional kwargs:
            start (int): Start of interval in ms from epoch. (API name: start)
            end (int): End of interval in ms from epoch. (API name: end)
            func (str): Computation aggregate function (MIN, MAX, MEAN, MEDIAN). (API name: func)
            limit (int): Total no. of samples per column. (API name: limit)
            group_by (str): Time grouping interval (e.g., 60s). (API name: groupBy)
            object_type (str): ObjectType criteria. (API name: objectType)
            name (List[str]): Name criteria. (API name: name, array)
            uuid (List[str]): UUID criteria. (API name: uuid, array)
            field (List[str]): Field names (e.g., network.bytesSent). (API name: field, array)
        """
        path = "/metrics"
        query_params = {}
        if "start" in kwargs: query_params["start"] = kwargs["start"]
        if "end" in kwargs: query_params["end"] = kwargs["end"]
        if "func" in kwargs: query_params["func"] = kwargs["func"]
        if "limit" in kwargs: query_params["limit"] = kwargs["limit"]
        if "group_by" in kwargs: query_params["groupBy"] = kwargs["group_by"]
        if "object_type" in kwargs: query_params["objectType"] = kwargs["object_type"]
        if "name" in kwargs: query_params["name"] = kwargs["name"] # requests handles list params
        if "uuid" in kwargs: query_params["uuid"] = kwargs["uuid"]
        if "field" in kwargs: query_params["field"] = kwargs["field"]
        
        logger.info(f"Querying custom metrics with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def get_metrics_capacity( # Renamed for clarity, path params are explicit
        self, object_type_path: str, object_uuid_path: str, **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Query influxDB for capacity metrics data. (GET /metrics/capacity/{objectType}/{objectUuid})
        OpId: getMetricsCapacityByObjectTypeAndObjectUuid
        Args:
            object_type_path (str): Source Object Type (CLUSTER, SHARE, etc.).
            object_uuid_path (str): Source Object UUID.
        Optional kwargs:
            preceding_duration (str): e.g., "30m". (API name: precedingDuration)
            interval_duration (str): e.g., "30s". (API name: intervalDuration)
            include_managed_data_usage (bool): (API name: includeManagedDataUsage)
        """
        path = f"/metrics/capacity/{object_type_path}/{object_uuid_path}"
        query_params = {}
        if "preceding_duration" in kwargs: query_params["precedingDuration"] = kwargs["preceding_duration"]
        if "interval_duration" in kwargs: query_params["intervalDuration"] = kwargs["interval_duration"]
        if "include_managed_data_usage" in kwargs:
            query_params["includeManagedDataUsage"] = str(kwargs["include_managed_data_usage"]).lower()
        
        logger.info(f"Getting capacity metrics for {object_type_path}/{object_uuid_path} with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Returns StatsResultView

    def query_metrics_native(self, **kwargs) -> Optional[Dict[str, Any]]: # Response is 'default'
        """
        Query metrics through native InfluxDB API. (GET /metrics/native) - OpId: queryMetricsNative
        Optional kwargs:
            q (str): InfluxDB native query. (API name: q)
        """
        path = "/metrics/native"
        query_params = {}
        if "q" in kwargs: query_params["q"] = kwargs["q"]
        
        logger.info(f"Querying native metrics with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)