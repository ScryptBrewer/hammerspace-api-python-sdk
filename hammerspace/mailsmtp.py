# hammerspace/mailsmtp.py
import logging
from typing import Optional, List, Dict, Any, Union
logger = logging.getLogger(__name__)

class MailsmtpClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def get(
        self,
        identifier: Optional[str] = None,
        **kwargs
    ) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        """
        Gets all SMTP configurations or a specific one by its identifier.

        If 'identifier' is provided, fetches a single SMTP configuration.
        (Corresponds to GET /mail/smtp/{identifier} - OpId: getMailSmtpConfigurationByIdentifier)

        Otherwise, lists all SMTP configurations.
        (Corresponds to GET /mail/smtp - OpId: listMailSmtpConfiguration)
        Optional kwargs for listing: spec (str), page (int), page_size (int),
                                     page_sort (str), page_sort_dir (str)
        """
        query_params = {} # GET /mail/smtp/{id} has no query params in spec
        if identifier:
            path = f"/mail/smtp/{identifier}"
            logger.info(f"Getting SMTP configuration by identifier: {identifier}")
        else:
            path = "/mail/smtp"
            if "spec" in kwargs: query_params["spec"] = kwargs["spec"]
            if "page" in kwargs: query_params["page"] = kwargs["page"]
            if "page_size" in kwargs: query_params["page.size"] = kwargs["page_size"]
            if "page_sort" in kwargs: query_params["page.sort"] = kwargs["page_sort"]
            if "page_sort_dir" in kwargs: query_params["page.sort.dir"] = kwargs["page_sort_dir"]
            logger.info(f"Listing SMTP configurations with effective query params: {query_params}")
        
        response = self.api_client.make_rest_call(path=path, method="GET", query_params=query_params)
        return self.api_client.read_and_parse_json_body(response)

    def create_mail_smtp_configuration(
        self, smtp_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Configure SMTP. (POST /mail/smtp) - OpId: createMailSmtpConfiguration"""
        path = "/mail/smtp"
        logger.info(f"Creating SMTP configuration with data: {smtp_data}")
        # No query params defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=smtp_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def test_mail_smtp_notification_by_email(
        self, email: str, monitor_task: bool = True, task_timeout_seconds: int = 120
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Test notification. (POST /mail/smtp/test/{email}) - OpId: testMailSmtpNotificationByEmail"""
        path = f"/mail/smtp/test/{email}"
        logger.info(f"Testing SMTP notification to email: {email}")
        # No query params or body defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def update(
        self, identifier: str, smtp_data: Dict[str, Any], monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Update SMTP. (PUT /mail/smtp/{identifier}) - OpId: updateMailSmtpConfigurationByIdentifier"""
        path = f"/mail/smtp/{identifier}"
        logger.info(f"Updating SMTP configuration '{identifier}' with data: {smtp_data}")
        # No query params defined in spec for this PUT
        return self.api_client.execute_and_monitor_task(
            path=path, method="PUT", initial_json_data=smtp_data,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def delete(
        self, identifier: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """Delete SMTP. (DELETE /mail/smtp/{identifier}) - OpId: deleteMailSmtpConfigurationByIdentifier"""
        path = f"/mail/smtp/{identifier}"
        logger.info(f"Deleting SMTP configuration '{identifier}'.")
        # No query params defined in spec for this DELETE
        return self.api_client.execute_and_monitor_task(
            path=path, method="DELETE",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )
