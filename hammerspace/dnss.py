# hammerspace/dnss.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class DnssClient:
    def __init__(self, api_client: Any):
        """
        Initializes the DnssClient for managing DNS server configurations.
        """
        self.api_client = api_client
        logger.info("DnssClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all DNS server configurations or a specific one by its identifier.

        If 'identifier' is provided, fetches a single DNS server configuration.
        (Corresponds to GET /dnss/{identifier} - OpId: getDnsByIdentifier)
        Note: The GET /dnss/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all DNS server configurations.
        (Corresponds to GET /dnss - OpId: listDns)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/dnss/{identifier}"
            logger.info(f"Getting DNS server configuration by identifier: {identifier}")
            # No query parameters are defined for GET /dnss/{identifier} in the spec.
        else:
            path = "/dnss"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all DNS server configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: DnsView or List[DnsView]

    def create_dns_server(
        self,
        dns_data: Dict[str, Any], # requestBody is DnsView
        monitor_task: bool = False, # Spec says 200 OK with DnsView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new DNS server configuration.
        (Corresponds to POST /dnss - OpId: createDns)
        The API spec indicates a 200 OK response with the created DnsView object.

        Args:
            dns_data (Dict[str, Any]): The data for the new DNS server (DnsView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created DnsView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/dnss"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Creating DNS server configuration with data: {dns_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=dns_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=dns_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: DnsView

    def update(
        self,
        identifier: str,
        dns_data: Dict[str, Any], # requestBody is DnsView
        monitor_task: bool = False, # Spec says 200 OK with DnsView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing DNS server configuration by its identifier.
        (Corresponds to PUT /dnss/{identifier} - OpId: updateDnsByIdentifier)
        The API spec indicates a 200 OK response with the updated DnsView object.

        Args:
            identifier (str): The identifier of the DNS server configuration to update.
            dns_data (Dict[str, Any]): The new data for the configuration (DnsView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated DnsView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/dnss/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating DNS server configuration '{identifier}' with data: {dns_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=dns_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=dns_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: DnsView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK with DnsView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a DNS server configuration by its identifier.
        (Corresponds to DELETE /dnss/{identifier} - OpId: deleteDnsByIdentifier)
        The API spec indicates a 200 OK response with the deleted DnsView object (unusual for DELETE).

        Args:
            identifier (str): The identifier of the DNS server configuration to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted DnsView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/dnss/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        
        logger.info(f"Deleting DNS server configuration '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: DnsView
