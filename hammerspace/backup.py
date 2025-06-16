# hammerspace/backup.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class BackupClient:
    def __init__(self, api_client: Any):
        """
        Initializes the BackupClient.
        """
        self.api_client = api_client
        logger.info("BackupClient initialized using provided OpenAPI spec.")

    def get(self, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """
        Gets all backup configurations (schedules).
        (Corresponds to GET /backup - OpId: listBackupConfiguration)

        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        
        Returns:
            A list of backup configuration dictionaries (BackupView schema) or None on failure.
        """
        path = "/backup"
        query_params = {}
        if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
        if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        
        logger.info(f"Listing backup configurations with effective query params: {query_params}")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: List[BackupView]

    # Note: The OpenAPI spec does not define a GET /backup/{identifier} for a single schedule.
    # If it exists, a merged get() method would be appropriate.

    def create_backup_schedule(
        self,
        schedule_data: Dict[str, Any], # requestBody is BackupView
        monitor_task: bool = False, # Spec says 200 OK with BackupView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new backup schedule.
        (Corresponds to POST /backup - OpId: createBackupSchedule)
        The API spec indicates a 200 OK response with the created BackupView object.

        Args:
            schedule_data (Dict[str, Any]): Data for the new backup schedule (BackupView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this POST).

        Returns:
            The created BackupView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/backup"
        query_params = {} # No query parameters defined in spec for this POST
        
        logger.info(f"Creating backup schedule with data: {schedule_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=schedule_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=schedule_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: BackupView

    def update_backup_schedule(
        self,
        identifier: str,
        schedule_data: Dict[str, Any], # requestBody is BackupView
        monitor_task: bool = False, # Spec says 200 OK with BackupView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing backup schedule by its identifier.
        (Corresponds to PUT /backup/{identifier} - OpId: updateBackupScheduleByIdentifier)
        The API spec indicates a 200 OK response with the updated BackupView object.

        Args:
            identifier (str): The identifier of the backup schedule to update.
            schedule_data (Dict[str, Any]): New data for the schedule (BackupView schema).
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this PUT).

        Returns:
            The updated BackupView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/backup/{identifier}"
        query_params = {} # No query parameters defined in spec for this PUT
        
        logger.info(f"Updating backup schedule '{identifier}' with data: {schedule_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=schedule_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=schedule_data, query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: BackupView

    def delete_backup_schedule(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK with BackupView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a backup schedule by its identifier.
        (Corresponds to DELETE /backup/{identifier} - OpId: deleteBackupScheduleByIdentifier)
        The API spec indicates a 200 OK response with the deleted BackupView object (unusual for DELETE).

        Args:
            identifier (str): The identifier of the backup schedule to delete.
            monitor_task (bool): Whether to treat as an asynchronous task if it might be long-running.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Optional keyword arguments for query parameters (none defined in spec for this DELETE).

        Returns:
            The deleted BackupView (or confirmation) if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/backup/{identifier}"
        query_params = {} # No query parameters defined in spec for this DELETE
        
        logger.info(f"Deleting backup schedule '{identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: BackupView

    def create_immediate_backup(
        self,
        volume_ip: str,
        export_path: str,
        monitor_task: bool = True, # Default response {} suggests async
        task_timeout_seconds: int = 1800 # Backups can take time
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates an immediate backup for a specified volume and export path.
        (Corresponds to POST /backup/backup-create/{volume-ip}/{export-path} - OpId: createImmediateBackupByVolumeIpAndExportPath)

        Args:
            volume_ip (str): The IP address of the volume.
            export_path (str): The export path for the backup.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        # URL encoding might be needed for export_path if it contains special characters.
        # requests library usually handles this for path parameters.
        path = f"/backup/backup-create/{volume_ip}/{export_path.lstrip('/')}"
        logger.info(f"Creating immediate backup for volume_ip='{volume_ip}', export_path='{export_path}'")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def list_backups(
        self,
        volume_ip: str,
        export_path: str
    ) -> Optional[List[str]]:
        """
        Lists all backups for a specified volume and export path.
        (Corresponds to GET /backup/backup-list/{volume-ip}/{export-path} - OpId: listAllBackupsByVolumeIpAndExportPath)

        Args:
            volume_ip (str): The IP address of the volume.
            export_path (str): The export path.

        Returns:
            A list of backup names (strings) or None on failure.
        """
        path = f"/backup/backup-list/{volume_ip}/{export_path.lstrip('/')}"
        logger.info(f"Listing all backups for volume_ip='{volume_ip}', export_path='{export_path}'")
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response) # Expected: List[str]

    def restore_latest_backup(
        self,
        volume_ip: str,
        export_path: str,
        monitor_task: bool = True, # Default response {} suggests async
        task_timeout_seconds: int = 3600, # Restores can take significant time
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Restores the latest backup from a storage volume.
        (Corresponds to POST /backup/backup-restore/{volume-ip}/{export-path} - OpId: restoreLatestBackupByVolumeIpAndExportPath)

        Args:
            volume_ip (str): The IP address of the volume.
            export_path (str): The export path.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        Optional kwargs:
            cluster_uuid (str): (API name: cluster-uuid)

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = f"/backup/backup-restore/{volume_ip}/{export_path.lstrip('/')}"
        query_params = {}
        if "cluster_uuid" in kwargs: query_params["cluster-uuid"] = kwargs["cluster_uuid"]
        
        logger.info(f"Restoring latest backup for volume_ip='{volume_ip}', export_path='{export_path}' with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def restore_backup_by_name(
        self,
        volume_ip: str,
        export_path: str,
        backup_name: str,
        monitor_task: bool = True, # Default response {} suggests async
        task_timeout_seconds: int = 3600, # Restores can take significant time
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Restores a specific backup by name from a storage volume.
        (Corresponds to POST /backup/backup-restore/{volume-ip}/{export-path}/{backup-name} - OpId: restoreBackupByVolumeIpAndExportPathAndBackupName)

        Args:
            volume_ip (str): The IP address of the volume.
            export_path (str): The export path.
            backup_name (str): The name of the backup to restore.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
        Optional kwargs:
            cluster_uuid (str): (API name: cluster-uuid)

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        path = f"/backup/backup-restore/{volume_ip}/{export_path.lstrip('/')}/{backup_name}"
        query_params = {}
        if "cluster_uuid" in kwargs: query_params["cluster-uuid"] = kwargs["cluster_uuid"]

        logger.info(f"Restoring backup '{backup_name}' for volume_ip='{volume_ip}', export_path='{export_path}' with params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )