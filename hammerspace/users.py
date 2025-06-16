# hammerspace/users.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class UsersClient:
    def __init__(self, api_client: Any):
        """
        Initializes the UsersClient.
        """
        self.api_client = api_client
        logger.info("UsersClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all users or a specific user by its identifier.

        If 'identifier' is provided, fetches a single user.
        (Corresponds to GET /users/{identifier} - OpId: getUserByIdentifier)
        Note: The GET /users/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all users.
        (Corresponds to GET /users - OpId: listUsers)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/users/{identifier}"
            logger.info(f"Getting user by identifier: {identifier}")
            # No query parameters are defined for GET /users/{identifier} in the spec.
        else:
            path = "/users"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all users with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: UserView or List[UserView]

    def create_user(
        self,
        user_data: Dict[str, Any], # requestBody is UserView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new user.
        (Corresponds to POST /users - OpId: createUser)
        The API spec indicates a 200 OK response with the created UserView object.

        Args:
            user_data (Dict[str, Any]): The data for the new user (UserView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created UserView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/users"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /users supports them

        logger.info(f"Creating user with data: {user_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=user_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=user_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: UserView

    def update(
        self,
        identifier: str,
        user_data: Dict[str, Any], # requestBody is UserView
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing user by its identifier.
        (Corresponds to PUT /users/{identifier} - OpId: updateUserByIdentifier)
        The API spec indicates a 200 OK response with the updated UserView object.

        Args:
            identifier (str): The identifier of the user to update.
            user_data (Dict[str, Any]): The new data for the user (UserView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated UserView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/users/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        # Process any kwargs for query parameters if your API's PUT /users/{id} supports them

        logger.info(f"Updating user '{identifier}' with data: {user_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=user_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=user_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: UserView

    def delete(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a user by its identifier.
        (Corresponds to DELETE /users/{identifier} - OpId: deleteUserByIdentifier)
        The API spec indicates a 200 OK response with the deleted UserView object.

        Args:
            identifier (str): The identifier of the user to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted UserView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/users/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        # Process any kwargs for query parameters if your API's DELETE /users/{id} supports them

        logger.info(f"Deleting user '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: UserView
