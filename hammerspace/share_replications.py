# hammerspace/share_replications.py
import logging
from typing import Optional, Dict, Any, Union, Literal # Added Literal
logger = logging.getLogger(__name__)

class ShareReplicationsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def remove_participant_from_replicating_share( # Renamed from deleteShareReplications
        self,
        share_identifier_path: str, # Path parameter, API name 'identifier'
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Default response (empty object)
        """
        Cause the specified participant to no longer participate in the replicating share.
        (PUT /share-replications/{identifier}) - OpId: deleteShareReplications (Note: OpId is 'delete' for a PUT)

        Args:
            share_identifier_path (str): Identifier of the share replication (path parameter).
            monitor_task (bool): Whether to monitor the task.
            task_timeout_seconds (int): Timeout for monitoring.
        Optional kwargs for query parameters:
            site_id (str): (API name: site-id)
            site_name (str): (API name: site-name)
            site_internal_id (str): (API name: site-internal-id)
            site_address (str): (API name: site-address)
            site_participant_id (int): (API name: site-participant-id)
            ignore_remote_failures (bool): (API name: ignoreRemoteFailures)
            force_master_acquisition (bool): (API name: force-master-acquisition)
        """
        path = f"/share-replications/{share_identifier_path}"
        query_params = {}
        if "site_id" in kwargs: query_params["site-id"] = kwargs["site_id"]
        if "site_name" in kwargs: query_params["site-name"] = kwargs["site_name"]
        if "site_internal_id" in kwargs: query_params["site-internal-id"] = kwargs["site_internal_id"]
        if "site_address" in kwargs: query_params["site-address"] = kwargs["site_address"]
        if "site_participant_id" in kwargs: query_params["site-participant-id"] = kwargs["site_participant_id"]
        if "ignore_remote_failures" in kwargs:
            query_params["ignoreRemoteFailures"] = str(kwargs["ignore_remote_failures"]).lower()
        if "force_master_acquisition" in kwargs:
            query_params["force-master-acquisition"] = str(kwargs["force_master_acquisition"]).lower()
        
        logger.info(f"Removing participant from replicating share '{share_identifier_path}' with query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )