# example_create_share_model.py
"""Create a share using pydantic models and receive typed results."""
import os
import logging
from dotenv import load_dotenv
from hammerspace.client import HammerspaceApiClient
from hammerspace.models import ExportOption, ShareCreate, ShareView

# Load environment variables from .env file
load_dotenv()

# Configure basic logging for visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
HS_BASE_URL = os.getenv("HS_BASE_URL")
HS_USERNAME = os.getenv("HS_USERNAME")
HS_PASSWORD = os.getenv("HS_PASSWORD")
VERIFY_SSL = os.getenv("VERIFY_SSL", "False").lower() in ("true", "1", "t")

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

    # --- Define the share with a validated model ---
    # snake_case attributes serialize to the API's camelCase fields
    # (export_options -> exportOptions); unknown/optional fields are omitted.
    share = ShareCreate(
        name="MyNewMarketingShare",
        path="/MyNewMarketingShare",
        comment="Share for the marketing department's new campaign.",
        export_options=[
            ExportOption(subnet="*", access_permissions="RW"),
        ],
        share_size_limit=1_000_000_000_000,
        warn_utilization_percent_threshold=90,
        smb_browsable=True,
    )

    logger.info(f"Attempting to create share: {share.name}")

    try:
        result = client.shares.create(
            share_data=share,          # model accepted directly
            monitor_task=True,
            task_timeout_seconds=600,
            as_model=True,             # typed ShareView result when the API returns one
        )

        if isinstance(result, ShareView):
            logger.info(f"Share created: uuid={result.uuid} name={result.name} path={result.path}")
        elif isinstance(result, dict):
            logger.info(f"Create share task/result data: {result}")
        elif isinstance(result, str):
            logger.info(f"Share creation task ID: {result}")
        else:
            logger.warning(f"Unexpected create response: {result}")

        # --- Typed listing ---
        for s in client.shares.get(as_model=True) or []:
            logger.info(f"Share: {s.name} -> {s.uuid} ({s.path})")

    except Exception as e:
        logger.error(f"An error occurred during share creation: {e}", exc_info=True)

if __name__ == "__main__":
    main()
