# tests/test_client_models.py
from typing import List, Optional
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from hammerspace import HammerspaceApiClient
from hammerspace.client import redact_params, scrub_exception_message
from hammerspace.models import HammerspaceBaseModel
from hammerspace.exceptions import TaskFailedError
from hammerspace.exceptions import ValidationError as HSValidationError


class ShareView(BaseModel):
    uuid: Optional[str] = None
    name: str


class ShareCreate(HammerspaceBaseModel):
    name: str
    export_options: Optional[List[str]] = None


@pytest.fixture
def raw_client(clean_env):
    client = HammerspaceApiClient(base_url="https://api.example.test", return_raw=True)
    client.session = MagicMock()
    return client


class TestReadAndParseModels:
    def test_single_dict_body_parsed_into_model(self, client, make_response):
        response = make_response(json_data={"uuid": "u-1", "name": "docs"})
        parsed = client.read_and_parse_json_body(response, model=ShareView)
        assert isinstance(parsed, ShareView)
        assert parsed.name == "docs"

    def test_list_body_parsed_into_models(self, client, make_response):
        response = make_response(json_data=[{"name": "a"}, {"name": "b"}])
        parsed = client.read_and_parse_json_body(response, model=ShareView)
        assert isinstance(parsed, list) and len(parsed) == 2
        assert all(isinstance(s, ShareView) for s in parsed)
        assert parsed[1].name == "b"

    def test_many_true_wraps_single_object(self, client, make_response):
        response = make_response(json_data={"name": "only"})
        parsed = client.read_and_parse_json_body(response, model=ShareView, many=True)
        assert isinstance(parsed, list) and parsed[0].name == "only"

    def test_no_model_returns_raw(self, client, make_response):
        response = make_response(json_data={"name": "raw"})
        assert client.read_and_parse_json_body(response) == {"name": "raw"}

    def test_client_return_raw_toggle_wins(self, raw_client, make_response):
        response = make_response(json_data={"name": "raw"})
        parsed = raw_client.read_and_parse_json_body(response, model=ShareView)
        assert parsed == {"name": "raw"}

    def test_per_call_raw_flag_wins(self, client, make_response):
        response = make_response(json_data={"name": "raw"})
        parsed = client.read_and_parse_json_body(response, model=ShareView, raw=True)
        assert parsed == {"name": "raw"}

    def test_invalid_payload_raises_hs_validation_error(self, client, make_response):
        response = make_response(json_data={"uuid": "u-1"})  # missing required name
        with pytest.raises(HSValidationError) as excinfo:
            client.read_and_parse_json_body(response, model=ShareView)
        assert excinfo.value.validation_errors


class TestRequestBodySerialization:
    def test_model_serialized_with_camel_aliases(self, client, make_response):
        client.session.request.return_value = make_response(status_code=201, json_data={"uuid": "u"})
        payload = ShareCreate(name="docs", export_options=["*"])
        client.make_rest_call("/shares", method="POST", json_data=payload)
        kwargs = client.session.request.call_args.kwargs
        assert kwargs["json"] == {"name": "docs", "exportOptions": ["*"]}

    def test_list_of_models_serialized(self, client, make_response):
        client.session.request.return_value = make_response(status_code=201, json_data={"uuid": "u"})
        client.make_rest_call("/shares", method="POST", json_data=[ShareCreate(name="a")])
        kwargs = client.session.request.call_args.kwargs
        assert kwargs["json"] == [{"name": "a"}]


class TestExecuteAndMonitorModels:
    def test_sync_200_with_result_model(self, client, make_response):
        client.session.request.return_value = make_response(
            status_code=200, json_data={"uuid": "u-1", "name": "synced"}
        )
        result = client.execute_and_monitor_task(
            "/shares", method="POST", initial_json_data={"name": "synced"},
            result_model=ShareView,
        )
        assert isinstance(result, ShareView)
        assert result.uuid == "u-1"

    def test_completed_202_with_result_model(self, client, make_response):
        client.session.request.side_effect = [
            make_response(
                status_code=202, json_data={"accepted": True},
                headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/1"},
            ),
            make_response(
                status_code=200, json_data={"state": "COMPLETED", "result": {"uuid": "u-2", "name": "tasked"}}
            ),
        ]
        result = client.execute_and_monitor_task(
            "/shares", method="POST", poll_interval_seconds=0, result_model=ShareView,
        )
        assert isinstance(result, ShareView)
        assert result.uuid == "u-2"

    def test_completed_202_without_result_model_stays_raw(self, client, make_response):
        client.session.request.side_effect = [
            make_response(
                status_code=202, json_data={"accepted": True},
                headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/2"},
            ),
            make_response(
                status_code=200, json_data={"state": "COMPLETED", "result": {"uuid": "u-3"}}
            ),
        ]
        result = client.execute_and_monitor_task("/shares", method="POST", poll_interval_seconds=0)
        assert result == {"uuid": "u-3"}

    def test_completed_202_return_raw_toggle(self, raw_client, make_response):
        raw_client.session = MagicMock()
        raw_client.session.request.side_effect = [
            make_response(
                status_code=202, json_data={"accepted": True},
                headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/3"},
            ),
            make_response(
                status_code=200, json_data={"state": "COMPLETED", "result": {"uuid": "u-4"}}
            ),
        ]
        result = raw_client.execute_and_monitor_task(
            "/shares", method="POST", poll_interval_seconds=0, result_model=ShareView,
        )
        assert result == {"uuid": "u-4"}

    def test_failed_task_still_raises_with_details(self, client, make_response):
        client.session.request.side_effect = [
            make_response(
                status_code=202, json_data={"accepted": True},
                headers={"Content-Type": "application/json", "Location": "https://api.example.test/tasks/4"},
            ),
            make_response(
                status_code=200, json_data={"state": "FAILED", "errorMessage": "boom"}
            ),
        ]
        with pytest.raises(TaskFailedError) as excinfo:
            client.execute_and_monitor_task("/shares", method="POST", poll_interval_seconds=0)
        assert excinfo.value.task_details["state"] == "FAILED"


class TestCacheWithModels:
    def test_cache_hit_returns_model_copy(self, client, make_response):
        response = make_response(json_data={"uuid": "u-9", "name": "orig"})
        client.session.request.return_value = response
        first = client.make_rest_call("/shares/u-9", method="GET", model=ShareView)
        assert first is response

        second = client.make_rest_call("/shares/u-9", method="GET", model=ShareView)
        assert isinstance(second, ShareView)
        second.name = "mutated"

        third = client.make_rest_call("/shares/u-9", method="GET", model=ShareView)
        assert third.name == "orig"
        assert client.session.request.call_count == 1


class TestCredentialRedaction:
    def test_redact_params_masks_credential_keys(self):
        params = {
            "license-server-password": "s3cret",
            "license-server-username": "svc",
            "page.size": "10",
        }
        redacted = redact_params(params)
        assert redacted["license-server-password"] == "***"
        assert redacted["license-server-username"] == "svc"
        assert redacted["page.size"] == "10"
        assert params["license-server-password"] == "s3cret"  # original untouched

    def test_redact_params_passthrough_non_dict(self):
        assert redact_params(None) is None

    def test_scrub_exception_message_masks_query_echo(self):
        exc = ConnectionError(
            "HTTPSConnectionPool: Max retries exceeded with url: "
            "/licenses?license-server-password=s3cret&page=1"
        )
        scrubbed = scrub_exception_message(exc, {"license-server-password": "s3cret"})
        assert "s3cret" not in scrubbed
        assert "license-server-password=***" in scrubbed
