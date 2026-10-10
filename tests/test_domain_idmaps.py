# tests/test_domain_idmaps.py
from hammerspace.domain_idmaps import DomainIdmapsClient


class TestGet:
    def test_list_all_does_not_raise_nameerror(self, mock_api):
        """Regression: get() was defined without `self` and raised NameError."""
        client = DomainIdmapsClient(mock_api)
        client.get()
        mock_api.make_rest_call.assert_called_once_with(
            path="/domain-idmaps", method="GET", query_params={}
        )

    def test_get_by_identifier(self, mock_api):
        client = DomainIdmapsClient(mock_api)
        client.get("abc-123")
        mock_api.make_rest_call.assert_called_once_with(
            path="/domain-idmaps/abc-123", method="GET", query_params={}
        )

    def test_query_param_mapping(self, mock_api):
        client = DomainIdmapsClient(mock_api)
        client.get(page=2, page_size=25, page_sort="name", spec="s", page_sort_dir="desc")
        mock_api.make_rest_call.assert_called_once_with(
            path="/domain-idmaps",
            method="GET",
            query_params={
                "spec": "s",
                "page": 2,
                "page.size": 25,
                "page.sort": "name",
                "page.sort.dir": "desc",
            },
        )

    def test_result_parsed_from_response(self, mock_api):
        mock_api.make_rest_call.return_value = object()
        mock_api.read_and_parse_json_body.return_value = [{"id": "map-1"}]
        client = DomainIdmapsClient(mock_api)
        assert client.get() == [{"id": "map-1"}]


class TestDelegations:
    def test_create(self, mock_api):
        client = DomainIdmapsClient(mock_api)
        client.create_domain_idmap({"source": "AD"})
        mock_api.execute_and_monitor_task.assert_called_once_with(
            path="/domain-idmaps",
            method="POST",
            initial_json_data={"source": "AD"},
            monitor_task=True,
            task_timeout_seconds=300,
        )

    def test_reload(self, mock_api):
        client = DomainIdmapsClient(mock_api)
        client.reload_domain_idmaps()
        mock_api.execute_and_monitor_task.assert_called_once_with(
            path="/domain-idmaps/reload",
            method="POST",
            monitor_task=True,
            task_timeout_seconds=120,
        )

    def test_update(self, mock_api):
        client = DomainIdmapsClient(mock_api)
        client.update_domain_idmap("id-1", {"source": "LDAP"}, monitor_task=False)
        mock_api.execute_and_monitor_task.assert_called_once_with(
            path="/domain-idmaps/id-1",
            method="PUT",
            initial_json_data={"source": "LDAP"},
            monitor_task=False,
            task_timeout_seconds=300,
        )

    def test_delete(self, mock_api):
        client = DomainIdmapsClient(mock_api)
        client.delete_domain_idmap("id-1")
        mock_api.execute_and_monitor_task.assert_called_once_with(
            path="/domain-idmaps/id-1",
            method="DELETE",
            monitor_task=True,
            task_timeout_seconds=300,
        )
