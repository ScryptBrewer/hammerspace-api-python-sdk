# hammerspace/identity_group_mappings.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class IdentityGroupMappingsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the IdentityGroupMappingsClient.
        """
        self.api_client = api_client
        logger.info("IdentityGroupMappingsClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all identity group mappings or a specific mapping by its identifier.

        If 'identifier' is provided, fetches a single identity group mapping.
        (Corresponds to GET /identity-group-mappings/{identifier} - OpId: getIdentityGroupMappingByIdentifier)
        Note: The GET /identity-group-mappings/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all identity group mappings.
        (Corresponds to GET /identity-group-mappings - OpId: listIdentityGroupMappings)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/identity-group-mappings/{identifier}"
            logger.info(f"Getting identity group mapping by identifier: {identifier}")
            # No query parameters are defined for GET /identity-group-mappings/{identifier} in the spec.
        else:
            path = "/identity-group-mappings"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all identity group mappings with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        # Expected: IdentityGroupMappingView or List[IdentityGroupMappingView]
        return self.api_client.read_and_parse_json_body(response)

    def create_identity_group_mapping(
        self,
        mapping_data: Dict[str, Any], # requestBody is IdentityGroupMappingView
        monitor_task: bool = False, # Spec says 200 OK with IdentityGroupMappingView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new identity group mapping.
        (Corresponds to POST /identity-group-mappings - OpId: createIdentityGroupMapping)
        The API spec indicates a 200 OK response with the created IdentityGroupMappingView object.

        Args:
            mapping_data (Dict[str, Any]): Data for the new mapping (IdentityGroupMappingView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created IdentityGroupMappingView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/identity-group-mappings"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Creating identity group mapping with data: {mapping_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=mapping_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=mapping_data, query_params=query_params
            )
            # Expected: IdentityGroupMappingView
            return self.api_client.read_and_parse_json_body(response)

    def update(
        self,
        identifier: str,
        mapping_data: Dict[str, Any], # requestBody is IdentityGroupMappingView
        monitor_task: bool = False, # Spec says 200 OK with IdentityGroupMappingView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing identity group mapping by its identifier.
        (Corresponds to PUT /identity-group-mappings/{identifier} - OpId: updateIdentityGroupMappingByIdentifier)
        The API spec indicates a 200 OK response with the updated IdentityGroupMappingView object.

        Args:
            identifier (str): The identifier of the identity group mapping to update.
            mapping_data (Dict[str, Any]): New data for the mapping (IdentityGroupMappingView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated IdentityGroupMappingView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/identity-group-mappings/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating identity group mapping '{identifier}' with data: {mapping_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=mapping_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=mapping_data, query_params=query_params
            )
            # Expected: IdentityGroupMappingView
            return self.api_client.read_and_parse_json_body(response)

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK with IdentityGroupMappingView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes an identity group mapping by its identifier.
        (Corresponds to DELETE /identity-group-mappings/{identifier} - OpId: deleteIdentityGroupMappingByIdentifier)
        The API spec indicates a 200 OK response with the deleted IdentityGroupMappingView object (unusual for DELETE).

        Args:
            identifier (str): The identifier of the identity group mapping to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted IdentityGroupMappingView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/identity-group-mappings/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        
        logger.info(f"Deleting identity group mapping '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            # Expected: IdentityGroupMappingView
            return self.api_client.read_and_parse_json_body(response)
