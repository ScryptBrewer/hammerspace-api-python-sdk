import os
from dotenv import load_dotenv
from hammerspace.client import HammerspaceApiClient

# Load environment variables from .env file
load_dotenv()

SHARE_NAME = os.getenv("SHARE_NAME", "Share007")

# Get credentials from environment variables
client = HammerspaceApiClient(
            base_url=os.getenv("HS_BASE_URL", "https://ANVILSERVER:8443/mgmt/v1.2/rest"),
            username=os.getenv("HS_USERNAME", "admin"),
            password=os.getenv("HS_PASSWORD"),
            verify_ssl=os.getenv("VERIFY_SSL", "False").lower() in ("true", "1", "t")
        )

## Create share Example
share_data = {
                "name": f"{SHARE_NAME}",
                "path": f"/{SHARE_NAME}", 
                "comment": "Share for the MI6 department's new campaign.",
                "exportOptions": [{"subnet": "192.168.2.0/23", "accessPermissions": "RW", "rootSquash": False, "insecure": False}],
            }

result = client.shares.create_share(
    share_data=share_data,
    monitor_task=True,
    task_timeout_seconds=600
)

# print(result)
# print("Final Status::",result.get('status',{}))

# Delete Share Example
# share_data = client.shares.get(spec=f"name=eq={SHARE_NAME}")

# if len(share_data) == 1:
#     result = client.shares.delete_share(share_data[0].get('uoid',{}).get('uuid', {}))
#     print(result)
# else:
#     print(f"Failed to delete due to incorrect share count: {len(share_data)}")

