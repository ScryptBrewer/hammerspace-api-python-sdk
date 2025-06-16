# hammerspace/gateways.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class GatewaysClient:
    def __init__(self, api_client: Any):
        """
        Initializes the GatewaysClient.
        """
        self.api_client = api_client
        logger.info("GatewaysClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all gateway configurations or a specific gateway by its identifier.

        If 'identifier' is provided, fetches a single gateway configuration.
        (Corresponds to GET /gateways/{identifier} - OpId: getGatewayByIdentifier)
        Note: The GET /gateways/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all gateway configurations.
        (Corresponds to GET /gateways - OpId: listGateways)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/gateways/{identifier}"
            logger.info(f"Getting gateway configuration by identifier: {identifier}")
            # No query parameters are defined for GET /gateways/{identifier} in the spec.
        else:
            path = "/gateways"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all gateway configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: GatewayView or List[GatewayView]

    def create_gateway(
        self,
        gateway_data: Dict[str, Any], # requestBody is GatewayView
        monitor_task: bool = False, # Spec says 200 OK with GatewayView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new gateway configuration.
        (Corresponds to POST /gateways - OpId: createGateway)
        The API spec indicates a 200 OK response with the created GatewayView object.

        Args:
            gateway_data (Dict[str, Any]): The data for the new gateway (GatewayView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created GatewayView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/gateways"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Creating gateway configuration with data: {gateway_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=gateway_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=gateway_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: GatewayView

    def update(
        self,
        identifier: str,
        gateway_data: Dict[str, Any], # requestBody is GatewayView
        monitor_task: bool = False, # Spec says 200 OK with GatewayView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing gateway configuration by its identifier.
        (Corresponds to PUT /gateways/{identifier} - OpId: updateGatewayByIdentifier)
        The API spec indicates a 200 OK response with the updated GatewayView object.

        Args:
            identifier (str): The identifier of the gateway configuration to update.
            gateway_data (Dict[str, Any]): The new data for the configuration (GatewayView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated GatewayView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/gateways/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating gateway configuration '{identifier}' with data: {gateway_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=gateway_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=gateway_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: GatewayView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK with GatewayView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a gateway configuration by its identifier.
        (Corresponds to DELETE /gateways/{identifier} - OpId: deleteGatewayByIdentifier)
        The API spec indicates a 200 OK response with the deleted GatewayView object (unusual for DELETE).

        Args:
            identifier (str): The identifier of the gateway configuration to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted GatewayView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/gateways/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        
        logger.info(f"Deleting gateway configuration '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: GatewayView
