# hammerspace/modeler.py
import logging
from typing import Optional, Dict, Any, Union
logger = logging.getLogger(__name__)

class ModelerClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def trigger_tree_stats_sweep( # Renamed from create_tree_stats
        self, share: str, monitor_task: bool = True, task_timeout_seconds: int = 300
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Trigger a tree stats sweep for a share. (POST /modeler/tree-stats/trigger-sweep/{share})
        OpId: createTreeStats (Returns 202 Accepted)
        """
        path = f"/modeler/tree-stats/trigger-sweep/{share}"
        logger.info(f"Triggering tree stats sweep for share: {share}")
        # No query params or body defined in spec for this POST
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST",
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )

    def get_latest_tree_stats(self, share: str) -> Optional[Dict[str, Any]]: # Renamed from get_tree_stats
        """
        Get latest tree stats of a share. (GET /modeler/tree-stats/{share})
        OpId: getTreeStats (Default response)
        """
        path = f"/modeler/tree-stats/{share}"
        logger.info(f"Getting latest tree stats for share: {share}")
        # No query params defined in spec for this GET
        response = self.api_client.make_rest_call(path=path, method="GET")
        return self.api_client.read_and_parse_json_body(response)