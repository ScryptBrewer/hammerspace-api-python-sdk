# hammerspace/files.py
import logging
from typing import Optional, List, Dict, Any, Union, IO
import requests # For accessing response.content directly for download

logger = logging.getLogger(__name__)

class FilesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the FilesClient for file and directory operations.
        """
        self.api_client = api_client
        logger.info("FilesClient initialized using provided OpenAPI spec.")

    def browse_files(
        self,
        share_name_or_uuid: str,
        path: str, # Path within the share
        **kwargs
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Browses files and directories at a given path within a share.
        (Corresponds to GET /files/browse/{share-name-or-uuid}/{path} - OpId: browseFiles)

        Args:
            share_name_or_uuid (str): The name or UUID of the share.
            path (str): The path within the share to browse. Use "." for the share root.
        Optional kwargs for listing:
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        
        Returns:
            A list of file/directory information dictionaries (FileView schema) or None on failure.
        """
        # Ensure path is URL-encoded properly, requests usually handles this for path segments
        # If path is empty or ".", it might represent the root of the share.
        # The API spec implies {path} can be multi-segment.
        effective_path = path.lstrip('/') if path else '.' # API might expect '.' for root
        api_path = f"/files/browse/{share_name_or_uuid}/{effective_path}"
        
        query_params = {}
        if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
        if "page" in kwargs: query_params["page"] = kwargs["page"]
        if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
        if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
        if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
        
        logger.info(f"Browsing files in share '{share_name_or_uuid}' at path '{effective_path}' with params: {query_params}")
        response = self.api_client.make_rest_call(path=api_path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response) # Expected: List[FileView]

    def download_file(
        self,
        share_name_or_uuid: str,
        path: str # Path within the share to the file
    ) -> Optional[bytes]:
        """
        Downloads a file from a given path within a share.
        (Corresponds to GET /files/download/{share-name-or-uuid}/{path} - OpId: downloadFile)

        Args:
            share_name_or_uuid (str): The name or UUID of the share.
            path (str): The path within the share to the file to download.

        Returns:
            The file content as bytes, or None on failure.
        """
        effective_path = path.lstrip('/')
        if not effective_path:
            logger.error("File path cannot be empty for download.")
            return None
        api_path = f"/files/download/{share_name_or_uuid}/{effective_path}"
        
        logger.info(f"Downloading file from share '{share_name_or_uuid}' at path '{effective_path}'")
        try:
            # Use stream=True if you want to handle large files efficiently,
            # but for simplicity here, we'll download directly.
            # For streaming, you'd return the response object and let the caller iterate.
            response = self.api_client.make_rest_call(path=api_path, method="GET", stream=False)
            # The spec indicates 'format: binary, type: string' which means raw bytes
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download file: {e}")
            return None

    def upload_file(
        self,
        share_name_or_uuid: str,
        path: str, # Destination path within the share, including filename
        file_object: IO, # An open file-like object (e.g., open('file.txt', 'rb'))
        overwrite: bool = False,
        monitor_task: bool = False, # Spec says 200 OK with FileView
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Uploads a file to a given path within a share.
        (Corresponds to POST /files/upload/{share-name-or-uuid}/{path} - OpId: uploadFile)
        The API spec indicates a 200 OK response with the FileView object.

        Args:
            share_name_or_uuid (str): The name or UUID of the share.
            path (str): The destination path within the share, including the desired filename.
            file_object (IO): The file-like object to upload (e.g., opened in 'rb' mode).
            overwrite (bool): Whether to overwrite the file if it already exists.
            monitor_task (bool): Whether to treat as an asynchronous task (unlikely for direct upload).
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.

        Returns:
            The FileView dictionary of the uploaded file if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        effective_path = path.lstrip('/')
        if not effective_path:
            logger.error("Destination path cannot be empty for upload.")
            return None
        api_path = f"/files/upload/{share_name_or_uuid}/{effective_path}"
        
        query_params = {"overwrite": str(overwrite).lower()}
        files_payload = {'file': file_object} # Key 'file' as per multipart/form-data spec

        logger.info(f"Uploading file to share '{share_name_or_uuid}' at path '{effective_path}', overwrite: {overwrite}")
        
        if monitor_task: # Unlikely to be a task, but support the pattern
            return self.api_client.execute_and_monitor_task(
                path=api_path, method="POST", initial_query_params=query_params,
                # execute_and_monitor_task needs to support 'files' if we go this route
                # For now, assuming direct call for upload
                monitor_task=False # Forcing direct call as execute_and_monitor_task doesn't handle 'files' yet
            )
        
        try:
            # Direct call for file upload
            response = self.api_client.make_rest_call(
                path=api_path, method="POST", query_params=query_params, files=files_payload
            )
            return self.api_client.read_and_parse_json_body(response) # Expected: FileView
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to upload file: {e}")
            return None

    def create_directory(
        self,
        share_name_or_uuid: str,
        path: str, # Path of the directory to create within the share
        monitor_task: bool = False, # Spec says 200 OK with FileView
        task_timeout_seconds: int = 60
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new directory at a given path within a share.
        (Corresponds to POST /files/create-directory/{share-name-or-uuid}/{path} - OpId: createDirectory)
        The API spec indicates a 200 OK response with the FileView object of the created directory.

        Args:
            share_name_or_uuid (str): The name or UUID of the share.
            path (str): The path within the share where the directory should be created.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.

        Returns:
            The FileView dictionary of the created directory if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        effective_path = path.lstrip('/')
        if not effective_path:
            logger.error("Directory path cannot be empty for creation.")
            return None
        api_path = f"/files/create-directory/{share_name_or_uuid}/{effective_path}"
        
        logger.info(f"Creating directory in share '{share_name_or_uuid}' at path '{effective_path}'")
        # This POST operation does not have a request body or query parameters according to the spec.
        if monitor_task:
             return self.api_client.execute_and_monitor_task(
                path=api_path, method="POST",
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(path=api_path, method="POST")
            return self.api_client.read_and_parse_json_body(response) # Expected: FileView

    def delete_file_or_directory(
        self,
        share_name_or_uuid: str,
        path: str, # Path of the file or directory to delete
        recursive: bool = False,
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes a file or directory at a given path within a share.
        (Corresponds to DELETE /files/delete/{share-name-or-uuid}/{path} - OpId: deleteFileOrDirectory)
        The API spec indicates a 202 Accepted response.

        Args:
            share_name_or_uuid (str): The name or UUID of the share.
            path (str): The path within the share to the file or directory to delete.
            recursive (bool): Whether to delete recursively (for directories).
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        effective_path = path.lstrip('/')
        if not effective_path:
            logger.error("Path cannot be empty for deletion.")
            return None
        api_path = f"/files/delete/{share_name_or_uuid}/{effective_path}"
        
        query_params = {"recursive": str(recursive).lower()}
        
        logger.info(f"Deleting file/directory in share '{share_name_or_uuid}' at path '{effective_path}', recursive: {recursive}")
        return self.api_client.execute_and_monitor_task(
            path=api_path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)

    def move_file_or_directory(
        self,
        source_share_name_or_uuid: str,
        source_path: str,
        dest_share_name_or_uuid: str, # API name: destShare (query param)
        dest_path: str,             # API name: destPath (query param)
        overwrite: bool = False,
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 600 # Moves can take time
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Moves a file or directory from a source path to a destination path.
        (Corresponds to POST /files/move/{source-share-name-or-uuid}/{source-path} - OpId: moveFileOrDirectory)
        The API spec indicates a 202 Accepted response.

        Args:
            source_share_name_or_uuid (str): The name or UUID of the source share.
            source_path (str): The source path within the source share.
            dest_share_name_or_uuid (str): The name or UUID of the destination share.
            dest_path (str): The destination path within the destination share.
            overwrite (bool): Whether to overwrite if the destination exists.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        effective_source_path = source_path.lstrip('/')
        if not effective_source_path:
            logger.error("Source path cannot be empty for move operation.")
            return None
        api_path = f"/files/move/{source_share_name_or_uuid}/{effective_source_path}"
        
        query_params = {
            "destShare": dest_share_name_or_uuid,
            "destPath": dest_path,
            "overwrite": str(overwrite).lower()
        }
        
        logger.info(f"Moving from share '{source_share_name_or_uuid}' path '{effective_source_path}' to "
                    f"share '{dest_share_name_or_uuid}' path '{dest_path}', overwrite: {overwrite}")
        return self.api_client.execute_and_monitor_task(
            path=api_path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)

    def copy_file_or_directory(
        self,
        source_share_name_or_uuid: str,
        source_path: str,
        dest_share_name_or_uuid: str, # API name: destShare (query param)
        dest_path: str,             # API name: destPath (query param)
        overwrite: bool = False,
        monitor_task: bool = True, # Spec says 202 Accepted
        task_timeout_seconds: int = 1800 # Copies can take significant time
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Copies a file or directory from a source path to a destination path.
        (Corresponds to POST /files/copy/{source-share-name-or-uuid}/{source-path} - OpId: copyFileOrDirectory)
        The API spec indicates a 202 Accepted response.

        Args:
            source_share_name_or_uuid (str): The name or UUID of the source share.
            source_path (str): The source path within the source share.
            dest_share_name_or_uuid (str): The name or UUID of the destination share.
            dest_path (str): The destination path within the destination share.
            overwrite (bool): Whether to overwrite if the destination exists.
            monitor_task (bool): Whether to monitor the asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.

        Returns:
            Task ID or result if monitoring, or initial response (empty dict). None on failure.
        """
        effective_source_path = source_path.lstrip('/')
        if not effective_source_path:
            logger.error("Source path cannot be empty for copy operation.")
            return None
        api_path = f"/files/copy/{source_share_name_or_uuid}/{effective_source_path}"
        
        query_params = {
            "destShare": dest_share_name_or_uuid,
            "destPath": dest_path,
            "overwrite": str(overwrite).lower()
        }
        
        logger.info(f"Copying from share '{source_share_name_or_uuid}' path '{effective_source_path}' to "
                    f"share '{dest_share_name_or_uuid}' path '{dest_path}', overwrite: {overwrite}")
        return self.api_client.execute_and_monitor_task(
            path=api_path, method="POST", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        ) # Expected: {} (from 202 response)
