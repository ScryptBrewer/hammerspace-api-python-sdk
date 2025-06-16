# hammerspace/data_analytics.py
import logging
from typing import Optional, List, Dict, Any
logger = logging.getLogger(__name__)

class DataAnalyticsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def query_data_analytics(
        self,
        start: Optional[int] = None, # int64
        end: Optional[int] = None,   # int64
        path_param: Optional[str] = None, 
        field: Optional[List[str]] = None,
        func: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> Optional[List[Dict[str, Any]]]: # Returns array of Serie
        # GET /data-analytics
        # Operation ID: queryDataAnalytics
        api_path = "/data-analytics"
        query_params = {}
        if start is not None: query_params["start"] = start
        if end is not None: query_params["end"] = end
        if path_param is not None: query_params["path"] = path_param
        if field is not None: query_params["field"] = field # Will be sent as multiple params
        if func is not None: query_params["func"] = func
        if group_by is not None: query_params["groupBy"] = group_by
        
        response = self.api_client.make_rest_call(path=api_path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)