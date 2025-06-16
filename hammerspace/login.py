 # hammerspace/login.py
import logging
from typing import Optional, Dict, Any
import requests # For requests.exceptions

logger = logging.getLogger(__name__)

class LoginClient:
    """
    Client for handling user login to the Hammerspace API.
    """
    def __init__(self, api_client: Any):
        """
        Initializes the LoginClient.

        Args:
            api_client: An instance of HammerspaceApiClient.
        """
        self.api_client = api_client

    def login_user(self, username: str, password: str, accept_eula: bool = True, **kwargs) -> None:
        """
        Logs in the user to the Hammerspace API. (POST /login)
        Uses application/x-www-form-urlencoded.
        Raises an exception on login failure.

        Args:
            username (str): The username for login.
            password (str): The password for login.
            **kwargs: Optional keyword arguments.
                accept_eula (bool): Whether the EULA is accepted.
                                    (API form field: acceptEula)
        
        Raises:
            requests.exceptions.HTTPError: If the login API call returns
                                           a non-successful status code.
            requests.exceptions.RequestException: For other network or
                                                  request-related errors.
        """
        path = "/login" # The API endpoint for login
        form_data: Dict[str, Any] = {
            "username": username,
            "password": password
        }

        if "accept_eula" in kwargs:
            # API spec might show boolean, requests 'data' param handles
            # bools by converting to 'true'/'false' strings for forms.
            # Ensure it's a string 'true' or 'false' if API is strict.
            form_data["acceptEula"] = str(kwargs["accept_eula"]).lower()

        # The Content-Type header is crucial for form data
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        full_url = f"{self.api_client.base_url}{path.lstrip('/')}"

        logger.info(f"Attempting login for user '{username}' to {full_url}.")
        
        try:
            # CRITICAL: Use the api_client's session object to make the request.
            # This ensures that any cookies set by the server upon successful
            # login are stored in the shared session and will be automatically
            # sent with subsequent requests made by HammerspaceApiClient.
            response = self.api_client.session.post(
                full_url,
                data=form_data,
                headers=headers,
                timeout=self.api_client.timeout,
                verify=self.api_client.verify_ssl
            )

            log_msg_prefix = (
                f"Login response for user '{username}': "
                f"Status {response.status_code}"
            )

            # Check if the login was successful.
            # Typically, a 2xx status code (e.g., 200 OK, 204 No Content)
            # indicates success for a login operation that sets a cookie.
            if 200 <= response.status_code < 300:
                logger.info(f"{log_msg_prefix} - Login successful.")
                # No need to return True, success is implied by no exception.
                # The cookie is now in self.api_client.session.
                # HammerspaceApiClient will set self.is_logged_in_via_cookie = True
                return
            else:
                # If login failed, raise an HTTPError.
                # This will be caught by _perform_login_action in HammerspaceApiClient.
                logger.warning(
                    f"{log_msg_prefix} - Login failed. "
                    f"Body: {response.text[:500]}"
                )
                response.raise_for_status() # This will raise HTTPError

        except requests.exceptions.HTTPError as http_err:
            # Logged by raise_for_status or if we re-raise.
            # Error will be propagated to HammerspaceApiClient.
            logger.error(
                f"Login HTTP error for user '{username}': {http_err}",
                exc_info=False # HTTPError str includes details
            )
            raise # Re-raise the HTTPError
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f"Login request failed for user '{username}': {req_err}",
                exc_info=True
            )
            raise # Re-raise the RequestException
        except Exception as e:
            # Catch any other unexpected errors during the login process
            logger.error(
                f"Unexpected error during login for user '{username}': {e}",
                exc_info=True
            )
            raise # Re-raise the unexpected error           