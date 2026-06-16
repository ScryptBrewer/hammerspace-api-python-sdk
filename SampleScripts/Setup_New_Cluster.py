import os
from dotenv import load_dotenv
from hammerspace.client import HammerspaceApiClient

# Load environment variables from .env file
load_dotenv()

SHARE_NAME = os.getenv("SHARE_NAME", "MyShare")

# Get credentials from environment variables
client = HammerspaceApiClient(
            base_url=os.getenv("HS_BASE_URL", "https://ANVILSERVER:8443/mgmt/v1.2/rest"),
            username=os.getenv("HS_USERNAME", "admin"),
            password=os.getenv("HS_PASSWORD"),
            verify_ssl=os.getenv("VERIFY_SSL", "False").lower() in ("true", "1", "t")
        )


#result = client.logical_volumes.get()
#result = client.licenses.get()
#result = client.ad.get()
#result = client.object_stores.get()
#result = client.backup.get()
#result = client.cntl.get()
#result = client.cntl.get_cluster_state()
#result = client.cntl.accept_eula()
#result = client.licenses.create_license(license_data={f"'activation_id':{ACTiVATION_ID}"})
#result = client.cntl.shutdown_cluster()
#result = client.data_portals.get()
#result =  client.disk_drives.get()
#result = client.dnss.get()
#result = client.data_copy_to_object.list_object_storage_buckets()
#result = client.events.get()
#result = client.events.clear()
#result = client.events.get_summary()
#result = client.file_snapshots.create_file_snapshot(filenameexpression=f"{SHARE_NAME}")
result = client.sites.get()

print(result)
#print("Final Status::",result.get('status',{}))


