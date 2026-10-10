# tests/test_models.py
from typing import Dict, Optional

from hammerspace.models import (
    ApiErrorDetail,
    HammerspaceBaseModel,
    TaskResult,
    TaskStatus,
)
from hammerspace.models.common import extract_entity_uuid


class Sample(HammerspaceBaseModel):
    site_uuid: Optional[str] = None
    display_name: Optional[str] = None


class TestHammerspaceBaseModel:
    def test_camel_case_serialization(self):
        sample = Sample(site_uuid="s1", display_name="name")
        assert sample.to_api() == {"siteUuid": "s1", "displayName": "name"}

    def test_camel_case_deserialization(self):
        sample = Sample.model_validate({"siteUuid": "s1", "displayName": "name"})
        assert sample.site_uuid == "s1"
        assert sample.display_name == "name"

    def test_populate_by_name_accepts_snake_case(self):
        assert Sample(site_uuid="s1").site_uuid == "s1"

    def test_to_api_excludes_unset_and_none(self):
        assert Sample().to_api() == {}
        assert Sample(site_uuid=None).to_api() == {}
        assert Sample(site_uuid="s1").to_api() == {"siteUuid": "s1"}

    def test_extra_fields_tolerated_and_preserved(self):
        sample = Sample.model_validate({"siteUuid": "s1", "brandNewField": 42})
        assert sample.site_uuid == "s1"
        assert sample.to_api()["brandNewField"] == 42

    def test_is_a_pydantic_base_model(self):
        assert issubclass(HammerspaceBaseModel, object)
        assert HammerspaceBaseModel.model_config.get("extra") == "allow"


class TestTaskStatus:
    def test_alias_round_trip(self):
        raw = {
            "uuid": "t-1",
            "state": "RUNNING",
            "progressPercent": 50,
            "statusMessage": "working",
        }
        status = TaskStatus.model_validate(raw)
        assert status.progress_percent == 50
        assert status.status_message == "working"
        assert status.to_api() == raw

    def test_effective_state_precedence(self):
        assert TaskStatus(state="running").effective_state == "RUNNING"
        assert TaskStatus(status="completed").effective_state == "COMPLETED"
        assert TaskStatus(status_message="all done").effective_state == "ALL DONE"
        assert TaskStatus().effective_state == ""
        assert TaskStatus(state="running", status="completed").effective_state == "RUNNING"

    def test_failed_states_normalizable(self):
        status = TaskStatus.model_validate({"state": "failed", "errorMessage": "boom"})
        assert status.effective_state == "FAILED"
        assert status.error_message == "boom"


class TestTaskResult:
    def test_entity_uuid_direct(self):
        assert TaskResult(uuid="u-1").entity_uuid == "u-1"

    def test_entity_uuid_from_ctx_map_dict(self):
        result = TaskResult.model_validate({"ctxMap": {"entity-uoid": {"uuid": "u-2"}}})
        assert result.entity_uuid == "u-2"

    def test_entity_uuid_from_ctx_map_string(self):
        result = TaskResult.model_validate(
            {"ctxMap": {"entity-uoid": "resource=[uuid=u-3,type=Share]"}}
        )
        assert result.entity_uuid == "u-3"

    def test_entity_uuid_missing(self):
        assert TaskResult().entity_uuid is None
        assert TaskResult.model_validate({"ctxMap": {"other": 1}}).entity_uuid is None
        assert TaskResult.model_validate(
            {"ctxMap": {"entity-uoid": {"uuid": ""}}}
        ).entity_uuid is None

    def test_entity_uuid_empty_value_string(self):
        result = TaskResult.model_validate({"ctxMap": {"entity-uoid": "uuid="}})
        assert result.entity_uuid is None

    def test_result_data_shape_from_client_contract(self):
        payload = {
            "uuid": "task-9",
            "state": "COMPLETED",
            "result": {"uuid": "share-77"},
        }
        parsed = TaskStatus.model_validate(payload)
        assert parsed.effective_state == "COMPLETED"
        inner = TaskResult.model_validate(payload.get("result", payload))
        assert inner.entity_uuid == "share-77"


class TestExtractEntityUuid:
    def test_none_and_empty(self):
        assert extract_entity_uuid(None) is None
        assert extract_entity_uuid({}) is None

    def test_dict_form(self):
        ctx: Dict[str, object] = {"entity-uoid": {"uuid": "u-5"}}
        assert extract_entity_uuid(ctx) == "u-5"

    def test_string_form_with_surroundings(self):
        ctx = {"entity-uoid": "ScopeEntityUoid=[uuid=u-6, type=SHARE]"}
        assert extract_entity_uuid(ctx) == "u-6"

    def test_non_uuid_string(self):
        assert extract_entity_uuid({"entity-uoid": "no-uuid-here"}) is None


class TestApiErrorDetail:
    def test_parses_appliance_error_list_entry(self):
        detail = ApiErrorDetail.model_validate(
            {"errorCode": "VALIDATION_VIOLATION", "message": "invalid", "args": ["name"]}
        )
        assert detail.error_code == "VALIDATION_VIOLATION"
        assert detail.message == "invalid"
        assert detail.args == ["name"]
        assert detail.to_api() == {
            "errorCode": "VALIDATION_VIOLATION",
            "message": "invalid",
            "args": ["name"],
        }

    def test_minimal_entry(self):
        detail = ApiErrorDetail.model_validate({"message": "only message"})
        assert detail.error_code is None
        assert detail.to_api() == {"message": "only message"}
