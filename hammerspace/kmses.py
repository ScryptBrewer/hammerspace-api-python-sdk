# hammerspace/kmses.py
import logging
from typing import Optional, List, Dict, Any, Union

logger = logging.getLogger(__name__)

class KmsesClient:
    def __init__(self, api_client: Any):
        """
        Initializes the KmsesClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all key management systems or a specific one by its identifier.

        If 'identifier' is provided, fetches a single KMS.
        (Corresponds to GET /kmses/{identifier} - OpId: getKmsByIdentifier)

        Otherwise, lists all KMSes, accepting pagination and filtering kwargs.
        (Corresponds to GET /kmses - OpId: listKmses)

        Args:
            identifier (Optional[str]): The ID or name of a specific KMS to retrieve.
            **kwargs: Optional keyword arguments.
                - For listing (identifier=None):
                    spec (str): Filter predicate.
                    page (int): Zero-based page number.
                    page_size (int): Elements per page. (API name: page.size)
                    page_sort (str): Field to sort on. (API name: page.sort)
                    page_sort_dir (str): Either 'asc' or 'desc'. (API name: page.sort.dir)
                - Note: The GET /kmses/{identifier} endpoint in the provided spec
                  does not list any query parameters, so kwargs are ignored if an
                  identifier is provided.

        Returns:
            - A list of KMS dictionaries if identifier is None and the call is successful.
            - A single KMS dictionary if identifier is provided and the call is successful.
            - None if the call fails or the KMS is not found.
        """
        if identifier:
            # Fetch a specific KMS by identifier
            path = f"/kmses/{identifier}"
            logger.info(f"Getting KMS by identifier: {identifier}")
            # According to the provided OpenAPI spec, GET /kmses/{identifier} has no query parameters.
            query_params = {} 
            response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
            return self.api_client.read_and_parse_json_body(response)
        else:
            # List all KMSes
            path = "/kmses"
            query_params = {}
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            
            logger.info(f"Listing all KMSes with effective query params: {query_params}")
            response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
            return self.api_client.read_and_parse_json_body(response)

    def create_kms(
        self, kms_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Add a key management system. (POST /kmses) - OpId: createKms
        The requestBody is BaseEntityView, but the response is KmsView.
        """
        path = "/kmses"
        logger.info(f"Creating KMS with data: {kms_data}")
        # No query parameters listed for this POST in the spec.
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=kms_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self, identifier: str, kms_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Update a key management system. (PUT /kmses/{identifier}) - OpId: updateKmsByIdentifier
        The requestBody is KmsView.
        """
        path = f"/kmses/{identifier}"
        logger.info(f"Updating KMS '{identifier}' with data: {kms_data}")
        # No query parameters listed for this PUT in the spec.
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=kms_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300, **kwargs
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Remove a key management system. (DELETE /kmses/{identifier}) - OpId: deleteKmsByIdentifier
        
        Optional kwargs:
            force (bool): If true, forces deletion. (API query param: force)
        """
        path = f"/kmses/{identifier}"
        query_params = {}
        if "force" in kwargs:
            query_params["force"] = str(kwargs["force"]).lower()
            
        logger.info(f"Deleting KMS '{identifier}' with query params: {query_params}")
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE", initial_query_params=query_params,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
