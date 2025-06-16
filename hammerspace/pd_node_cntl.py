# hammerspace/pd_node_cntl.py
import logging
from typing import Optional, Dict, Any, Union
logger = logging.getLogger(__name__)

class PdNodeCntlClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def add_ha_node( 
        self, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add HA node. (POST /pd-node-cntl/add) - OpId: addPdNodeNntl (Typo in OpId)
        Optional kwargs for query parameters:
            ip (str): IP address of the HA node. (API name: ip)
        """
        path = "/pd-node-cntl/add"
        query_params = {}
        if "ip" in kwargs: query_params["ip"] = kwargs["ip"]
        logger.info(f"Adding HA node with query params: {query_params}")
        # OpenAPI says 200 response (empty object), but adding a node sounds async.
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def repair_storage_node( 
        self, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Repair storage node. (POST /pd-node-cntl/repair) - OpId: repairPdNodeNntlByIdentifier (Typo in OpId)
        Optional kwargs for query parameters:
            node_id (str): ID of the node to repair. (API name: id)
        """
        path = "/pd-node-cntl/repair"
        query_params = {}
        if "node_id" in kwargs: query_params["id"] = kwargs["node_id"] # API param is 'id'
        logger.info(f"Repairing storage node with query params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
