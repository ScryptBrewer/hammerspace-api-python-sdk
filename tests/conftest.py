# tests/conftest.py
import json
from unittest.mock import MagicMock

import pytest
import requests


class FakeResponse:
    """Minimal offline stand-in for requests.Response."""

    def __init__(self, status_code=200, json_data=None, headers=None, text=""):
        self.status_code = status_code
        self._json_data = json_data
        self.headers = headers if headers is not None else {"Content-Type": "application/json"}
        if text:
            self.text = text
        elif json_data is not None:
            self.text = json.dumps(json_data)
        else:
            self.text = ""
        self.content = self.text.encode("utf-8")
        self.reason = ""

    def json(self):
        if self._json_data is None:
            raise requests.exceptions.JSONDecodeError("No JSON", self.text, 0)
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"HTTP {self.status_code}", response=self
            )


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Keep tests hermetic: no ambient Hammerspace credentials or URLs."""
    for var in ("HS_BASE_URL", "HS_USERNAME", "HS_PASSWORD", "VERIFY_SSL"):
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def mock_api():
    return MagicMock()


@pytest.fixture
def make_response():
    return lambda **kwargs: FakeResponse(**kwargs)


@pytest.fixture
def client(clean_env):
    """Real client with no credentials, so no login/network on init.

    The HTTP session is replaced with a mock so tests stay fully offline.
    """
    from hammerspace import HammerspaceApiClient

    client = HammerspaceApiClient(base_url="https://api.example.test")
    client.session = MagicMock()
    return client
