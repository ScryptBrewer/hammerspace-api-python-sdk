# hammerspace/cntl.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class CntlClient:
    def __init__(self, api_client: Any):
        """
        Initializes the CntlClient for cluster control operations.
        """
        self.api_client = api_client
        logger.info("CntlClient initialized using provided OpenAPI spec.")

    def get(self, identifier: Optional[str] = None, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Get cluster info. Typically, this might return a list containing a single cluster's details.
        (Corresponds to GET /cntl - OpId: listClusterInfo)

        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        
        Returns:
            A list of cluster information dictionaries (PdClusterView schema) or None on failure.
        """
        query_params = {}
        if identifier:
            path = f"/cntl/{identifier}" 
            logger.warning(
                f"get_share by id: Attempting GET from '{path}'. "
            )
            # If GET /cntl/{id} has query params, process kwargs here
        else:
            path = "/cntl"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            
        logger.info(f"Listing cluster info with effective query params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: List[PdClusterView]

    def get_cluster_state(self, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get current cluster state information.
        (Corresponds to GET /cntl/state - OpId: getCntlState)

        Optional kwargs:
            with_unclear_event_severity (List[str]): Augment response with unclearedEvents.
                                                      (API name: withUnclearedEventSeverity, array of strings)
        Returns:
            A dictionary containing cluster state information (PdClusterView schema) or None on failure.
        """
        path = "/cntl/state"
        query_params = {}
        if "with_unclear_event_severity" in kwargs:
            # Ensure it's a list for the 'form' style, 'explode: true' parameter
            query_params["withUnclearedEventSeverity"] = kwargs["with_unclear_event_severity"]
            
        logger.info(f"Getting cluster state with effective query params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: PdClusterView

    def update_cluster_info(
        self,
        identifier: str,
        cluster_data: Dict[str, Any], # requestBody is PdClusterView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates cluster information for a specific cluster identifier.
        (Corresponds to PUT /cntl/{identifier} - OpId: updateCntlByIdentifier)
        The API spec indicates a 200 OK response with the updated PdClusterView object.

        Args:
            identifier (str): The identifier of the cluster to update.
            cluster_data (Dict[str, Any]): New data for the cluster (PdClusterView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated PdClusterView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/cntl/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating cluster info for identifier '{identifier}' with data: {cluster_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=cluster_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=cluster_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: PdClusterView

    def accept_eula(
        self,
        monitor_task: bool = True, # Default response {} suggests async or simple ack
        task_timeout_seconds: int = 60
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Accepts the End User License Agreement (EULA).
        (Corresponds to POST /cntl/accept-eula - OpId: acceptCntlEula)

        Args:
            monitor_task (bool): Whether to monitor if this action triggers a background task.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = "/cntl/accept-eula"
        logger.info("Accepting EULA.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {}

    def shutdown_cluster(
        self,
        monitor_task: bool = False, # Nothing responds after shudown
        task_timeout_seconds: int = 600, # Shutdown can take time
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Initiates a cluster shutdown or reboot.
        (Corresponds to POST /cntl/shutdown - OpId: shutdownCntl)
        The API spec indicates a 202 Accepted response.

        Args:
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        Optional kwargs:
            poweroff (bool): If true, power off the system after shutdown.
            reboot (bool): If true, reboot the system after shutdown.
            reason (str): Reason for the shutdown/reboot.

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = "/cntl/shutdown"
        query_params = {}
        if "poweroff" in kwargs: query_params["poweroff"] = str(kwargs["poweroff"]).lower()
        if "reboot" in kwargs: query_params["reboot"] = str(kwargs["reboot"]).lower()
        if "reason" in kwargs: query_params["reason"] = kwargs["reason"]
        
        logger.info(f"Initiating cluster shutdown/reboot with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)