# hammerspace/idp.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class IdpClient:
    def __init__(self, api_client: Any):
        """
        Initializes the IdpClient for managing Identity Provider configurations.
        """
        self.api_client = api_client
        logger.info("IdpClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all IdP configurations or a specific IdP configuration by its identifier.

        If 'identifier' is provided, fetches a single IdP configuration.
        (Corresponds to GET /idp/{identifier} - OpId: getIdpByIdentifier)
        Note: The GET /idp/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all IdP configurations.
        (Corresponds to GET /idp - OpId: listIdps)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/idp/{identifier}"
            logger.info(f"Getting IdP configuration by identifier: {identifier}")
            # No query parameters are defined for GET /idp/{identifier} in the spec.
        else:
            path = "/idp"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all IdP configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: IdpView or List[IdpView]

    def create_idp_configuration(
        self,
        idp_data: Dict[str, Any], # requestBody is IdpView
        monitor_task: bool = False, # Spec says 200 OK with IdpView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new IdP configuration.
        (Corresponds to POST /idp - OpId: createIdp)
        The API spec indicates a 200 OK response with the created IdpView object.

        Args:
            idp_data (Dict[str, Any]): The data for the new IdP configuration (IdpView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created IdpView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/idp"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Creating IdP configuration with data: {idp_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=idp_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=idp_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: IdpView

    def update(
        self,
        identifier: str,
        idp_data: Dict[str, Any], # requestBody is IdpView
        monitor_task: bool = False, # Spec says 200 OK with IdpView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing IdP configuration by its identifier.
        (Corresponds to PUT /idp/{identifier} - OpId: updateIdpByIdentifier)
        The API spec indicates a 200 OK response with the updated IdpView object.

        Args:
            identifier (str): The identifier of the IdP configuration to update.
            idp_data (Dict[str, Any]): The new data for the configuration (IdpView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated IdpView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/idp/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating IdP configuration '{identifier}' with data: {idp_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=idp_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=idp_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: IdpView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK with IdpView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes an IdP configuration by its identifier.
        (Corresponds to DELETE /idp/{identifier} - OpId: deleteIdpByIdentifier)
        The API spec indicates a 200 OK response with the deleted IdpView object (unusual for DELETE).

        Args:
            identifier (str): The identifier of the IdP configuration to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted IdpView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/idp/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        
        logger.info(f"Deleting IdP configuration '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: IdpView
