# hammerspace/s3server.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class S3ServerClient:
    def __init__(self, api_client: Any):
        """
        Initializes the S3ServerClient for managing S3 server configurations.
        """
        self.api_client = api_client
        logger.info("S3ServerClient initialized using provided OpenAPI spec.")

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all S3 server configurations or a specific S3 server by its identifier.

        If 'identifier' is provided, fetches a single S3 server configuration.
        (Corresponds to GET /s3server/{identifier} - OpId: get)
        Optional kwargs for get by identifier:
            withUnclearedEventSeverity (List[str]): Augment response with uncleared events.

        Otherwise, lists all S3 server configurations.
        (Corresponds to GET /s3server - OpId: list)
        Optional kwargs for listing:
            referenceView (bool): Whether to return a reference view.
            spec (str): Filter predicate.
            page (int): Zero-based page number.
            page_size (int): Elements per page. (API name: page.size)
            page_sort (str): Field to sort on. (API name: page.sort)
            page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
        """
        query_params = {}
        if identifier:
            path = f"/s3server/{identifier}"
            if "withUnclearedEventSeverity" in kwargs:
                query_params["withUnclearedEventSeverity"] = kwargs["withUnclearedEventSeverity"]
            logger.info(f"Getting S3 server by identifier: {identifier} with params: {query_params}")
        else:
            path = "/s3server"
            if "referenceView" in kwargs: query_params["referenceView"] = kwargs["referenceView"]
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing all S3 servers with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        # Expected: S3ServerConfigView or List[S3ServerConfigView]
        return self.api_client.read_and_parse_json_body(response)

    def create_s3_server(
        self,
        server_data: Dict[str, Any], # requestBody is S3ServerConfigView
        validate_only: Optional[bool] = None,
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Creates a new S3 server configuration.
        (Corresponds to POST /s3server - OpId: post)
        The API spec indicates a 200 OK response with the created S3ServerConfigView object.

        Args:
            server_data (Dict[str, Any]): Data for the new S3 server (S3ServerConfigView schema).
            validate_only (Optional[bool]): If true, only validates the request without creating.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The created S3ServerConfigView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = "/s3server"
        query_params = {}
        if validate_only is not None:
            query_params["validate-only"] = validate_only
        
        logger.info(f"Creating S3 server with data: {server_data}, query_params: {query_params}")
        if monitor_task: # Unlikely for 200 OK, but supported
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=server_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=server_data, query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)

    def update_s3_server(
        self,
        identifier: str,
        server_data: Dict[str, Any], # requestBody is S3ServerConfigView
        validate_only: Optional[bool] = None,
        delete_bucket_content: Optional[bool] = None,
        delete_content_preserve_dir: Optional[bool] = None,
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Updates an existing S3 server configuration.
        (Corresponds to PUT /s3server/{identifier} - OpId: put)
        The API spec indicates a 200 OK response with the updated S3ServerConfigView object.

        Args:
            identifier (str): The identifier of the S3 server to update.
            server_data (Dict[str, Any]): New data for the S3 server (S3ServerConfigView schema).
            validate_only (Optional[bool]): If true, only validates the request.
            delete_bucket_content (Optional[bool]): Query param for update.
            delete_content_preserve_dir (Optional[bool]): Query param for update.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The updated S3ServerConfigView dictionary if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/s3server/{identifier}"
        query_params = {}
        if validate_only is not None: query_params["validate-only"] = validate_only
        if delete_bucket_content is not None: query_params["deleteBucketContent"] = delete_bucket_content
        if delete_content_preserve_dir is not None: query_params["deleteContentPreserveDir"] = delete_content_preserve_dir
        
        logger.info(f"Updating S3 server '{identifier}' with data: {server_data}, query_params: {query_params}")
        if monitor_task: # Unlikely for 200 OK, but supported
            return self.api_client.execute_and_monitor_task(
                path=path, method="PUT", initial_json_data=server_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="PUT", json_data=server_data, query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)

    def delete_s3_server(
        self,
        identifier: str,
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Deletes an S3 server configuration.
        (Corresponds to DELETE /s3server/{identifier} - OpId: delete)
        The API spec indicates a 200 OK response with the S3ServerConfigView object (unusual for DELETE).

        Args:
            identifier (str): The identifier of the S3 server to delete.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring if monitor_task is True.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The S3ServerConfigView of the deleted server if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/s3server/{identifier}"
        query_params = {} # No query params defined for DELETE by identifier in spec
        
        logger.info(f"Deleting S3 server '{identifier}'")
        if monitor_task: # Unlikely for 200 OK, but supported
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)

    def add_bucket_to_s3_server(
        self,
        s3_server_identifier: str,
        bucket_data: Dict[str, Any], # requestBody is S3BucketDescriptorBaseView
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Adds a bucket or bucket container to an existing S3 server.
        (Corresponds to POST /s3server/{identifier}/bucket - OpId: post, distinct from create_s3_server's OpId)
        The API spec indicates a 200 OK response with the updated S3ServerConfigView object.

        Args:
            s3_server_identifier (str): Identifier of the S3 server.
            bucket_data (Dict[str, Any]): Data for the new bucket (S3BucketDescriptorBaseView schema).
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The updated S3ServerConfigView if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/s3server/{s3_server_identifier}/bucket"
        query_params = {} # No query params defined for this POST in spec
        
        logger.info(f"Adding bucket to S3 server '{s3_server_identifier}' with data: {bucket_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=bucket_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=bucket_data, query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)

    def remove_bucket_from_s3_server(
        self,
        s3_server_identifier: str,
        bucket_name: str,
        delete_bucket_content: Optional[bool] = None,
        delete_content_preserve_dir: Optional[bool] = None,
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Removes an S3 bucket from an S3 server.
        (Corresponds to DELETE /s3server/{identifier}/bucket - OpId: deleteBucket)
        The API spec indicates a 200 OK response with the updated S3ServerConfigView object.

        Args:
            s3_server_identifier (str): Identifier of the S3 server.
            bucket_name (str): Name of the bucket to remove.
            delete_bucket_content (Optional[bool]): Query param.
            delete_content_preserve_dir (Optional[bool]): Query param.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The updated S3ServerConfigView if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/s3server/{s3_server_identifier}/bucket"
        query_params = {"bucketName": bucket_name}
        if delete_bucket_content is not None: query_params["deleteBucketContent"] = delete_bucket_content
        if delete_content_preserve_dir is not None: query_params["deleteContentPreserveDir"] = delete_content_preserve_dir
        
        logger.info(f"Removing bucket '{bucket_name}' from S3 server '{s3_server_identifier}', query_params: {query_params}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)

    def list_buckets_for_s3_server(
        self,
        s3_server_identifier: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]: # S3ServerConfigView contains buckets
        """
        Lists buckets for a specific S3 server.
        (Corresponds to GET /s3server/{identifier}/listBuckets - OpId: listBuckets)
        The response is the S3ServerConfigView which should contain the bucket list.

        Args:
            s3_server_identifier (str): Identifier of the S3 server.
            **kwargs: Additional optional keyword arguments for query parameters (none defined in spec).

        Returns:
            The S3ServerConfigView dictionary containing bucket information, or None on failure.
        """
        path = f"/s3server/{s3_server_identifier}/listBuckets"
        query_params = {} # No query params defined for this GET in spec
        
        logger.info(f"Listing buckets for S3 server '{s3_server_identifier}'")
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        # Expected: S3ServerConfigView
        return self.api_client.read_and_parse_json_body(response)

    def add_user_to_s3_server(
        self,
        s3_server_identifier: str,
        user_data: Dict[str, Any], # requestBody is S3UserView
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Adds an S3 user to an existing S3 server.
        (Corresponds to POST /s3server/{identifier}/user - OpId: postUserAdd)
        The API spec indicates a 200 OK response with the updated S3ServerConfigView object.

        Args:
            s3_server_identifier (str): Identifier of the S3 server.
            user_data (Dict[str, Any]): Data for the new S3 user (S3UserView schema).
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The updated S3ServerConfigView if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/s3server/{s3_server_identifier}/user"
        query_params = {} # No query params defined for this POST in spec
        
        logger.info(f"Adding user to S3 server '{s3_server_identifier}' with data: {user_data}")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="POST", initial_json_data=user_data, initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="POST", json_data=user_data, query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)

    def remove_user_from_s3_server(
        self,
        s3_server_identifier: str,
        user_name: str,
        monitor_task: bool = False, # Spec says 200 OK with S3ServerConfigView
        task_timeout_seconds: int = 300,
        **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Removes an S3 user from an S3 server.
        (Corresponds to DELETE /s3server/{identifier}/user - OpId: deleteS3User)
        The API spec indicates a 200 OK response with the updated S3ServerConfigView object.

        Args:
            s3_server_identifier (str): Identifier of the S3 server.
            user_name (str): Name of the S3 user to remove.
            monitor_task (bool): Whether to treat as an asynchronous task.
            task_timeout_seconds (int): Timeout for task monitoring.
            **kwargs: Additional optional keyword arguments.

        Returns:
            The updated S3ServerConfigView if successful and not monitoring,
            or task ID/result if monitoring. None on failure.
        """
        path = f"/s3server/{s3_server_identifier}/user"
        query_params = {"userName": user_name}
        
        logger.info(f"Removing user '{user_name}' from S3 server '{s3_server_identifier}'")
        if monitor_task:
            return self.api_client.execute_and_monitor_task(
                path=path, method="DELETE", initial_query_params=query_params,
                monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
            )
        else:
            response = self.api_client.make_rest_call(
                path=path, method="DELETE", query_params=query_params
            )
            # Expected: S3ServerConfigView
            return self.api_client.read_and_parse_json_body(response)
