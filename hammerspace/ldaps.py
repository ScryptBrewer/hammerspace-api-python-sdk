# hammerspace/ldaps.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class LdapsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all LDAP configurations or a specific one by its identifier.

        If 'identifier' is provided, fetches a single LDAP configuration.
        (Corresponds to GET /ldaps/{identifier} - OpId: getLdapConfigurationByIdentifier)

        Otherwise, lists all LDAP configurations.
        (Corresponds to GET /ldaps - OpId: listLdapConfiguration)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /ldaps/{id} has no query params in spec
        if identifier:
            path = f"/ldaps/{identifier}"
            logger.info(f"Getting LDAP configuration by identifier: {identifier}")
        else:
            path = "/ldaps"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing LDAP configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self, ldap_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Configure LDAP. (POST /ldaps) - OpId: createLdapConfiguration"""
        path = "/ldaps"
        logger.info(f"Creating LDAP configuration with data: {ldap_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=ldap_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self, identifier: str, ldap_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update LDAP configuration. (PUT /ldaps/{identifier}) - OpId: updateLdapConfigurationByIdentifier"""
        path = f"/ldaps/{identifier}"
        logger.info(f"Updating LDAP configuration '{identifier}' with data: {ldap_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=ldap_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete LDAP configuration. (DELETE /ldaps/{identifier}) - OpId: deleteLdapConfigurationByIdentifier"""
        path = f"/ldaps/{identifier}"
        logger.info(f"Deleting LDAP configuration '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
