# hammerspace/file_snapshots.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class FileSnapshotsClient:
    def __init__(self, api_client: Any):
        """
        Initializes the FileSnapshotsClient.
        """
        self.api_client = api_client
        logger.info("FileSnapshotsClient initialized.")

    def get(
        self,
        **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """
        List all file snapshots.
        (Corresponds to GET /file-snapshots - OpId: list)

        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        path = "/file-snapshots"
        query_params = {}
        if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
        if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        logger.info(f"Listing all file snapshots with query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        # Expected: List[FileSnapshotView]
        return self.api_client.read_and_parse_json_body(response)

    def create_file_snapshot_with_body(
        self,
        snapshot_data: Dict[str, Any],
        monitor_task: bool = False, # Assuming this might be sync based on 200 OK
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Create file snapshot using a request body.
        (Corresponds to POST /file-snapshots - OpId: post)
        The API spec indicates a 200 OK response, suggesting it might be synchronous.
        If it can be asynchronous, set monitor_task=True.

        Args:
            snapshot_data (Dict[str, Any]): The file snapshot data (FileSnapshotView).
            monitor_task (bool): Whether to monitor if it's an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        """
        path = "/file-snapshots"
        logger.info(f"Creating file snapshot with body: {snapshot_data}")
        
        if monitor_task:
            # If you expect this to sometimes be async and return a task
            return self.api_client.execute_and_monitor_task(
                path=path,
                method="POST",
                initial_json_data=snapshot_data,
                monitor_task=monitor_task,
                task_timeout_seconds=task_timeout_seconds
            )
        else:
            # Standard synchronous call
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=snapshot_data
            )
            # Expected: FileSnapshotView
            return self.api_client.read_and_parse_json_body(response)

    def create_snapshot_with_filename_expression(
        self,
        filename_expression: Optional[str] = None,
        monitor_task: bool = True, # Default spec response suggests async
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Create file snapshot using a filename expression.
        (Corresponds to POST /file-snapshots/create - OpId: createSnapshot)
        The API spec indicates a 'default' response, often used for 202 Accepted.

        Args:
            filename_expression (Optional[str]): Expression to match filenames.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        """
        path_op = "/file-snapshots/create"
        query_params = {}
        if filename_expression is not None:
            query_params["filename-expression"] = filename_expression
        
        logger.info(f"Creating file snapshot with filename expression: {query_params.get('filename-expression')}")
        return self.api_client.execute_and_monitor_task(
            path=path_op,
            method="POST",
            initial_query_params=query_params,
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} or task result

    def delete_snapshot_with_expressions(
        self,
        filename_expression: Optional[str] = None,
        date_time_expression: Optional[str] = None,
        # monitor_task: bool = False, # Spec says 200 OK, implying sync
        # task_timeout_seconds: int = 300
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Delete file snapshot using filename and date-time expressions.
        (Corresponds to POST /file-snapshots/delete - OpId: deleteSnapshot)
        The API spec indicates a 200 OK response.

        Args:
            filename_expression (Optional[str]): Expression to match filenames.
            date_time_expression (Optional[str]): Expression to match date and time.
        """
        path_op = "/file-snapshots/delete"
        query_params = {}
        if filename_expression is not None:
            query_params["filename-expression"] = filename_expression
        if date_time_expression is not None:
            query_params["date-time-expression"] = date_time_expression
            
        logger.info(f"Deleting file snapshots with filename_expression: '{query_params.get('filename-expression')}' and date_time_expression: '{query_params.get('date-time-expression')}'")
        response = self.api_client.make_rest_call(
            path=path_op, method="POST", query_params=query_params
        )
        # Expected: List[CommandResultView]
        return self.api_client.read_and_parse_json_body(response)

    def list_snapshots_with_filename_expression(
        self,
        filename_expression: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get all file snapshots, optionally filtered by filename expression.
        (Corresponds to GET /file-snapshots/list - OpId: listSnapshots)

        Args:
            filename_expression (Optional[str]): Expression to filter snapshots by filename.
        """
        path = "/file-snapshots/list"
        query_params = {}
        if filename_expression is not None:
            query_params["filename-expression"] = filename_expression
        
        logger.info(f"Listing file snapshots with filename_expression: {query_params.get('filename-expression')}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        # Expected: List[FileStatView]
        return self.api_client.read_and_parse_json_body(response)

    def restore_file_from_snapshot(
        self,
        filename_expression: Optional[str] = None,
        date_time_expression: Optional[str] = None,
        # monitor_task: bool = False, # Spec says 200 OK, implying sync
        # task_timeout_seconds: int = 300
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Restore file from snapshot using filename and date-time expressions.
        (Corresponds to POST /file-snapshots/restore - OpId: restore)
        The API spec indicates a 200 OK response.

        Args:
            filename_expression (Optional[str]): Expression to match filenames.
            date_time_expression (Optional[str]): Expression to match date and time.
        """
        path_op = "/file-snapshots/restore"
        query_params = {}
        if filename_expression is not None:
            query_params["filename-expression"] = filename_expression
        if date_time_expression is not None:
            query_params["date-time-expression"] = date_time_expression

        logger.info(f"Restoring file from snapshot with filename_expression: '{query_params.get('filename-expression')}' and date_time_expression: '{query_params.get('date-time-expression')}'")
        response = self.api_client.make_rest_call(
            path=path_op, method="POST", query_params=query_params
        )
        # Expected: List[CommandResultView]
        return self.api_client.read_and_parse_json_body(response)

    def clone_file(
        self,
        file_source: str,
        file_destination: str,
        monitor_task: bool = True, # Default spec response suggests async
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]: # Assuming default response means empty or task result
        """
        Clone a file from the source to the destination path.
        (Corresponds to POST /file-snapshots/{file-source}/{file-destination} - OpId: clone)
        The API spec indicates a 'default' response.

        Args:
            file_source (str): Source file path.
            file_destination (str): Destination file path.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        """
        path = f"/file-snapshots/{file_source}/{file_destination}"
        logger.info(f"Cloning file from '{file_source}' to '{file_destination}'")
        # No query params or body defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path,
            method="POST",
            monitor_task=monitor_task,
            task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} or task result

    def get_file_snapshot(
        self,
        identifier: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a file snapshot by its identifier.
        (Corresponds to GET /file-snapshots/{identifier} - OpId: get)

        Args:
            identifier (str): The identifier of the file snapshot.
        """
        path = f"/file-snapshots/{identifier}"
        logger.info(f"Getting file snapshot by identifier: {identifier}")
        # No query parameters defined for this GET in the spec.
        response = self.api_client.make_rest_call(path=path, method="GET")
        # Expected: FileSnapshotView
        return self.api_client.read_and_parse_json_body(response)

    def update_file_snapshot(
        self,
        identifier: str,
        snapshot_data: Dict[str, Any], # FileSnapshotView
        monitor_task: bool = False, # Assuming this might be sync based on 200 OK
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update a file snapshot by its identifier.
        (Corresponds to PUT /file-snapshots/{identifier} - OpId: put)
        The API spec indicates a 200 OK response.

        Args:
            identifier (str): The identifier of the file snapshot.
            snapshot_data (Dict[str, Any]): The updated file snapshot data.
            monitor_task (bool): Whether to monitor if it's an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        """
        path = f"/file-snapshots/{identifier}"
        logger.info(f"Updating file snapshot '{identifier}' with data: {snapshot_data}")

        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path,
                method="PUT",
                initial_json_data=snapshot_data,
                monitor_task=monitor_task,
                task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=snapshot_data
            )
            # Expected: FileSnapshotView
            return self.api_client.read_and_parse_json_body(response)

    def delete_file_snapshot(
        self,
        identifier: str,
        monitor_task: bool = False, # Assuming this might be sync based on 200 OK
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a file snapshot by its identifier.
        (Corresponds to DELETE /file-snapshots/{identifier} - OpId: delete)
        The API spec indicates a 200 OK response.

        Args:
            identifier (str): The identifier of the file snapshot to delete.
            monitor_task (bool): Whether to monitor if it's an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        """
        path = f"/file-snapshots/{identifier}"
        logger.info(f"Deleting file snapshot '{identifier}'")

        if monitor_task:
             return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE",
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=path, method="DELETE")
            # Expected: FileSnapshotView (though delete often returns 204 No Content or the deleted object)
            # The spec says 200 with FileSnapshotView, so we'll parse it.
            return self.api_client.read_and_parse_json_body(response)
