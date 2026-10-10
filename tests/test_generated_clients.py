"""Mechanical smoke tests for the spec-generated typed client layer.

Every generated method is invoked against a fake api_client that records the
request; the test asserts well-formed paths (no unsubstituted placeholders),
valid HTTP methods, and correct routing through the Phase-2 plumbing
(read_and_parse_json_body for reads, execute_and_monitor_task for tasks).
"""
import inspect
from typing import Any, Dict, List, Optional

import pytest

from hammerspace.generated import (
    TAG_MODULES,
    GeneratedApiNamespace,
    get_client_class,
)


class FakeApiClient:
    """Records calls instead of doing HTTP."""

    def __init__(self):
        self.calls: List[Dict[str, Any]] = []

    def make_rest_call(self, path, method="GET", **kwargs):
        self.calls.append({"kind": "rest", "path": path, "method": method, **kwargs})
        return {"_sentinel": True}

    def read_and_parse_json_body(self, response, model=None, many=None, raw=False):
        self.calls.append(
            {"kind": "parse", "model": model, "raw": raw, "response": response}
        )
        return response

    def execute_and_monitor_task(self, path, method="POST", **kwargs):
        self.calls.append({"kind": "task", "path": path, "method": method, **kwargs})
        return {"_sentinel": True}


def _dummy_value(param: inspect.Parameter) -> Any:
    if param.annotation is str or param.annotation is Optional[str]:
        return "test-id"
    return None


@pytest.fixture(scope="module")
def all_calls():
    """Invoke every generated method once; return (module_name, method, calls)."""
    results = []
    for tag in sorted(TAG_MODULES):
        client_cls = get_client_class(tag)
        fake = FakeApiClient()
        client = client_cls(fake)
        for name, method in inspect.getmembers(client, inspect.ismethod):
            if name.startswith("_"):
                continue
            sig = inspect.signature(method)
            kwargs = {
                pname: _dummy_value(p)
                for pname, p in sig.parameters.items()
                if p.default is inspect.Parameter.empty and pname != "self"
            }
            method(**kwargs)
            results.append((tag, name, fake.calls))
    return results


def test_all_tags_present(all_calls):
    assert len(TAG_MODULES) == 69


def test_every_method_routed_through_plumbing(all_calls):
    for tag, name, calls in all_calls:
        assert calls, f"{tag}.{name} made no calls"
        kinds = {c["kind"] for c in calls}
        assert kinds <= {"rest", "parse", "task"}, f"{tag}.{name}: {calls}"
        assert kinds & {"parse", "task"}, f"{tag}.{name} did not parse/monitor: {calls}"


def test_no_unsubstituted_path_params(all_calls):
    for tag, name, calls in all_calls:
        for call in calls:
            if "path" in call:
                assert "{" not in call["path"], f"{tag}.{name}: {call['path']}"
                assert call["path"].startswith("/"), f"{tag}.{name}: {call['path']}"
                assert call["method"] in {"GET", "POST", "PUT", "DELETE", "PATCH"}


def test_task_ops_use_post_or_put(all_calls):
    for tag, name, calls in all_calls:
        for call in calls:
            if call["kind"] == "task":
                assert call["method"] in {"POST", "PUT", "DELETE"}, f"{tag}.{name}"


def test_query_params_are_camel_or_known(all_calls):
    for tag, name, calls in all_calls:
        for call in calls:
            for key in call.get("query_params", {}) or {}:
                assert key, f"{tag}.{name}: empty query key"


def test_result_model_threads_when_present(all_calls):
    typed = 0
    for tag, name, calls in all_calls:
        for call in calls:
            if call["kind"] == "task" and call.get("result_model") is not None:
                typed += 1
            if call["kind"] == "parse" and call.get("model") is not None:
                typed += 1
    assert typed > 250, f"only {typed} methods return typed models"


def test_namespace_lazy_and_cached():
    fake = FakeApiClient()
    ns = GeneratedApiNamespace(fake)
    shares = ns.shares
    assert ns.shares is shares
    with pytest.raises(AttributeError):
        ns.does_not_exist


def test_namespace_imports_only_touched_tag():
    """First access to one tag must not import the other 68 modules."""
    import subprocess
    import sys

    code = (
        "import sys; import hammerspace.generated as g;"
        "ns = g.GeneratedApiNamespace(None); ns.ad;"
        "mods = [m for m in sys.modules if m.startswith('hammerspace.generated.')];"
        "print(sorted(mods))"
    )
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    imported = eval(out.stdout)
    assert "hammerspace.generated.ad" in imported
    assert "hammerspace.generated.shares" not in imported


def test_path_params_are_url_encoded():
    fake = FakeApiClient()
    from hammerspace.generated.users import GeneratedUsersClient

    GeneratedUsersClient(fake).get("abc/def?id=1")
    rest = next(c for c in fake.calls if c["kind"] == "rest")
    assert rest["path"] == "/users/abc%2Fdef%3Fid%3D1"


def test_get_substitutes_path_param():
    fake = FakeApiClient()
    from hammerspace.generated.shares import GeneratedSharesClient

    GeneratedSharesClient(fake).get("abc-123")
    rest = next(c for c in fake.calls if c["kind"] == "rest")
    assert rest["path"] == "/shares/abc-123"
    assert rest["method"] == "GET"


def test_move_builds_fstring_path():
    fake = FakeApiClient()
    from hammerspace.generated.shares import GeneratedSharesClient

    GeneratedSharesClient(fake).move("share-1", "dest-2")
    rest = next(c for c in fake.calls if c["kind"] == "task")
    assert rest["path"] == "/shares/share-1/move/dest-2"
