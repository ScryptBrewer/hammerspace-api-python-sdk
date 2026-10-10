# tests/test_exceptions.py
import pytest

from hammerspace.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConfigurationError,
    ConnectionError,
    HammerspaceApiError,
    RateLimitError,
    ResourceNotFoundError,
    RetryExhaustedError,
    ServerError,
    TaskFailedError,
    TaskTimeoutError,
    ValidationError,
)


@pytest.mark.parametrize(
    "exc",
    [
        AuthenticationError,
        AuthorizationError,
        ResourceNotFoundError,
        ValidationError,
        RateLimitError,
        ServerError,
        TaskTimeoutError,
        TaskFailedError,
        ConnectionError,
        ConfigurationError,
        RetryExhaustedError,
    ],
)
def test_all_errors_inherit_base(exc):
    assert issubclass(exc, HammerspaceApiError)


class TestStrFormatting:
    def test_plain_message(self):
        assert str(HammerspaceApiError("boom")) == "boom"

    def test_includes_status_and_error_code(self):
        message = str(HammerspaceApiError("boom", status_code=500, error_code="X"))
        assert "boom" in message
        assert "Status Code: 500" in message
        assert "Error Code: X" in message

    def test_includes_truncated_response_text(self):
        error = HammerspaceApiError("boom", response_text="x" * 500)
        rendered = str(error)
        assert "Response: " in rendered
        assert "x" * 500 not in rendered


class TestSpecificErrors:
    def test_task_failed_extracts_task_id(self):
        error = TaskFailedError(task_details={"uuid": "t-1", "state": "FAILED"})
        assert error.task_id == "t-1"
        assert error.error_code == "TASK_FAILED"

    def test_task_timeout_carries_context(self):
        error = TaskTimeoutError(task_id="t-2", timeout_seconds=5)
        assert error.task_id == "t-2"
        assert error.timeout_seconds == 5

    def test_rate_limit_carries_retry_after(self):
        error = RateLimitError(retry_after=42)
        assert error.retry_after == 42

    def test_validation_error_defaults_to_empty_list(self):
        assert ValidationError().validation_errors == []

    def test_retry_exhausted_carries_attempts(self):
        error = RetryExhaustedError(total_attempts=3)
        assert error.total_attempts == 3
        assert error.error_code == "RETRY_EXHAUSTED"
