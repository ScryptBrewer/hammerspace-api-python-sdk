# hammerspace/schedules.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class SchedulesClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all snapshot schedules or a specific one by its identifier.

        If 'identifier' is provided, fetches a single snapshot schedule.
        (Corresponds to GET /schedules/{identifier} - OpId: getSchedulesByIdentifier)

        Otherwise, lists all snapshot schedules.
        (Corresponds to GET /schedules - OpId: listSchedules)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /schedules/{id} has no query params in spec
        if identifier:
            path = f"/schedules/{identifier}"
            logger.info(f"Getting snapshot schedule by identifier: {identifier}")
        else:
            path = "/schedules"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing snapshot schedules with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_schedule( # Renamed from createSchedules
        self, schedule_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create snapshot schedule. (POST /schedules) - OpId: createSchedules"""
        path = "/schedules"
        logger.info(f"Creating snapshot schedule with data: {schedule_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=schedule_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update_schedule( 
        self, identifier: str, schedule_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update snapshot schedule. (PUT /schedules/{identifier}) - OpId: updateSchedulesByIdentifier"""
        path = f"/schedules/{identifier}"
        logger.info(f"Updating snapshot schedule '{identifier}' with data: {schedule_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=schedule_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_schedule(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete snapshot schedule. (DELETE /schedules/{identifier}) - OpId: deleteSchedulesByIdentifier"""
        path = f"/schedules/{identifier}"
        logger.info(f"Deleting snapshot schedule '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
