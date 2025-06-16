# hammerspace/static_routes.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class StaticRoutesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the StaticRoutesClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client
        logger.info("StaticRoutesClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all static routes or a specific static route by its identifier.

        If 'identifier' is provided, fetches a single static route.
        (Corresponds to GET /static-routes/{identifier} - OpId: getStaticRouteByIdentifier)
        Note: The GET /static-routes/{identifier} endpoint in the provided spec
              does not list any query parameters, so kwargs are ignored if an
              identifier is provided for this specific call.

        Otherwise, lists all static routes.
        (Corresponds to GET /static-routes - OpId: listStaticRoutes)
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/static-routes/{identifier}"
            logger.info(f"Getting static route by identifier: {identifier}")
            # No query parameters are defined for GET /static-routes/{identifier} in the spec.
        else:
            path = "/static-routes"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all static routes with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: StaticRouteView or List[StaticRouteView]

    def create(
        self,
        route_data: Dict[str, Any],
        monitor_task: bool = True, # Defaulting to True as network changes can take time/be async
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new static route.
        (Corresponds to POST /static-routes - OpId: createStaticRoute)
        The API spec indicates a 200 OK response with the created object, but network
        configurations can sometimes be asynchronous.

        Args:
            route_data (Dict[str, Any]): The data for the new static route (StaticRouteView schema).
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created StaticRouteView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/static-routes"
        query_params = {} # No query parameters defined in spec for this POST
        # Process any kwargs for query parameters if your API's POST /static-routes supports them

        logger.info(f"Creating static route with data: {route_data}")
        # Even if spec says 200, network changes often benefit from task monitoring pattern
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=route_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self,
        identifier: str,
        route_data: Dict[str, Any],
        monitor_task: bool = True, # Defaulting to True
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing static route by its identifier.
        (Corresponds to PUT /static-routes/{identifier} - OpId: updateStaticRouteByIdentifier)
        The API spec indicates a 200 OK response with the updated object.

        Args:
            identifier (str): The identifier of the static route to update.
            route_data (Dict[str, Any]): The new data for the route (StaticRouteView schema).
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated StaticRouteView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/static-routes/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        # Process any kwargs for query parameters if your API's PUT /static-routes/{id} supports them

        logger.info(f"Updating static route '{identifier}' with data: {route_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=route_data, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self,
        identifier: str,
        monitor_task: bool = True, # Defaulting to True
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a static route by its identifier.
        (Corresponds to DELETE /static-routes/{identifier} - OpId: deleteStaticRouteByIdentifier)
        The API spec indicates a 200 OK response with the deleted object (or perhaps empty).

        Args:
            identifier (str): The identifier of the static route to delete.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted StaticRouteView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/static-routes/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        # Process any kwargs for query parameters if your API's DELETE /static-routes/{id} supports them

        logger.info(f"Deleting static route '{identifier}'")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
