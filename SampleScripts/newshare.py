# newshare.py
import os
import logging
from dotenv import load_dotenv
from hammerspace.client import HammerspaceApiClient

# Load environment variables from .env file
load_dotenv()

# Configure basic logging for visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
# Get credentials from environment variables
HS_BASE_URL = os.getenv("HS_BASE_URL")
HS_USERNAME = os.getenv("HS_USERNAME")
HS_PASSWORD = os.getenv("HS_PASSWORD")
VERIFY_SSL = os.getenv("VERIFY_SSL", "False").lower() in ("true", "1", "t")

# Validate required environment variables
if not all([HS_BASE_URL, HS_USERNAME, HS_PASSWORD]):
    logger.error("Missing required environment variables. Please set HS_BASE_URL, HS_USERNAME, and HS_PASSWORD in .env file.")
    raise ValueError("Missing required environment variables")

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
        # --- Call Create Share Method ---
        for x in range(5):

            share_data = {
                "name": f"MarketingShare0{x}",
                "path": f"/MarketingShare0{x}", 
                "comment": "Share for the marketing department's new campaign.",
                "exportOptions": [{"subnet": "192.168.2.0/23", "accessPermissions": "RW", "rootSquash": False, "insecure": False}],
            }

            logger.info(f"Attempting to create share with data: {share_data}")

            # Simpler call if no extra query params are needed beyond the body
            result = client.shares.create_share(
                share_data=share_data,
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
