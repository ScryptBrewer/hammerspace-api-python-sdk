# hammerspace/objectives.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class ObjectivesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all objectives or a specific one by its identifier.

        If 'identifier' is provided, fetches a single objective.
        (Corresponds to GET /objectives/{identifier} - OpId: listObjectivesByIdentifier)

        Otherwise, lists all objectives.
        (Corresponds to GET /objectives - OpId: listObjectives)
        Optional kwargs for listing: hide_tech_preview (bool), spec (str), page (int),
                                     page_size (int), page_sort (str), page_sort_dir (str)
        """
        query_params = {}
        if identifier:
            path = f"/objectives/{identifier}"
            logger.info(f"Getting objective by identifier: {identifier}")
            # GET /objectives/{id} has no query params in spec
        else:
            path = "/objectives"
            if "hide_tech_preview" in kwargs:
                query_params["hideTechPreview"] = str(kwargs["hide_tech_preview"]).lower()
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing objectives with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create(
        self, objective_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create objective. (POST /objectives) - OpId: createObjectives"""
        path = "/objectives"
        logger.info(f"Creating objective with data: {objective_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=objective_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def export(
        self, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Export objectives. (POST /objectives/export) - OpId: exportObjectivesObjectives
        Optional kwargs for query parameters:
            uuid (str), name (str), target (str)
        """
        path = "/objectives/export"
        query_params = {}
        if "uuid" in kwargs: query_params["uuid"] = kwargs["uuid"]
        if "name" in kwargs: query_params["name"] = kwargs["name"]
        if "target" in kwargs: query_params["target"] = kwargs["target"]
        logger.info(f"Exporting objectives with query params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Returns ObjectiveView

    def find_matching_volumes_for_objective(
        self, objective_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Find matching volumes for an objective. (POST /objectives/findMatchingVolumes)
        OpId: findMatchingVolumesObjectives
        """
        path = "/objectives/findMatchingVolumes"
        logger.info(f"Finding matching volumes for objective. Body: {objective_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=objective_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Returns array of ObjectiveView

    def import_objectives(
        self, objectives_data_array: List[Dict[str, Any]], # requestBody is array
        monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Import objectives. (POST /objectives/import) - OpId: importObjectivesObjectives
        objectives_data_array: The main request body (array of ObjectiveView).
        Optional kwargs for query parameters:
            source (str), name (str), prefix (str), merge (bool), insecure (bool)
        """
        path = "/objectives/import"
        query_params = {}
        if "source" in kwargs: query_params["source"] = kwargs["source"]
        if "name" in kwargs: query_params["name"] = kwargs["name"]
        if "prefix" in kwargs: query_params["prefix"] = kwargs["prefix"]
        if "merge" in kwargs: query_params["merge"] = str(kwargs["merge"]).lower()
        if "insecure" in kwargs: query_params["insecure"] = str(kwargs["insecure"]).lower()
        logger.info(f"Importing objectives. Body: <array>, Query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=objectives_data_array, initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Default response (empty object)

    def validate_objective_expression(self, exp: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Validate objective expression. (GET /objectives/validate/{exp}) - OpId: validateObjectives
        Optional kwargs: hide_tech_preview (bool)
        """
        path = f"/objectives/validate/{exp}"
        query_params = {}
        if "hide_tech_preview" in kwargs:
            query_params["hideTechPreview"] = str(kwargs["hide_tech_preview"]).lower()
        logger.info(f"Validating objective expression '{exp}' with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Returns HammerscriptResponseView

    def update(
        self, identifier: str, objective_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update objective. (PUT /objectives/{identifier}) - OpId: updateObjectivesByIdentifier"""
        path = f"/objectives/{identifier}"
        logger.info(f"Updating objective '{identifier}'. Body: {objective_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=objective_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete objective. (DELETE /objectives/{identifier}) - OpId: deleteObjectivesByIdentifier"""
        path = f"/objectives/{identifier}"
        logger.info(f"Deleting objective '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
