# hammerspace/subnet_gateways.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class SubnetGatewaysClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client
        logger.info("SubnetGatewaysClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all subnet gateways or a specific one by its identifier.

        If 'identifier' is provided, fetches a single subnet gateway.
        (Corresponds to GET /subnet-gateways/{identifier} - OpId: getSubnetGatewayByIdentifier)

        Otherwise, lists all subnet gateways.
        (Corresponds to GET /subnet-gateways - OpId: listSubnetGateways)
        Optional kwargs for listing: spec, page, page.size, page.sort, page.sort.dir
        """
        query_params = {}
        if identifier:
            path = f"/subnet-gateways/{identifier}"
            logger.info(f"Getting subnet gateway by identifier: {identifier}")
            # No query params defined for GET /subnet-gateways/{identifier} in spec
        else:
            path = "/subnet-gateways"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing subnet gateways with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Returns SubnetGatewayView or List

    def create(
        self,
        gateway_data: Dict[str, Any],
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new subnet gateway.
        (Corresponds to POST /subnet-gateways - OpId: createSubnetGateway)
        """
        path = "/subnet-gateways"
        query_params = {} # No query params for POST in spec
        logger.info(f"Creating subnet gateway with data: {gateway_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=gateway_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Returns SubnetGatewayView

    def update(
        self,
        identifier: str,
        gateway_data: Dict[str, Any],
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing subnet gateway by its identifier.
        (Corresponds to PUT /subnet-gateways/{identifier} - OpId: updateSubnetGatewayByIdentifier)
        """
        path = f"/subnet-gateways/{identifier}"
        query_params = {} # No query params for PUT in spec
        logger.info(f"Updating subnet gateway '{identifier}' with data: {gateway_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=gateway_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Returns SubnetGatewayView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a subnet gateway by its identifier.
        (Corresponds to DELETE /subnet-gateways/{identifier} - OpId: deleteSubnetGatewayByIdentifier)
        """
        path = f"/subnet-gateways/{identifier}"
        query_params = {} # No query params for DELETE in spec
        logger.info(f"Deleting subnet gateway '{identifier}'")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
