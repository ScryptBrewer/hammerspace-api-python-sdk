# hammerspace/labels.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class LabelsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all labels or a specific one by its identifier.

        If 'identifier' is provided, fetches a single label.
        (Corresponds to GET /labels/{identifier} - OpId: getLabelByIdentifier)

        Otherwise, lists all labels.
        (Corresponds to GET /labels - OpId: listLabels)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /labels/{id} has no query params in spec
        if identifier:
            path = f"/labels/{identifier}"
            logger.info(f"Getting label by identifier: {identifier}")
        else:
            path = "/labels"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all labels with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_label(
        self, label_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create a label. (POST /labels) - OpId: createLabel"""
        path = "/labels"
        logger.info(f"Creating label with data: {label_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=label_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self, identifier: str, label_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update a label. (PUT /labels/{identifier}) - OpId: updateLabelByIdentifier"""
        path = f"/labels/{identifier}"
        logger.info(f"Updating label '{identifier}' with data: {label_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=label_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Remove a label. (DELETE /labels/{identifier}) - OpId: deleteLabelByIdentifier"""
        path = f"/labels/{identifier}"
        logger.info(f"Deleting label '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
