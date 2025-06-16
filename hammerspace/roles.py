# hammerspace/roles.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class RolesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all roles or a specific one by its identifier.

        If 'identifier' is provided, fetches a single role.
        (Corresponds to GET /roles/{identifier} - OpId: listRolesByIdentifier)

        Otherwise, lists all roles.
        (Corresponds to GET /roles - OpId: listRoles)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /roles/{id} has no query params in spec
        if identifier:
            path = f"/roles/{identifier}"
            logger.info(f"Getting role by identifier: {identifier}")
        else:
            path = "/roles"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing roles with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_role(
        self, role_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create role. (POST /roles) - OpId: createRoles"""
        path = "/roles"
        logger.info(f"Creating role with data: {role_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=role_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update_role(
        self, identifier: str, role_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update role. (PUT /roles/{identifier}) - OpId: updateRolesByIdentifier"""
        path = f"/roles/{identifier}"
        logger.info(f"Updating role '{identifier}' with data: {role_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=role_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_role(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete role. (DELETE /roles/{identifier}) - OpId: deleteRolesByIdentifier"""
        path = f"/roles/{identifier}"
        logger.info(f"Deleting role '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
