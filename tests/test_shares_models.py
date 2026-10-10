# tests/test_shares_models.py
import pytest

from hammerspace.models import ExportOption, ShareCreate, ShareUpdate, ShareView
from hammerspace.shares import SharesClient

FIXTURE_SHARE = {
    "uoid": {"uuid": "abc-123", "type": "Share"},
    "name": "docs",
    "path": "/docs",
    "comment": "team docs",
    "shareState": "ONLINE",
    "exportOptions": [
        {"subnet": "*", "accessPermissions": "RW", "rootSquash": False, "insecure": True}
    ],
    "shareSizeLimit": 1000000000000,
    "warnUtilizationPercentThreshold": 90,
    "smbBrowsable": True,
    "brandNewFieldFromFutureAppliance": {"x": 1},
}


class TestShareModels:
    def test_shareview_parses_camel_case_fixture(self):
        share = ShareView.model_validate(FIXTURE_SHARE)
        assert share.name == "docs"
        assert share.uuid == "abc-123"
        assert share.share_state == "ONLINE"
        # export_options validate into the codegen ExportOptionsView; enum-valued
        assert share.export_options[0].access_permissions.value == "RW"
        assert share.export_options[0].root_squash is False

    def test_shareview_tolerates_unknown_fields_and_round_trips_them(self):
        share = ShareView.model_validate(FIXTURE_SHARE)
        dumped = share.model_dump()
        assert dumped["brandNewFieldFromFutureAppliance"] == {"x": 1}

    def test_shareview_uuid_missing(self):
        assert ShareView().uuid is None

    def test_shareview_uuid_from_task_result_extra(self):
        # Task-completion results carry the id as a top-level "uuid" key.
        share = ShareView.model_validate({"uuid": "task-entity-id"})
        assert share.uuid == "task-entity-id"

    def test_shareview_uuid_prefers_uoid(self):
        share = ShareView.model_validate(
            {"uuid": "top-level", "uoid": {"uuid": "nested"}}
        )
        assert share.uuid == "nested"

    def test_share_create_requires_name_and_path(self):
        with pytest.raises(Exception):
            ShareCreate(name="only-name")
        share = ShareCreate(name="s", path="/s")
        assert share.to_api() == {"name": "s", "path": "/s"}

    def test_share_create_serializes_camel_case(self):
        share = ShareCreate(
            name="s",
            path="/s",
            export_options=[ExportOption(subnet="*", access_permissions="RW")],
            share_size_limit=1_000_000_000_000,
            warn_utilization_percent_threshold=90,
            smb_browsable=True,
        )
        payload = share.to_api()
        assert payload["exportOptions"] == [{"subnet": "*", "accessPermissions": "RW"}]
        assert payload["shareSizeLimit"] == 1_000_000_000_000
        assert payload["smbBrowsable"] is True
        assert payload["warnUtilizationPercentThreshold"] == 90

    def test_share_update_all_optional(self):
        assert ShareUpdate().to_api() == {}
        assert ShareUpdate(name="renamed").to_api() == {"name": "renamed"}

    def test_export_option_accepts_camel_case_and_snake_case(self):
        from_alias = ExportOption.model_validate({"accessPermissions": "RO"})
        from_name = ExportOption(access_permissions="RO")
        assert from_alias.access_permissions == from_name.access_permissions == "RO"


class TestBuildShareData:
    def test_output_matches_legacy_dict_builder(self):
        client = SharesClient(api_client=None)
        data = client._build_share_data(
            name="s",
            path="/s",
            comment="c",
            export_options=[{"subnet": "*", "accessPermissions": "RW"}],
            share_size_limit=5,
            smb_browsable=True,
        )
        assert data == {
            "name": "s",
            "path": "/s",
            "comment": "c",
            "exportOptions": [{"subnet": "*", "accessPermissions": "RW"}],
            "shareSizeLimit": 5,
            "smbBrowsable": True,
        }

    def test_empty_build_returns_empty_dict(self):
        client = SharesClient(api_client=None)
        assert client._build_share_data() == {}


class TestSharesClientTyped:
    def test_get_as_model_returns_shareviews(self, client, make_response):
        client.session.request.return_value = make_response(json_data=[FIXTURE_SHARE])
        shares = client.shares.get(as_model=True)
        assert isinstance(shares, list) and all(isinstance(s, ShareView) for s in shares)
        assert shares[0].uuid == "abc-123"

    def test_get_default_returns_dicts(self, client, make_response):
        client.session.request.return_value = make_response(json_data=[FIXTURE_SHARE])
        shares = client.shares.get()
        assert isinstance(shares[0], dict)

    def test_get_as_model_single_identifier(self, client, make_response):
        client.session.request.return_value = make_response(json_data=FIXTURE_SHARE)
        share = client.shares.get("abc-123", as_model=True)
        assert isinstance(share, ShareView)
        assert client.session.request.call_args[0][1] == "https://api.example.test/shares/abc-123"

    def test_get_simple_with_models(self, client, make_response):
        client.session.request.return_value = make_response(json_data=[FIXTURE_SHARE])
        simple = client.shares.get(simple=True, as_model=True)
        assert simple == [{"uuid": "abc-123", "name": "docs", "path": "/docs"}]

    def test_create_accepts_model_body(self, client, make_response):
        client.session.request.return_value = make_response(
            status_code=200, json_data={"name": "modelled", "path": "/modelled"}
        )
        share = ShareCreate(name="modelled", path="/modelled", comment="hi")
        client.shares.create(share_data=share, monitor_task=False)
        kwargs = client.session.request.call_args.kwargs
        assert kwargs["json"] == {"name": "modelled", "path": "/modelled", "comment": "hi"}

    def test_create_sync_result_as_model(self, client, make_response):
        client.session.request.return_value = make_response(
            status_code=200, json_data={"uoid": {"uuid": "u-1"}, "name": "modelled", "path": "/modelled"}
        )
        result = client.shares.create(
            share_data=ShareCreate(name="modelled", path="/modelled"),
            monitor_task=False,
            as_model=True,
        )
        assert isinstance(result, ShareView)
        assert result.uuid == "u-1"

    def test_create_default_result_stays_dict(self, client, make_response):
        client.session.request.return_value = make_response(
            status_code=200, json_data={"uoid": {"uuid": "u-1"}, "name": "modelled", "path": "/m"}
        )
        result = client.shares.create(
            share_data=ShareCreate(name="modelled", path="/m"),
            monitor_task=False,
        )
        assert isinstance(result, dict) and result["name"] == "modelled"

    def test_update_accepts_model_body(self, client, make_response):
        client.session.request.return_value = make_response(
            status_code=200, json_data={"name": "renamed"}
        )
        client.shares.update("abc-123", share_data=ShareUpdate(name="renamed"), monitor_task=False)
        args, kwargs = client.session.request.call_args
        assert args[0] == "PUT"
        assert args[1] == "https://api.example.test/shares/abc-123"
        assert kwargs["json"] == {"name": "renamed"}

    def test_create_with_snapshots_uses_model_name(self, client, make_response, monkeypatch):
        client.session.request.return_value = make_response(
            status_code=200, json_data={"uoid": {"uuid": "u-2"}, "name": "snap", "path": "/snap"}
        )
        snapshot_calls = []
        monkeypatch.setattr(
            client.shares, "_create_share_snapshots",
            lambda *args, **kwargs: snapshot_calls.append(args),
        )
        client.shares.create(
            share_data=ShareCreate(name="snap", path="/snap"),
            create_snapshots=True,
            monitor_task=False,
        )
        assert snapshot_calls and snapshot_calls[0][0] == "snap"
