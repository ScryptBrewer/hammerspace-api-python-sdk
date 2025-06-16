# example_create_share.py
import logging
from hammerspace.client import HammerspaceApiClient

# Configure basic logging for visibility
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
# Replace with your Hammerspace API details
HS_BASE_URL = "https://ANVILSERVER:8443/mgmt/v1.2/rest" # Or your specific version
HS_USERNAME = "admin"
HS_PASSWORD = "Your Password"
VERIFY_SSL = False # Set to True in production with valid certs

def main():
    logger.info("Initializing Hammerspace API client...")
    try:
        client = HammerspaceApiClient(
            base_url=HS_BASE_URL,
            username=HS_USERNAME,
            password=HS_PASSWORD,
            verify_ssl=VERIFY_SSL
        )
        logger.info("Client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize client: {e}")
        return

    try:
        # To update a existing share you must grab all data from the share then update desired values then
        # write the whole json back.

        for x in range(2):

            find_data = client.shares.get(
                spec=f"name=eq=MarketingShare0{x}")
            
            find_data[0]['comment'] = "this is a new Comment for the share UPDATED!!!!"
            
            # Simpler call if no extra query params are needed beyond the body
            result = client.shares.update_share(
                identifier=find_data[0].get('uoid', {}).get('uuid'),
                share_data=find_data[0],
                monitor_task=True, # Set to False if you know it's always synchronous (200 OK)
                task_timeout_seconds=600
            )

            if result:
                logger.info("Create share operation successful.")
                if isinstance(result, str): # Likely a task ID
                    logger.info(f"Task ID for share creation: {result}")
                    logger.info("Monitor this task ID using the TasksClient or check the UI.")
                elif isinstance(result, dict) and result.get("state") and result.get("uuid"): # Task object
                    logger.info(f"Share creation task details: {result}")
                    if result.get("state", "").upper() == "COMPLETED":
                        logger.info(f"Share created successfully (from task result): {result.get('result', result)}")
                    else:
                        logger.warning(f"Share creation task ended with state: {result.get('state')}")
                elif isinstance(result, dict): # Direct ShareView object
                    logger.info(f"Share created successfully (direct response): {result}")
                else:
                    logger.info(f"Create share response: {result}")
            else:
                logger.error("Create share operation failed or returned no result.")

    except Exception as e:
        logger.error(f"An error occurred during share creation: {e}", exc_info=True)

if __name__ == "__main__":
    main()
