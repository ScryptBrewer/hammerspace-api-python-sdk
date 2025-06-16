# hammerspace/snmp.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class SnmpClient:
    def __init__(self, api_client: Any):
        """
        Initializes the SnmpClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client
        logger.info("SnmpClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all SNMP configurations or a specific SNMP configuration by its identifier.

        If 'identifier' is provided, fetches a single SNMP configuration.
        (Corresponds to GET /snmp/{identifier} - OpId: getSnmpConfigurationByIdentifier)
        Note: The GET /snmp/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all SNMP configurations.
        (Corresponds to GET /snmp - OpId: listSnmpConfiguration)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/snmp/{identifier}"
            logger.info(f"Getting SNMP configuration by identifier: {identifier}")
            # No query parameters are defined for GET /snmp/{identifier} in the spec.
        else:
            path = "/snmp"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all SNMP configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: SnmpView or List[SnmpView]

    def create(
        self,
        snmp_data: Dict[str, Any], # requestBody is BaseEntityView, but likely contains SnmpView fields
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Configures SNMP. (Corresponds to POST /snmp - OpId: createSnmpConfiguration)
        The API spec indicates a 200 OK response with the created SnmpView object.
        The requestBody schema is BaseEntityView, which might be a generic wrapper.
        Ensure snmp_data contains fields relevant to SnmpView for creation.

        Args:
            snmp_data (Dict[str, Any]): The data for the new SNMP configuration.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created SnmpView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/snmp"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /snmp supports them

        logger.info(f"Creating SNMP configuration with data: {snmp_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=snmp_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=snmp_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: SnmpView

    def update(
        self,
        identifier: str,
        snmp_data: Dict[str, Any], # requestBody is SnmpView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing SNMP configuration by its identifier.
        (Corresponds to PUT /snmp/{identifier} - OpId: updateSnmpConfigurationByIdentifier)
        The API spec indicates a 200 OK response with the updated SnmpView object.

        Args:
            identifier (str): The identifier of the SNMP configuration to update.
            snmp_data (Dict[str, Any]): The new data for the configuration (SnmpView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated SnmpView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/snmp/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        # Process any kwargs for query parameters if your API's PUT /snmp/{id} supports them

        logger.info(f"Updating SNMP configuration '{identifier}' with data: {snmp_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=snmp_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=snmp_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: SnmpView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes an SNMP configuration by its identifier.
        (Corresponds to DELETE /snmp/{identifier} - OpId: deleteSnmpConfigurationByIdentifier)
        The API spec indicates a 200 OK response with the deleted SnmpView object.

        Args:
            identifier (str): The identifier of the SNMP configuration to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted SnmpView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/snmp/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        # Process any kwargs for query parameters if your API's DELETE /snmp/{id} supports them

        logger.info(f"Deleting SNMP configuration '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: SnmpView

    def test_snmp_notification_by_address(
        self,
        address: str,
        monitor_task: bool = False, # Default endpoint, likely synchronous test
        task_timeout_seconds: int = 120
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Default response is empty object {}
        """
        Tests SNMP notification to a specified address.
        (Corresponds to POST /snmp/test/{address} - OpId: testSnmpNotificationByAddress)
        The API spec indicates a default response (empty object), suggesting a synchronous test.

        Args:
            address (str): The address to send the test SNMP notification to.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.

        Returns:
            An empty dictionary if successful and not monitoring, or task ID/result if monitoring.
            None on failure.
        """
        path = f"/snmp/test/{address}"
        logger.info(f"Testing SNMP notification to address: {address}")
        # No query parameters or request body defined in spec for this POST
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST",
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=path, method="POST")
            return self.api_client.read_and_parse_json_body(response) # Expected: {}
