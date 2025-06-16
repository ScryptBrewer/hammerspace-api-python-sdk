# hammerspace/pd_support.py
import logging
from typing import Dict, Any, Union, Optional
logger = logging.getLogger(__name__)

class PdSupportClient:
    def __init__(self, api_client: Any):
        self.api_client = api_client

    def create_support_bundle( 
        self, support_data: Dict[str, Any],
        monitor_task: bool = True, task_timeout_seconds: int = 600 # Bundles can be large
    ) -> Union[Optional[str], Optional[Dict[str, Any]]]:
        """
        Collect logs for support. (POST /pd-support) - OpId: createPdSupport
        support_data: The request body (PdSupportView schema).
        """
        path = "/pd-support"
        logger.info(f"Creating support bundle with data: {support_data}")
        headers = {'Content-Type': 'application/json'} 
        return self.api_client.execute_and_monitor_task(
            path=path, method="POST", initial_json_data=support_data, initial_headers=headers,
            monitor_task=monitor_task, task_timeout_seconds=task_timeout_seconds
        )