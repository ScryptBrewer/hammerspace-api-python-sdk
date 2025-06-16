# hammerspace/sites.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class SitesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the SitesClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client
        logger.info("SitesClient initialized.")

    def get(
        self,
        identifier: Optional[str] = None,
        local: Optional[bool] = False,
        discover_address: Optional[str] = None,
        # Parameters for GET /sites/{identifier}
        type_query: Optional[str] = None,
        # Parameters for GET /sites/discover/{address}
        sync: Optional[bool] = None,
        validate_replication_ports: Optional[bool] = None,
        # Parameters for GET /sites (list all)
        spec: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        page_sort: Optional[str] = None,
        page_sort_dir: Optional[str] = None,
        **kwargs  # For any other potential future pass-throughs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Unified method to get site information.
        - If 'identifier' is provided, fetches a specific site.
        - If 'local' is True, fetches the local site.
        - If 'discover_address' is provided, discovers a remote site.
        - Otherwise, lists all sites with optional filtering and pagination.

        Order of precedence if multiple exclusive flags are set:
        1. identifier
        2. local
        3. discover_address
        4. list all

        Args:
            identifier (str, optional): The ID of a specific site to retrieve.
            local (bool, optional): If True, fetch the local site. Defaults to False.
            discover_address (str, optional): Management address to discover a remote site.
            type_query (str, optional): Query parameter 'type' for GET /sites/{identifier}.
            sync (bool, optional): For discover_remote_site: If true, synchronize.
            validate_replication_ports (bool, optional): For discover_remote_site: Test ports.
            spec (str, optional): For list_sites: Filter predicate.
            page (int, optional): For list_sites: Zero-based page number.
            page_size (int, optional): For list_sites: Elements per page.
            page_sort (str, optional): For list_sites: Field to sort on.
            page_sort_dir (str, optional): For list_sites: 'asc' or 'desc'.

        Returns:
            A list of site objects, a single site object, or an error dictionary.
        """
        path = ""
        query_params = {}
        method = "GET" # All these are GET requests

        if identifier:
            path = f"/sites/{identifier}"
            if type_query is not None:
                query_params["type"] = type_query
            logger.info(
                f"Getting site by identifier: {identifier} "
                f"with query_params: {query_params}"
            )
        elif local:
            path = "/sites/local"
            logger.info("Getting local site information.")
            # No specific query params for /sites/local from spec
        elif discover_address:
            path = f"/sites/discover/{discover_address}"
            if sync is not None:
                query_params["sync"] = sync
            if validate_replication_ports is not None:
                query_params["validateReplicationPorts"] = validate_replication_ports
            logger.info(
                f"Discovering remote site at address: {discover_address} "
                f"with query_params: {query_params}"
            )
        else: # Default to listing all sites
            path = "/sites"
            if spec is not None: query_params["spec"] = spec
            if page is not None: query_params["page"] = page
            if page_size is not None: query_params["page.size"] = page_size
            if page_sort is not None: query_params["page.sort"] = page_sort
            if page_sort_dir is not None: query_params["page.sort.dir"] = page_sort_dir
            logger.info(f"Listing all sites with query params: {query_params}")

        response = self.api_client.make_rest_call(
            path=path, method=method, query_params=query_params
        )
        return self.api_client.read_and_parse_json_body(response)

    def add_remote_site(
        self,
        remote_site_data: Dict[str, Any],
        monitor_task: bool = True, # Assuming this might be a task
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add a new remote site. (POST /sites - OpId: addRemoteSite)

        Args:
            remote_site_data (Dict[str, Any]): Data for the new remote site.
                                               Schema: RemoteSiteView
            monitor_task (bool): Whether to monitor if the operation is async.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            The created site view object, task ID, or an error dictionary.
        """
        path = "/sites"
        logger.info(f"Adding remote site with data: {remote_site_data}")
        # POST /sites in spec does not list query parameters
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            initial_json_data=remote_site_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def update_site(
        self,
        identifier: str,
        site_data: Dict[str, Any],
        monitor_task: bool = True, # Assuming this might be a task
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update a site. (PUT /sites/{identifier} - OpId: put)

        Args:
            identifier (str): The ID of the site to update.
            site_data (Dict[str, Any]): Data to update the site with.
                                        Schema: SiteView
            monitor_task (bool): Whether to monitor if the operation is async.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            The updated site view object, task ID, or an error dictionary.
        """
        path = f"/sites/{identifier}"
        logger.info(f"Updating site '{identifier}' with data: {site_data}")
        # PUT /sites/{identifier} in spec does not list query parameters
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="PUT",
            initial_json_data=site_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def delete_remote_site(
        self,
        identifier: str,
        monitor_task: bool = True, # Assuming this might be a task
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Remove a remote site. (DELETE /sites/{identifier} - OpId: delete)

        Args:
            identifier (str): The ID of the remote site to remove.
            monitor_task (bool): Whether to monitor if the operation is async.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            A command result view object, task ID, or an error dictionary.
        """
        path = f"/sites/{identifier}"
        logger.info(f"Deleting remote site '{identifier}'.")
        # DELETE /sites/{identifier} in spec does not list query parameters
        return self.api_client.execute_and_monitor__task(
            path=path,
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )
    # --- (Assuming they are still needed as separate operations) ---

    def add_remote_site(
        self,
        remote_site_data: Dict[str, Any],
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add a new remote site. (POST /sites - OpId: addRemoteSite)
        """
        path = "/sites"
        logger.info(f"Adding remote site with data: {remote_site_data}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            initial_json_data=remote_site_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def update_site(
        self,
        identifier: str,
        site_data: Dict[str, Any],
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update a site. (PUT /sites/{identifier} - OpId: put)
        """
        path = f"/sites/{identifier}"
        logger.info(f"Updating site '{identifier}' with data: {site_data}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="PUT",
            initial_json_data=site_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def delete_remote_site(
        self,
        identifier: str,
        monitor_task: bool = True,
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Remove a remote site. (DELETE /sites/{identifier} - OpId: delete)
        """
        path = f"/sites/{identifier}"
        logger.info(f"Deleting remote site '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )
