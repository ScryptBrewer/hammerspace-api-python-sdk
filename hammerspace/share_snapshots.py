# hammerspace/share_snapshots.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class ShareSnapshotsClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get_snapshot_schedules( # Renamed from listShareSnapshots for clarity
        self, **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """
        List all share scheduled snapshots (schedules).
        (GET /share-snapshots) - OpId: listShareSnapshots
        Optional kwargs: spec (str), page (int), page_size (int),
                         page_sort (str), page_sort_dir (str)
        """
        path = "/share-snapshots"
        query_params = {}
        if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
        if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        logger.info(f"Listing share snapshot schedules with effective query params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_snapshot_schedule( # Renamed from createShareSnapshots
        self, schedule_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Create share snapshot schedule. (POST /share-snapshots) - OpId: createShareSnapshots"""
        path = "/share-snapshots"
        logger.info(f"Creating share snapshot schedule with data: {schedule_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=schedule_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def clone_share_snapshot( # Renamed from cloneCreateShareSnapshotsByIdentifier
        self, share_identifier_path: str, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Returns 202 Accepted
        """
        Clone share snapshot. (POST /share-snapshots/clone-create/{share-identifier})
        OpId: cloneCreateShareSnapshotsByIdentifier
        Args:
            share_identifier_path (str): Identifier of the share (path parameter).
        Optional kwargs for query parameters:
            snapshot_name (str): (API name: snapshot-name)
            destination_path (str): (API name: destination-path)
            overwrite_destination (bool): (API name: overwrite-destination)
        """
        path = f"/share-snapshots/clone-create/{share_identifier_path}"
        query_params = {}
        if "snapshot_name" in kwargs: query_params["snapshot-name"] = kwargs["snapshot_name"]
        if "destination_path" in kwargs: query_params["destination-path"] = kwargs["destination_path"]
        if "overwrite_destination" in kwargs:
            query_params["overwrite-destination"] = str(kwargs["overwrite_destination"]).lower()
        logger.info(f"Cloning share snapshot for share '{share_identifier_path}' with query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def create_immediate_share_snapshot( # Renamed from CreateShareSnapshotsByIdentifier
        self, share_identifier_path: str, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[str]]: # Returns string (snapshot name) or task ID
        """
        Create immediate share snapshot. (POST /share-snapshots/snapshot-create/{share-identifier})
        OpId: CreateShareSnapshotsByIdentifier
        Args:
            share_identifier_path (str): Identifier of the share (path parameter).
        Optional kwargs for query parameters:
            snapshot_name (str): (API name: snapshot-name)
        """
        path = f"/share-snapshots/snapshot-create/{share_identifier_path}"
        query_params = {}
        if "snapshot_name" in kwargs: query_params["snapshot-name"] = kwargs["snapshot_name"]
        logger.info(f"Creating immediate share snapshot for share '{share_identifier_path}' with query: {query_params}")
        # This endpoint returns a string directly (snapshot name) on 200, or could be async.
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_share_snapshot( # Renamed from DeleteSnapshotShareSnapshotsByIdentifier
        self, share_identifier_path: str, snapshot_name_path: str,
        monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[List[Dict[str, Any]]]]: # Returns array of CommandResultView or task ID
        """
        Delete share snapshot. (POST /share-snapshots/snapshot-delete/{share-identifier}/{snapshot-name})
        OpId: DeleteSnapshotShareSnapshotsByIdentifier
        """
        path = f"/share-snapshots/snapshot-delete/{share_identifier_path}/{snapshot_name_path}"
        logger.info(f"Deleting share snapshot '{snapshot_name_path}' for share '{share_identifier_path}'.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", # Note: DELETE action via POST
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def list_share_snapshots_for_share(self, share_identifier_path: str) -> Optional[List[str]]: # Renamed
        """
        List share snapshots for a specific share. (GET /share-snapshots/snapshot-list/{share-identifier})
        OpId: ListShareSnapshotsByShareIdentifier
        """
        path = f"/share-snapshots/snapshot-list/{share_identifier_path}"
        logger.info(f"Listing snapshots for share '{share_identifier_path}'.")
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response) # Returns array of strings

    def restore_files_from_share_snapshot( # Renamed from createRestoreShareSnapshotsByShareSnapshotIdentifier
        self, share_identifier_path: str, snapshot_name_path: str,
        monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[List[Dict[str, Any]]]]: # Returns array of CommandResultView or task ID
        """
        Restore files from share snapshot. (POST /share-snapshots/snapshot-restore-files/{share-identifier}/{snapshot-name})
        OpId: createRestoreShareSnapshotsByShareSnapshotIdentifier
        Optional kwargs for query parameters:
            filename (str): (API name: filename)
        """
        path = f"/share-snapshots/snapshot-restore-files/{share_identifier_path}/{snapshot_name_path}"
        query_params = {}
        if "filename" in kwargs: query_params["filename"] = kwargs["filename"]
        logger.info(f"Restoring files from snapshot '{snapshot_name_path}' for share '{share_identifier_path}', query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def restore_entire_share_from_snapshot(
        self, share_identifier_path: str, snapshot_name_path: str,
        monitor_task: bool = True, task_timeout_seconds: int = 600 # Potentially long operation
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Returns 202 Accepted
        """
        Restore entire share from a snapshot. (POST /share-snapshots/snapshot-restore/{share-identifier}/{snapshot-name})
        OpId: restoreRestoreShareSnapshotsByShareSnapshotIdentifier
        """
        path = f"/share-snapshots/snapshot-restore/{share_identifier_path}/{snapshot_name_path}"
        logger.info(f"Restoring entire share '{share_identifier_path}' from snapshot '{snapshot_name_path}'.")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update_snapshot_schedule( 
        self, identifier: str, schedule_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update share snapshot schedule. (PUT /share-snapshots/{identifier}) - OpId: updateShareSnapshotsByIdentifier"""
        path = f"/share-snapshots/{identifier}" # This refers to the schedule ID
        logger.info(f"Updating share snapshot schedule '{identifier}' with data: {schedule_data}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=schedule_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete_snapshot_schedule(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Delete share snapshot schedule. (DELETE /share-snapshots/{identifier}) - OpId: deleteShareSnapshotsSheduleByIdentifier
        Optional kwargs for query parameters:
            clear_snapshots (bool): (API name: clear-snapshots)
        """
        path = f"/share-snapshots/{identifier}" # This refers to the schedule ID
        query_params = {}
        if "clear_snapshots" in kwargs: query_params["clear-snapshots"] = str(kwargs["clear_snapshots"]).lower()
        logger.info(f"Deleting share snapshot schedule '{identifier}' with query: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
