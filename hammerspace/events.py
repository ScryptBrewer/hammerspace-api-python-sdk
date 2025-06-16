# hammerspace/events.py
import logging
from typing import Optional, List, Dict, Any, Union
# from .client import HammerspaceApiClient

logger = logging.getLogger(__name__)

class EventsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all events or a specific event by its identifier.

        If 'identifier' is provided, fetches a single event.
        (Corresponds to GET /events/{identifier} - OpId: getEventByIdentifier)

        Otherwise, lists all events.
        (Corresponds to GET /events - OpId: listEvents)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {}
        if identifier:
            path = f"/events/{identifier}"
            logger.info(f"Getting event by ID: {identifier}")
        else:
            path = "/events"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing events with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def clear(self, monitor_task: bool = True, task_timeout_seconds: int = 120) -> Union[Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Clears events. (PUT /events/clear) - Operation ID: clearEvents
        OpenAPI shows 200, but a PUT action could be async.
        """
        path = "/events/clear"
        logger.info("Clearing events.")
        return self.api_client.execute_and_monitor_task(
            path=path, 
            method="PUT",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )

    def get_summary(
        self,
        group_by: str = "type",  
        spec: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        page_sort: Optional[str] = None,
        page_sort_dir: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get event counts grouped by given field.
        (GET /events/summary) - Operation ID: getEventsSummary
        'group_by' defaults to "type" if not provided.
        """
        path = "/events/summary"
        query_params = {}
        # groupBy is now always included, using the default or user-provided value
        query_params["groupBy"] = group_by
        
        if spec is not None: query_params["spec"] = spec
        if page is not None: query_params["page"] = page
        if page_size is not None: query_params["page.size"] = page_size
        if page_sort is not None: query_params["page.sort"] = page_sort
        if page_sort_dir is not None: query_params["page.sort.dir"] = page_sort_dir
        
        logger.info(f"Getting events summary with params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def update_event(
        self, identifier: str, event_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 120
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update an event. (PUT /events/{identifier}) - Operation ID: updateEventByIdentifier
        OpenAPI shows "default" response (empty object). Assuming it can be async.
        """
        path = f"/events/{identifier}"
        logger.info(f"Updating event ID: {identifier} with data: {event_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, 
            method="PUT", 
            initial_json_data=event_data,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        )