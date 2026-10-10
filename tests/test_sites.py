# tests/test_sites.py
import inspect

from hammerspace.sites import SitesClient


class TestNoDuplicates:
    def test_write_methods_defined_exactly_once(self):
        """Regression: add_remote_site, update_site and delete_remote_site were
        each defined twice; the later copies silently shadowed the earlier ones."""
        source = inspect.getsource(SitesClient)
        for name in ("add_remote_site", "update_site", "delete_remote_site"):
            assert source.count(f"def {name}(") == 1, f"{name} is defined more than once"


class TestReads:
    def test_list_all(self, mock_api):
        client = SitesClient(mock_api)
        client.get()
        assert mock_api.make_rest_call.call_args.kwargs["path"] == "/sites"

    def test_get_by_identifier(self, mock_api):
        client = SitesClient(mock_api)
        client.get("site-9")
        assert mock_api.make_rest_call.call_args.kwargs["path"] == "/sites/site-9"


class TestWrites:
    def test_add_remote_site(self, mock_api):
        client = SitesClient(mock_api)
        client.add_remote_site({"name": "remote"})
        mock_api.execute_and_monitor_task.assert_called_once()
        kwargs = mock_api.execute_and_monitor_task.call_args.kwargs
        assert kwargs["path"] == "/sites"
        assert kwargs["method"] == "POST"
        assert kwargs["initial_json_data"] == {"name": "remote"}

    def test_update_site(self, mock_api):
        client = SitesClient(mock_api)
        client.update_site("site-1", {"name": "renamed"})
        mock_api.execute_and_monitor_task.assert_called_once()
        kwargs = mock_api.execute_and_monitor_task.call_args.kwargs
        assert kwargs["path"] == "/sites/site-1"
        assert kwargs["method"] == "PUT"
        assert kwargs["initial_json_data"] == {"name": "renamed"}

    def test_delete_remote_site(self, mock_api):
        """Regression: the surviving definition called the misspelled
        execute_and_monitor__task, which would raise AttributeError."""
        client = SitesClient(mock_api)
        client.delete_remote_site("site-1")
        mock_api.execute_and_monitor_task.assert_called_once()
        kwargs = mock_api.execute_and_monitor_task.call_args.kwargs
        assert kwargs["path"] == "/sites/site-1"
        assert kwargs["method"] == "DELETE"
