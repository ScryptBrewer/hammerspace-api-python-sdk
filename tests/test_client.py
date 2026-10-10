# tests/test_client.py
import pytest
import requests
from unittest.mock import MagicMock

import hammerspace.client as client_module
from hammerspace import HammerspaceApiClient
from hammerspace.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConnectionError as HSConnectionError,
    HammerspaceApiError,
    RateLimitError,
    ResourceNotFoundError,
    RetryExhaustedError,
    ServerError,
    TaskFailedError,
    ValidationError,
)


class TestClientConfiguration:
    def test_base_url_gets_trailing_slash(self, client):
        assert client.base_url == "https://api.example.test/"

    def test_missing_base_url_raises_configuration_error(self):
        with pytest.raises(Exception, match="base_url is required"):
            HammerspaceApiClient()

    def test_base_url_falls_back_to_environment(self, monkeypatch):
        monkeypatch.setenv("HS_BASE_URL", "https://env.example.test")
        client = HammerspaceApiClient()
        assert client.base_url == "https://env.example.test/"

    def test_no_login_attempt_without_credentials(self, client):
        assert client.is_logged_in_via_cookie is False
        assert client.session.request.call_count == 0


class TestMakeRestCall:
    def test_builds_url_and_returns_response(self, client, make_response):
        client.session.request.return_value = make_response(json_data={"ok": True})
        response = client.make_rest_call("/shares", method="GET")
        assert response.json() == {"ok": True}
        args, kwargs = client.session.request.call_args
        assert args[0] == "GET"
        assert args[1] == "https://api.example.test/shares"

    def test_get_response_is_cached(self, client, make_response):
        client.session.request.return_value = make_response(json_data=[{"uuid": "1"}])
        first = client.make_rest_call("/shares", method="GET")
        second = client.make_rest_call("/shares", method="GET")
        assert client.session.request.call_count == 1
        assert second == [{"uuid": "1"}]
        assert first.json() == [{"uuid": "1"}]

    def test_clear_cache_forces_new_request(self, client, make_response):
        client.session.request.return_value = make_response(json_data={"a": 1})
        client.make_rest_call("/nodes", method="GET")
        client.clear_cache()
        client.make_rest_call("/nodes", method="GET")
        assert client.session.request.call_count == 2

    def test_lazy_login_when_credentials_present(self, client, make_response):
        client.username = "user"
        client.password = "secret"
        client.session.request.return_value = make_response(json_data={})
        calls = []
        client._perform_login_action = lambda: calls.append(1)
        client.make_rest_call("/shares", method="GET")
        assert calls, "lazy login should be attempted before the first call"
        assert client.session.request.call_count == 1

    def test_lazy_login_failure_propagates(self, client, make_response):
        client.username = "user"
        client.password = "secret"

        def boom():
            raise AuthenticationError()

        client._perform_login_action = boom
        with pytest.raises(AuthenticationError):
            client.make_rest_call("/shares", method="GET")
        assert client.session.request.call_count == 0


class TestErrorMapping:
    def _request_that_fails(self, client, make_response, status, headers=None):
        response = make_response(status_code=status, headers=headers, text="error body")
        client.session.request.return_value = response
        return response

    def test_401_maps_to_authentication_error(self, client, make_response):
        self._request_that_fails(client, make_response, 401)
        with pytest.raises(AuthenticationError):
            client.make_rest_call("/login", method="POST", is_login=True)

    def test_403_maps_to_authorization_error(self, client, make_response):
        self._request_that_fails(client, make_response, 403)
        with pytest.raises(AuthorizationError):
            client.make_rest_call("/shares", method="GET")

    def test_404_maps_to_resource_not_found(self, client, make_response):
        self._request_that_fails(client, make_response, 404)
        with pytest.raises(ResourceNotFoundError):
            client.make_rest_call("/shares/nope", method="GET")

    def test_400_maps_to_validation_error(self, client, make_response):
        self._request_that_fails(client, make_response, 400)
        with pytest.raises(ValidationError):
            client.make_rest_call("/shares", method="POST", json_data={"bad": 1})

    def test_429_maps_to_rate_limit_error(self, client, make_response):
        self._request_that_fails(
            client, make_response, 429, headers={"Content-Type": "text/plain", "Retry-After": "30"}
        )
        with pytest.raises(RateLimitError) as excinfo:
            client.make_rest_call("/shares", method="GET")
        assert excinfo.value.retry_after == 30

    def test_500_maps_to_server_error(self, client, make_response):
        self._request_that_fails(client, make_response, 500)
        with pytest.raises(ServerError):
            client.make_rest_call("/shares", method="GET")

    def test_connection_error_maps_to_hs_connection_error(self, client):
        client.session.request.side_effect = requests.exceptions.ConnectionError("boom")
        with pytest.raises(HSConnectionError):
            client.make_rest_call("/shares", method="GET")


class TestRetry:
    def test_retry_exhaustion_raises_retry_exhausted(self, monkeypatch):
        monkeypatch.setattr(client_module.time, "sleep", lambda seconds: None)
        client = HammerspaceApiClient(
            base_url="https://api.example.test", max_retries=2
        )
        client.session = MagicMock()
        client.session.request.side_effect = requests.exceptions.ConnectionError("down")
        with pytest.raises(RetryExhaustedError) as excinfo:
            client.make_rest_call_with_retry("/shares", method="GET")
        assert excinfo.value.total_attempts == 2
        assert client.session.request.call_count == 2


class TestReadAndParseJsonBody:
    def test_passthrough_for_already_parsed_body(self, client):
        assert client.read_and_parse_json_body({"a": 1}) == {"a": 1}
        assert client.read_and_parse_json_body([1, 2]) == [1, 2]

    def test_204_returns_none(self, client, make_response):
        response = make_response(status_code=204)
        response.content = b""
        assert client.read_and_parse_json_body(response) is None

    def test_invalid_json_returns_none(self, client, make_response):
        response = make_response(text="not json")
        assert client.read_and_parse_json_body(response) is None


class TestExecuteAndMonitorTask:
    @pytest.fixture(autouse=True)
    def _legacy_raw_behavior(self, mock_api):
        """These tests pin the legacy raw-dict contract; the mock bypasses the
        real model plumbing, so stub it with the legacy passthrough."""
        mock_api.return_raw = True
        mock_api._maybe_model_result = lambda data, result_model, raw: data
        return mock_api

    def test_sync_200_returns_data(self, mock_api, make_response):
        mock_api.make_rest_call_with_retry.return_value = make_response(
            status_code=200, json_data={"uuid": "sync-1"}
        )
        mock_api.read_and_parse_json_body.return_value = {"uuid": "sync-1"}
        result = client_module.HammerspaceApiClient.execute_and_monitor_task(
            mock_api, "/shares", method="POST", initial_json_data={"name": "s"}
        )
        assert result == {"uuid": "sync-1"}

    def test_monitor_disabled_returns_initial_data(self, mock_api, make_response):
        mock_api.make_rest_call_with_retry.return_value = make_response(
            status_code=202, json_data={"accepted": True},
            headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/1"},
        )
        mock_api.read_and_parse_json_body.return_value = {"accepted": True}
        result = client_module.HammerspaceApiClient.execute_and_monitor_task(
            mock_api, "/shares", method="POST", monitor_task=False
        )
        assert result == {"accepted": True}
        mock_api.make_rest_call.assert_not_called()

    def test_202_with_completed_task_returns_result(self, mock_api, make_response):
        mock_api.make_rest_call_with_retry.return_value = make_response(
            status_code=202, json_data={"accepted": True},
            headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/1"},
        )
        mock_api.read_and_parse_json_body.side_effect = [
            {"accepted": True},
            {"state": "COMPLETED", "result": {"uuid": "done-1"}},
        ]
        mock_api.make_rest_call.return_value = make_response(
            status_code=200, json_data={"state": "COMPLETED", "result": {"uuid": "done-1"}}
        )
        result = client_module.HammerspaceApiClient.execute_and_monitor_task(
            mock_api, "/shares", method="POST", poll_interval_seconds=0
        )
        assert result == {"uuid": "done-1"}
        poll_args = mock_api.make_rest_call.call_args
        assert poll_args.kwargs.get("is_absolute_url") is True

    def test_202_with_failed_task_raises(self, mock_api, make_response):
        mock_api.make_rest_call_with_retry.return_value = make_response(
            status_code=202, json_data={"accepted": True},
            headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/2"},
        )
        mock_api.read_and_parse_json_body.side_effect = [
            {"accepted": True},
            {"state": "FAILED", "errorMessage": "boom"},
        ]
        mock_api.make_rest_call.return_value = make_response(
            status_code=200, json_data={"state": "FAILED", "errorMessage": "boom"}
        )
        with pytest.raises(TaskFailedError) as excinfo:
            client_module.HammerspaceApiClient.execute_and_monitor_task(
                mock_api, "/shares", method="POST", poll_interval_seconds=0
            )
        assert excinfo.value.task_details["state"] == "FAILED"

    def test_initial_failure_wraps_in_api_error(self, mock_api):
        mock_api.make_rest_call_with_retry.side_effect = HammerspaceApiError(
            "down", status_code=500
        )
        with pytest.raises(HammerspaceApiError, match="Task initialization failed"):
            client_module.HammerspaceApiClient.execute_and_monitor_task(
                mock_api, "/shares", method="POST"
            )
