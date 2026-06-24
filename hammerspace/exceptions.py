# hammerspace/exceptions.py

class HammerspaceApiError(Exception):
    """Base exception for Hammerspace API errors."""
    def __init__(self, message: str, status_code: int = None, response_text: str = None, error_code: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text
        self.error_code = error_code
        
    def __str__(self):
        parts = [super().__str__()]
        if self.status_code:
            parts.append(f"Status Code: {self.status_code}")
        if self.error_code:
            parts.append(f"Error Code: {self.error_code}")
        if self.response_text:
            parts.append(f"Response: {self.response_text[:200]}...")
        return " | ".join(parts)

class AuthenticationError(HammerspaceApiError):
    """Exception raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed", status_code: int = 401, response_text: str = None, error_code: str = "AUTHENTICATION_ERROR"):
        super().__init__(message, status_code, response_text, error_code)

class AuthorizationError(HammerspaceApiError):
    """Exception raised when user is authorized but lacks permissions for the requested operation."""
    def __init__(self, message: str = "Authorization failed - insufficient permissions", status_code: int = 403, response_text: str = None, error_code: str = "AUTHORIZATION_ERROR"):
        super().__init__(message, status_code, response_text, error_code)

class ResourceNotFoundError(HammerspaceApiError):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found", status_code: int = 404, response_text: str = None, error_code: str = "RESOURCE_NOT_FOUND"):
        super().__init__(message, status_code, response_text, error_code)

class ValidationError(HammerspaceApiError):
    """Exception raised when request validation fails."""
    def __init__(self, message: str = "Request validation failed", status_code: int = 400, response_text: str = None, error_code: str = "VALIDATION_ERROR", validation_errors: list = None):
        super().__init__(message, status_code, response_text, error_code)
        self.validation_errors = validation_errors or []

class RateLimitError(HammerspaceApiError):
    """Exception raised when API rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded", status_code: int = 429, response_text: str = None, retry_after: int = None):
        super().__init__(message, status_code, response_text, "RATE_LIMIT_ERROR")
        self.retry_after = retry_after

class ServerError(HammerspaceApiError):
    """Exception raised when the server encounters an unexpected error."""
    def __init__(self, message: str = "Server error occurred", status_code: int = 500, response_text: str = None, error_code: str = "SERVER_ERROR"):
        super().__init__(message, status_code, response_text, error_code)

class TaskTimeoutError(HammerspaceApiError):
    """Exception raised when a task monitoring times out."""
    def __init__(self, message: str = "Task monitoring timed out", task_id: str = None, timeout_seconds: int = None):
        super().__init__(message, status_code=None, error_code="TASK_TIMEOUT")
        self.task_id = task_id
        self.timeout_seconds = timeout_seconds

class TaskFailedError(HammerspaceApiError):
    """Exception raised when a monitored task reports a FAILED status."""
    def __init__(self, message: str = "Task failed", task_details: dict = None, status_code: int = None, response_text: str = None):
        super().__init__(message, status_code, response_text, "TASK_FAILED")
        self.task_details = task_details or {}
        self.task_id = task_details.get("uuid") if task_details else None

class ConnectionError(HammerspaceApiError):
    """Exception raised when connection to the API server fails."""
    def __init__(self, message: str = "Connection to API server failed", original_error: Exception = None):
        super().__init__(message, status_code=None, error_code="CONNECTION_ERROR")
        self.original_error = original_error

class ConfigurationError(HammerspaceApiError):
    """Exception raised when client configuration is invalid."""
    def __init__(self, message: str = "Invalid client configuration"):
        super().__init__(message, status_code=None, error_code="CONFIGURATION_ERROR")

class RetryExhaustedError(HammerspaceApiError):
    """Exception raised when all retry attempts are exhausted."""
    def __init__(self, message: str = "All retry attempts exhausted", total_attempts: int = None, last_error: Exception = None):
        super().__init__(message, status_code=None, error_code="RETRY_EXHAUSTED")
        self.total_attempts = total_attempts
        self.last_error = last_error

