# tests/test_package.py
from unittest.mock import MagicMock

import hammerspace


def _exported_client_classes():
    return [
        getattr(hammerspace, name)
        for name in dir(hammerspace)
        if name.endswith("Client")
        and isinstance(getattr(hammerspace, name), type)
        and name != "HammerspaceApiClient"
    ]


def test_package_exports_resource_clients():
    classes = _exported_client_classes()
    assert len(classes) >= 60
    assert hammerspace.HammerspaceApiClient is not None


def test_version_is_exposed():
    assert isinstance(hammerspace.__version__, str)
    assert hammerspace.__version__


def test_every_resource_client_instantiates():
    """Broad smoke test: catches broken constructors (e.g. missing `self`)."""
    api = MagicMock()
    for cls in _exported_client_classes():
        instance = cls(api)
        assert instance.api_client is api


def test_top_level_client_builds_all_resources():
    client = hammerspace.HammerspaceApiClient(base_url="https://api.example.test")
    for cls in _exported_client_classes():
        found = any(
            isinstance(getattr(client, attr, None), cls)
            for attr in dir(client)
            if not attr.startswith("_")
        )
        assert found, f"No attribute of HammerspaceApiClient is a {cls.__name__}"
