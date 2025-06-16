# hammerspace/user_groups.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class UserGroupsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the UserGroupsClient.
        """
        self.api_client = api_client
        logger.info("UserGroupsClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all user groups or a specific user group by its identifier.

        If 'identifier' is provided, fetches a single user group.
        (Corresponds to GET /user-groups/{identifier} - OpId: getUserGroupByIdentifier)
        Note: The GET /user-groups/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all user groups.
        (Corresponds to GET /user-groups - OpId: listUserGroups)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/user-groups/{identifier}"
            logger.info(f"Getting user group by identifier: {identifier}")
            # No query parameters are defined for GET /user-groups/{identifier} in the spec.
        else:
            path = "/user-groups"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all user groups with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: UserGroupView or List[UserGroupView]

    def create(
        self,
        group_data: Dict[str, Any], # requestBody is UserGroupView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new user group.
        (Corresponds to POST /user-groups - OpId: createUserGroup)
        The API spec indicates a 200 OK response with the created UserGroupView object.

        Args:
            group_data (Dict[str, Any]): The data for the new user group (UserGroupView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created UserGroupView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/user-groups"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /user-groups supports them

        logger.info(f"Creating user group with data: {group_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=group_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=group_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: UserGroupView

    def update(
        self,
        identifier: str,
        group_data: Dict[str, Any], # requestBody is UserGroupView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing user group by its identifier.
        (Corresponds to PUT /user-groups/{identifier} - OpId: updateUserGroupByIdentifier)
        The API spec indicates a 200 OK response with the updated UserGroupView object.

        Args:
            identifier (str): The identifier of the user group to update.
            group_data (Dict[str, Any]): The new data for the group (UserGroupView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated UserGroupView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/user-groups/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        # Process any kwargs for query parameters if your API's PUT /user-groups/{id} supports them

        logger.info(f"Updating user group '{identifier}' with data: {group_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=group_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=group_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: UserGroupView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a user group by its identifier.
        (Corresponds to DELETE /user-groups/{identifier} - OpId: deleteUserGroupByIdentifier)
        The API spec indicates a 200 OK response with the deleted UserGroupView object.

        Args:
            identifier (str): The identifier of the user group to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted UserGroupView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/user-groups/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        # Process any kwargs for query parameters if your API's DELETE /user-groups/{id} supports them

        logger.info(f"Deleting user group '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: UserGroupView
