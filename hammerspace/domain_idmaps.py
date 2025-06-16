# hammerspace/domain_idmaps.py
import logging
from typing import Optional, List, Dict, Any, Union
# from .client import HammerspaceApiClient # For standalone testing

logger = logging.getLogger(__name__)

class DomainIdmapsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(identifier: Optional[str] = None, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Get all LDAP ID maps. (GET /domain-idmaps)
        Operation ID: listDomainIdmaps
        """
        query_params = {}
        if identifier:
            path = f"/domain-idmaps/{identifier}" 
            logger.warning( f"get_share by id: Attempting GET from '{path}'. ")
            # If GET /domain-idmaps/{id} has query params, process kwargs here
        else:
            path = "/domain-idmaps"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        
        logger.info(f"Listing domain ID maps with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_domain_idmap(
        self, idmap_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Create LDAP ID map. (POST /domain-idmaps)
        Operation ID: createDomainIdmap
        Assuming 200 OK or 202 Accepted.
        """
        path = "/domain-idmaps"
        logger.info(f"Creating domain ID map with data: {idmap_data}")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            initial_json_data=idmap_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def reload_domain_idmaps(self, monitor_task: bool = True, task_timeout_seconds: int = 120) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Reload domain mapping rules. (POST /domain-idmaps/reload)
        Operation ID: reloadDomainIdmaps
        OpenAPI shows 200 response, but reload operations can sometimes be async.
        """
        path = "/domain-idmaps/reload"
        logger.info("Reloading domain ID maps.")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def update_domain_idmap(
        self, identifier: str, idmap_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update LDAP ID map. (PUT /domain-idmaps/{identifier})
        Operation ID: updateDomainIdmapByIdentifier
        """
        path = f"/domain-idmaps/{identifier}"
        logger.info(f"Updating domain ID map '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="PUT",
            initial_json_data=idmap_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def delete_domain_idmap(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Delete LDAP ID map. (DELETE /domain-idmaps/{identifier})
        Operation ID: deleteDomainIdmapByIdentifier
        """
        path = f"/domain-idmaps/{identifier}"
        logger.info(f"Deleting domain ID map '{identifier}'.")
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="DELETE",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )