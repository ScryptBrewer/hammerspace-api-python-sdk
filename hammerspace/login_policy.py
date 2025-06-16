# hammerspace/login_policy.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class LoginPolicyClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all login policies or a specific one by its identifier.

        If 'identifier' is provided, fetches a single login policy.
        (Corresponds to GET /login-policy/{identifier} - OpId: getLoginPolicyByIdentifier)

        Otherwise, lists all login policies.
        (Corresponds to GET /login-policy - OpId: listLoginPolicies)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /login-policy/{id} has no query params in spec
        if identifier:
            path = f"/login-policy/{identifier}"
            logger.info(f"Getting login policy by identifier: {identifier}")
        else:
            path = "/login-policy"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing login policies with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self, policy_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create a login policy. (POST /login-policy) - OpId: createLoginPolicy"""
        path = "/login-policy"
        logger.info(f"Creating login policy with data: {policy_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=policy_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self, identifier: str, policy_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update a login policy. (PUT /login-policy/{identifier}) - OpId: updateLoginPolicyByIdentifier"""
        path = f"/login-policy/{identifier}"
        logger.info(f"Updating login policy '{identifier}' with data: {policy_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=policy_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete a login policy. (DELETE /login-policy/{identifier}) - OpId: deleteLoginPolicyByIdentifier"""
        path = f"/login-policy/{identifier}"
        logger.info(f"Deleting login policy '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
