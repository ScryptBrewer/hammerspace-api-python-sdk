# hammerspace/exceptions.py (Optional)

class HammerspaceApiError(Exception):
    """Base exception for Hammerspace API errors."""
    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

class TaskTimeoutError(HammerspaceApiError):
    """Exception raised when a task monitoring times out."""
    pass

class TaskFailedError(HammerspaceApiError):
    """Exception raised when a monitored task reports a FAILED status."""
    def __init__(self, message, task_details=None, status_code=None, response_text=None):
        super().__init__(message, status_code, response_text)
        self.task_details = task_details

