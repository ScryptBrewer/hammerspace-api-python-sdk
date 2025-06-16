# hammerspace/share_participants.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class ShareParticipantsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all share participants or a specific one by its identifier.

        If 'identifier' is provided, fetches a single share participant.
        (Corresponds to GET /share-participants/{identifier} - OpId: getShareParticipantsByIdentifier)

        Otherwise, lists all share participants.
        (Corresponds to GET /share-participants - OpId: listShareParticipantsByIdentifier - Note: OpId is reused)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /share-participants/{id} has no query params in spec
        if identifier:
            path = f"/share-participants/{identifier}"
            logger.info(f"Getting share participant by identifier: {identifier}")
        else:
            path = "/share-participants"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing share participants with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_share_participant( # Renamed from createShareParticipants
        self, participant_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Returns 202 Accepted (empty body)
        """
        Adds a new GFS participant to a share. (POST /share-participants) - OpId: createShareParticipants
        """
        path = "/share-participants"
        logger.info(f"Creating share participant with data: {participant_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=participant_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def change_admin_state_for_share_participants( # Renamed from changeAdminStateShareParticipants
        self, monitor_task: bool = True, task_timeout_seconds: int = 120, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Default response (empty object)
        """
        Update adminState for share participants which match criteria. (PUT /share-participants/change-admin-state)
        OpId: changeAdminStateShareParticipants
        Optional kwargs for query parameters:
            state (str), site (str), share (str)
        """
        path = "/share-participants/change-admin-state"
        query_params = {}
        if "state" in kwargs: query_params["state"] = kwargs["state"]
        if "site" in kwargs: query_params["site"] = kwargs["site"]
        if "share" in kwargs: query_params["share"] = kwargs["share"]
        logger.info(f"Changing admin state for share participants with query params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update_share_participant( 
        self, identifier: str, participant_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update a share participant. (PUT /share-participants/{identifier}) - OpId: updateShareParticipantsByIdentifier
        Only adminState, comment, and extendedInfo may be changed.
        """
        path = f"/share-participants/{identifier}"
        logger.info(f"Updating share participant '{identifier}' with data: {participant_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=participant_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_share_participant(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Returns 202 Accepted (empty body)
        """
        Removes a GFS participant from a share by its direct ID.
        (DELETE /share-participants/{identifier}) - OpId: deleteShareParticipantsByIdentifier
        Optional kwargs for query parameters:
            ignore_remove_failures (bool): (API name: ignoreRemoveFailures)
            force_master_acquisition (bool): (API name: forceMasterAcquisition)
        """
        path = f"/share-participants/{identifier}"
        query_params = {}
        if "ignore_remove_failures" in kwargs:
            query_params["ignoreRemoveFailures"] = str(kwargs["ignore_remove_failures"]).lower()
        if "force_master_acquisition" in kwargs:
            query_params["forceMasterAcquisition"] = str(kwargs["force_master_acquisition"]).lower()
        logger.info(f"Deleting share participant '{identifier}' with query params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def remove_share_participant_by_share_and_site( 
        self, share_identifier: str, site_identifier: str,
        monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Returns 202 Accepted (empty body)
        """
        Removes a GFS participant from a share using share and site identifiers.
        (DELETE /share-participants/{share-identifier}/{site-identifier}) - OpId: removeShareParticipantsByShareSiteIdentifier
        Optional kwargs for query parameters:
            ignore_remove_failures (bool): (API name: ignoreRemoveFailures)
            force_master_acquisition (bool): (API name: forceMasterAcquisition)
        """
        path = f"/share-participants/{share_identifier}/{site_identifier}"
        query_params = {}
        if "ignore_remove_failures" in kwargs:
            query_params["ignoreRemoveFailures"] = str(kwargs["ignore_remove_failures"]).lower()
        if "force_master_acquisition" in kwargs:
            query_params["forceMasterAcquisition"] = str(kwargs["force_master_acquisition"]).lower()
        logger.info(f"Removing share participant for share '{share_identifier}', site '{site_identifier}' with query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
