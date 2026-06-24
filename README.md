# Hammerspace Python API Client

## Overview

The Hammerspace Python API Client is a comprehensive library that provides programmatic access to the Hammerspace data management platform. This client enables automation of various administrative tasks, configuration management, and operational workflows within a Hammerspace environment.

## Basic Setup and Configuration

### Installation

#### Prerequisites

- Python 3.8 or newer
- `pip` (bundled with Python)

#### Install from PyPI

```bash
pip install hammerspace-api-client
```

#### Install from a local checkout (recommended for development or offline use)

Installing into a virtual environment is strongly recommended so the SDK and its
dependencies don't clash with other projects. From the project root directory:

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows PowerShell

# 2. Upgrade pip, then install the package from this directory
python -m pip install --upgrade pip
pip install .
```

#### Editable (development) install

Use an editable install to make changes to the source take effect immediately
without reinstalling — ideal while developing or debugging the SDK:

```bash
pip install -e .
```

#### Install with development dependencies

Adds the linting, formatting, type-checking, and testing tooling
(pytest, black, isort, flake8, mypy, etc.):

```bash
pip install -e ".[dev]"
```

#### Build a wheel for offline installation

Build a redistributable wheel from the local source, then install it
(e.g. on a host without internet access):

```bash
python -m pip install build
python -m build            # produces dist/hammerspace_api_client-0.1.0-py3-none-any.whl
pip install dist/hammerspace_api_client-0.1.0-py3-none-any.whl
```

#### Verify the installation

```bash
python -c "import hammerspace; print(hammerspace.__version__)"
```

You should see the installed version (e.g. `0.1.0`) printed with no errors.

## Basic Configuration

The client reads its connection details from environment variables (or a local
`.env` file) rather than hardcoded values. Copy `.env.example` to `.env` and fill
in your values — `HS_BASE_URL`, `HS_USERNAME`, `HS_PASSWORD`, and `VERIFY_SSL`.

```python
from hammerspace.client import HammerspaceApiClient

# The client is configured from HS_BASE_URL / HS_USERNAME / HS_PASSWORD /
# VERIFY_SSL in your environment or .env file. No credentials in code.
client = HammerspaceApiClient()

# Now you can use the client to interact with various Hammerspace modules
# (e.g. client.shares, client.nodes, client.snapshots, ...)
```

## Creating a Basic Script
Here's a simple example script that demonstrates how to use the Hammerspace API client to list shares and create a new share:

```python
from hammerspace.client import HammerspaceApiClient

# Client is configured from your environment / .env file (see .env.example)
client = HammerspaceApiClient()

# Access the shares sub-client (the client exposes one per module)
shares = client.shares

# List all shares
all_shares = shares.get(simple=True)
print("Current shares:")
for share in all_shares:
    print(f"- {share['name']}: {share['path']}")

# Create a new share
new_share = shares.create(
    name="test-share",
    path="/data/test-share",
    comment="Test share created via API",
    export_options=[
        shares.create_export_option(subnet="192.168.1.0/24", access_permissions="RW")
    ]
)
print(f"Created new share: {new_share}")
```

## Modules and Functions
The Hammerspace API client is organized into multiple modules, each providing specific functionality. Below is a comprehensive list of all modules and their functions:

## Detailed Module Documentation

### Shares (shares.py)

The `shares.py` module provides functionality for managing shares in the Hammerspace system. Shares are the primary mechanism for exposing data to users and applications. This module enables creating, retrieving, updating, and deleting shares, as well as configuring share properties like export options, objectives, and snapshot schedules.

#### Key Functions

##### `get(identifier=None, simple=False, **kwargs)`
Retrieves share information. If an identifier is provided, fetches a specific share; otherwise, lists all shares.

**Parameters:**
- `identifier` (Optional[str]): Share UUID or name to fetch a specific share
- `simple` (bool): If True, returns only uuid, name, and path fields
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Share information or a list of shares, simplified if requested

##### `_simplify_shares_response(shares_data)`
Internal method to simplify share response to only include uuid, name, and path fields.

**Parameters:**
- `shares_data` (Union[List[Dict[str, Any]], Dict[str, Any]]): Full share data from API response

**Returns:**
- Simplified share data with only uuid, name, and path

##### `create(share_data=None, name=None, path=None, comment=None, export_options=None, share_objectives=None, share_size_limit=None, warn_utilization_percent_threshold=None, smb_browsable=None, create_snapshots=False, snapshot_schedules=None, use_default_snapshot_plans=True, monitor_task=True, task_timeout_seconds=300)`
Creates a new share with optional snapshot configuration.

**Parameters:**
- `share_data` (Optional[Dict[str, Any]]): Complete share configuration dict (if provided, other params ignored)
- `name` (Optional[str]): Share name (required if share_data not provided)
- `path` (Optional[str]): Share path (required if share_data not provided)
- `comment` (Optional[str]): Share description
- `export_options` (Optional[List[Dict[str, Any]]]): List of export option dicts
- `share_objectives` (Optional[List[Dict[str, Any]]]): List of objective dicts
- `share_size_limit` (Optional[int]): Size limit in bytes
- `warn_utilization_percent_threshold` (Optional[int]): Warning threshold percentage
- `smb_browsable` (Optional[bool]): Whether share is SMB browsable
- `create_snapshots` (bool): Whether to create snapshot schedules for this share
- `snapshot_schedules` (Optional[List[Dict[str, Any]]]): Custom snapshot schedule configurations
- `use_default_snapshot_plans` (bool): Use system default snapshot retention plans
- `monitor_task` (bool): Whether to monitor the task
- `task_timeout_seconds` (int): Task timeout

**Returns:**
- Created share information or task ID

##### `update(identifier, share_data=None, name=None, path=None, comment=None, export_options=None, share_objectives=None, share_size_limit=None, warn_utilization_percent_threshold=None, smb_browsable=None, monitor_task=True, task_timeout_seconds=300)`
Updates a specific share by its identifier.

**Parameters:**
- `identifier` (str): Share UUID or name
- `share_data` (Optional[Dict[str, Any]]): Complete share configuration dict (if provided, other params ignored)
- `name` (Optional[str]): Share name
- `path` (Optional[str]): Share path
- `comment` (Optional[str]): Share description
- `export_options` (Optional[List[Dict[str, Any]]]): List of export option dicts
- `share_objectives` (Optional[List[Dict[str, Any]]]): List of objective dicts
- `share_size_limit` (Optional[int]): Size limit in bytes
- `warn_utilization_percent_threshold` (Optional[int]): Warning threshold percentage
- `smb_browsable` (Optional[bool]): Whether share is SMB browsable
- `monitor_task` (bool): Whether to monitor the task
- `task_timeout_seconds` (int): Task timeout

**Returns:**
- Updated share information or task ID

##### `_build_share_data(name=None, path=None, comment=None, export_options=None, share_objectives=None, share_size_limit=None, warn_utilization_percent_threshold=None, smb_browsable=None)`
Internal method to build share data dictionary from individual parameters.

**Parameters:**
- `name` (Optional[str]): Share name
- `path` (Optional[str]): Share path
- `comment` (Optional[str]): Share description
- `export_options` (Optional[List[Dict[str, Any]]]): List of export configurations
- `share_objectives` (Optional[List[Dict[str, Any]]]): List of share objectives
- `share_size_limit` (Optional[int]): Size limit in bytes
- `warn_utilization_percent_threshold` (Optional[int]): Warning threshold percentage
- `smb_browsable` (Optional[bool]): SMB browsable flag

**Returns:**
- Dictionary containing share configuration

##### `create_export_option(subnet="*", access_permissions="RW", root_squash=False, insecure=False)`
Helper method to create export option dictionary.

**Parameters:**
- `subnet` (str): Network subnet (default "*" for all)
- `access_permissions` (str): "RW" or "RO"
- `root_squash` (bool): Whether to enable root squashing
- `insecure` (bool): Whether to allow insecure connections

**Returns:**
- Export option dictionary

##### `create_share_objective(objective_name, applicability="TRUE", removable=True)`
Helper method to create share objective dictionary.

**Parameters:**
- `objective_name` (str): Name of the objective (e.g., "keep-online", "optimize-for-capacity")
- `applicability` (str): Applicability condition (default "TRUE")
- `removable` (bool): Whether objective can be removed

**Returns:**
- Share objective dictionary

##### `delete(identifier, delete_snapshots=True, monitor_task=True, task_timeout_seconds=300, **kwargs)`
Deletes a specific share by its identifier, optionally deleting snapshots first.

**Parameters:**
- `identifier` (str): Share UUID or name
- `delete_snapshots` (bool): Whether to delete all snapshots before deleting share
- `monitor_task` (bool): Whether to monitor the task
- `task_timeout_seconds` (int): Task timeout
- `**kwargs`: Additional delete parameters (delete_delay, delete_path)

**Returns:**
- Delete operation result or task ID

##### `_create_share_snapshots(share_identifier, snapshot_schedules=None, use_default_plans=True, monitor_task=True, task_timeout_seconds=300)`
Internal method to create snapshot schedules for a share.

**Parameters:**
- `share_identifier` (str): Share name or UUID
- `snapshot_schedules` (Optional[List[Dict[str, Any]]]): Custom snapshot schedule configurations
- `use_default_plans` (bool): Whether to use default system retention plans
- `monitor_task` (bool): Whether to monitor tasks
- `task_timeout_seconds` (int): Task timeout

##### `_get_default_snapshot_schedules(share_identifier)`
Internal method to get default snapshot schedule configurations based on system retention plans.

**Parameters:**
- `share_identifier` (str): Share name or UUID

**Returns:**
- List of default snapshot schedule configurations

##### `_get_snapshot_retention_plans()`
Internal method to get available snapshot retention plans from the system.

**Returns:**
- List of available retention plans

##### `_delete_all_share_snapshots(share_identifier, monitor_task=True, task_timeout_seconds=300)`
Internal method to delete all snapshots and snapshot schedules for a share.

**Parameters:**
- `share_identifier` (str): Share name or UUID
- `monitor_task` (bool): Whether to monitor tasks
- `task_timeout_seconds` (int): Task timeout

##### `create_snapshot_schedule_config(name, cron_expression, retention_name, share_identifier)`
Helper method to create snapshot schedule configuration.

**Parameters:**
- `name` (str): Schedule name (e.g., "daily", "weekly")
- `cron_expression` (str): Cron expression for schedule
- `retention_name` (str): Name of retention plan to use
- `share_identifier` (str): Share name or UUID

**Returns:**
- Snapshot schedule configuration dictionary

#### Usage Examples

##### Simple Share Creation
```python
from hammerspace.client import HammerspaceApiClient

# Client is configured from your environment / .env file
client = HammerspaceApiClient()
shares = client.shares

# Create a simple share
result = shares.create(
    name="simple-share",
    path="/data/simple-share",
    comment="A simple share example"
)
print(f"Created share: {result}")
```

### Active Directory (ad.py)

The `ad.py` module provides functionality for managing Active Directory integration in the Hammerspace system. This includes retrieving, updating, and managing Active Directory configurations.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves Active Directory configuration. If an identifier is provided, fetches a specific AD configuration; otherwise, lists all AD configurations.

**Parameters:**
- `identifier` (Optional[str]): AD configuration UUID or name
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- AD configuration information or a list of configurations

##### `discover_ad_realm_info_by_domain(domain, **kwargs)`
Discovers Active Directory realm information for a specific domain.

**Parameters:**
- `domain` (str): Domain name to discover
- `**kwargs`: Optional query parameters

**Returns:**
- AD realm information for the specified domain

##### `flush_ad_cache(monitor_task=True, task_timeout_seconds=120)`
Flushes the Active Directory cache to ensure fresh data.

**Parameters:**
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Flush operation result or task ID

##### `update(identifier, ad_data, monitor_task=True, task_timeout_seconds=300)`
Updates an Active Directory configuration.

**Parameters:**
- `identifier` (str): AD configuration UUID or name
- `ad_data` (Dict[str, Any]): Updated AD configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated AD configuration information or task ID

### Antivirus (antivirus.py)

The `antivirus.py` module provides functionality for managing antivirus services in the Hammerspace system. This includes creating, retrieving, updating, and deleting antivirus service configurations.

#### Key Functions

##### `list_antivirus_services()`
Lists all antivirus services configured in the system.

**Returns:**
- List of antivirus service configurations

##### `create_antivirus_service(antivirus_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new antivirus service configuration.

**Parameters:**
- `antivirus_data` (Dict[str, Any]): Antivirus service configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created antivirus service information or task ID

##### `get(identifier)`
Retrieves a specific antivirus service configuration by its identifier.

**Parameters:**
- `identifier` (str): Antivirus service UUID or name

**Returns:**
- Antivirus service configuration information

##### `update(identifier, antivirus_data, monitor_task=True, task_timeout_seconds=300)`
Updates an antivirus service configuration.

**Parameters:**
- `identifier` (str): Antivirus service UUID or name
- `antivirus_data` (Dict[str, Any]): Updated antivirus service configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated antivirus service information or task ID

##### `delete(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes an antivirus service configuration.

**Parameters:**
- `identifier` (str): Antivirus service UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Backup (backup.py)

The `backup.py` module provides functionality for managing backups in the Hammerspace system. This includes creating, retrieving, updating, and deleting backup schedules, as well as creating immediate backups and restoring from backups.

#### Key Functions

##### `get(**kwargs)`
Retrieves backup configurations.

**Parameters:**
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- List of backup configurations

##### `create_backup_schedule(backup_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new backup schedule.

**Parameters:**
- `backup_data` (Dict[str, Any]): Backup schedule configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created backup schedule information or task ID

##### `update_backup_schedule(identifier, backup_data, monitor_task=True, task_timeout_seconds=300)`
Updates a backup schedule.

**Parameters:**
- `identifier` (str): Backup schedule UUID or name
- `backup_data` (Dict[str, Any]): Updated backup schedule configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated backup schedule information or task ID

##### `delete_backup_schedule(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a backup schedule.

**Parameters:**
- `identifier` (str): Backup schedule UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

##### `create_immediate_backup(backup_data, monitor_task=True, task_timeout_seconds=300)`
Creates an immediate backup.

**Parameters:**
- `backup_data` (Dict[str, Any]): Backup configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Backup operation result or task ID

##### `list_backups(**kwargs)`
Lists all backups.

**Parameters:**
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- List of backups

##### `restore_latest_backup(monitor_task=True, task_timeout_seconds=300)`
Restores the latest backup.

**Parameters:**
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Restore operation result or task ID

##### `restore_backup_by_name(name, monitor_task=True, task_timeout_seconds=300)`
Restores a specific backup by name.

**Parameters:**
- `name` (str): Backup name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Restore operation result or task ID

### Base Storage Volumes (base_storage_volumes.py)

The `base_storage_volumes.py` module provides functionality for managing base storage volumes in the Hammerspace system. Base storage volumes are the foundation for data storage in the system.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves base storage volume information. If an identifier is provided, fetches a specific volume; otherwise, lists all volumes.

**Parameters:**
- `identifier` (Optional[str]): Volume UUID or name to fetch a specific volume
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Volume information or a list of volumes

### Client (client.py)

The `client.py` module provides the core functionality for interacting with the Hammerspace API. It handles authentication, API calls, and task monitoring.

#### Key Functions

##### `_perform_login_action()`
Internal method to perform login action and authenticate with the Hammerspace API.

**Returns:**
- Authentication result

##### `make_rest_call(path, method, json_data=None, query_params=None, headers=None)`
Makes a REST API call to the Hammerspace server.

**Parameters:**
- `path` (str): API endpoint path
- `method` (str): HTTP method (GET, POST, PUT, DELETE)
- `json_data` (Optional[Dict[str, Any]]): JSON data for the request body
- `query_params` (Optional[Dict[str, Any]]): Query parameters
- `headers` (Optional[Dict[str, str]]): HTTP headers

**Returns:**
- API response

##### `read_and_parse_json_body(response)`
Reads and parses JSON response body from an API response.

**Parameters:**
- `response` (requests.Response): API response

**Returns:**
- Parsed JSON data

##### `execute_and_monitor_task(path, method, initial_json_data=None, initial_query_params=None, monitor_task=True, task_timeout_seconds=300)`
Executes an API call and monitors the resulting task until completion.

**Parameters:**
- `path` (str): API endpoint path
- `method` (str): HTTP method (GET, POST, PUT, DELETE)
- `initial_json_data` (Optional[Dict[str, Any]]): JSON data for the request body
- `initial_query_params` (Optional[Dict[str, Any]]): Query parameters
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Task result or task ID

### Control (cntl.py)

The `cntl.py` module provides functionality for managing cluster control operations in the Hammerspace system. This includes retrieving cluster information, updating cluster settings, accepting the EULA, and shutting down the cluster.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves cluster control information. If an identifier is provided, fetches specific information; otherwise, lists all information.

**Parameters:**
- `identifier` (Optional[str]): Control information identifier
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Cluster control information or a list of information

##### `get_cluster_state(**kwargs)`
Gets the current state of the cluster.

**Parameters:**
- `**kwargs`: Optional query parameters

**Returns:**
- Cluster state information

##### `update_cluster_info(cluster_data, monitor_task=True, task_timeout_seconds=300)`
Updates cluster information.

**Parameters:**
- `cluster_data` (Dict[str, Any]): Updated cluster configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated cluster information or task ID

##### `accept_eula(monitor_task=True, task_timeout_seconds=300)`
Accepts the End User License Agreement (EULA).

**Parameters:**
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- EULA acceptance result or task ID

##### `shutdown_cluster(monitor_task=True, task_timeout_seconds=300)`
Shuts down the cluster.

**Parameters:**
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Shutdown operation result or task ID

### Data Analytics (data_analytics.py)

The `data_analytics.py` module provides functionality for querying and analyzing data in the Hammerspace system. This includes retrieving analytics information about data usage, performance, and other metrics.

#### Key Functions

##### `query_data_analytics(**kwargs)`
Queries data analytics information.

**Parameters:**
- `**kwargs`: Query parameters for filtering and specifying the analytics query

**Returns:**
- Data analytics query results

### Data Copy to Object (data_copy_to_object.py)

The `data_copy_to_object.py` module provides functionality for copying data to object storage in the Hammerspace system. This includes starting data copy tasks and listing available object storage buckets.

#### Key Functions

##### `start_data_copy_to_object_task(task_data, monitor_task=True, task_timeout_seconds=300)`
Starts a data copy to object task.

**Parameters:**
- `task_data` (Dict[str, Any]): Task configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Task operation result or task ID

##### `list_object_storage_buckets(**kwargs)`
Lists object storage buckets.

**Parameters:**
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- List of object storage buckets

### Data Portals (data_portals.py)

The `data_portals.py` module provides functionality for managing data portals in the Hammerspace system. Data portals provide access to data for external systems and users.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves data portal information. If an identifier is provided, fetches a specific portal; otherwise, lists all portals.

**Parameters:**
- `identifier` (Optional[str]): Portal UUID or name to fetch a specific portal
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Portal information or a list of portals

##### `create_data_portal(portal_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new data portal.

**Parameters:**
- `portal_data` (Dict[str, Any]): Portal configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created portal information or task ID

##### `update_data_portal(identifier, portal_data, monitor_task=True, task_timeout_seconds=300)`
Updates a data portal.

**Parameters:**
- `identifier` (str): Portal UUID or name
- `portal_data` (Dict[str, Any]): Updated portal configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated portal information or task ID

##### `delete_data_portal(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a data portal.

**Parameters:**
- `identifier` (str): Portal UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Disk Drives (disk_drives.py)

The `disk_drives.py` module provides functionality for managing disk drives in the Hammerspace system. This includes retrieving information about physical disk drives in the system.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves disk drive information. If an identifier is provided, fetches a specific disk drive; otherwise, lists all disk drives.

**Parameters:**
- `identifier` (Optional[str]): Disk drive UUID or name to fetch a specific disk drive
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Disk drive information or a list of disk drives

### DNS (dnss.py)

The `dnss.py` module provides functionality for managing DNS server configurations in the Hammerspace system. This includes creating, retrieving, updating, and deleting DNS server configurations.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves DNS server information. If an identifier is provided, fetches a specific DNS server; otherwise, lists all DNS servers.

**Parameters:**
- `identifier` (Optional[str]): DNS server UUID or name to fetch a specific DNS server
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- DNS server information or a list of DNS servers

##### `create_dns_server(dns_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new DNS server configuration.

**Parameters:**
- `dns_data` (Dict[str, Any]): DNS server configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created DNS server information or task ID

##### `update(identifier, dns_data, monitor_task=True, task_timeout_seconds=300)`
Updates a DNS server configuration.

**Parameters:**
- `identifier` (str): DNS server UUID or name
- `dns_data` (Dict[str, Any]): Updated DNS server configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated DNS server information or task ID

##### `delete(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a DNS server configuration.

**Parameters:**
- `identifier` (str): DNS server UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Domain ID Maps (domain_idmaps.py)

The `domain_idmaps.py` module provides functionality for managing domain ID mappings in the Hammerspace system. Domain ID mappings are used to map user and group IDs between different domains.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves domain ID map information. If an identifier is provided, fetches a specific mapping; otherwise, lists all mappings.

**Parameters:**
- `identifier` (Optional[str]): Mapping UUID or name to fetch a specific mapping
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Mapping information or a list of mappings

##### `create_domain_idmap(idmap_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new domain ID map.

**Parameters:**
- `idmap_data` (Dict[str, Any]): Mapping configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created mapping information or task ID

##### `reload_domain_idmaps(monitor_task=True, task_timeout_seconds=120)`
Reloads domain ID maps to ensure they are up to date.

**Parameters:**
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Reload operation result or task ID

##### `update_domain_idmap(identifier, idmap_data, monitor_task=True, task_timeout_seconds=300)`
Updates a domain ID map.

**Parameters:**
- `identifier` (str): Mapping UUID or name
- `idmap_data` (Dict[str, Any]): Updated mapping configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated mapping information or task ID

##### `delete_domain_idmap(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a domain ID map.

**Parameters:**
- `identifier` (str): Mapping UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Events (events.py)

The `events.py` module provides functionality for managing events in the Hammerspace system. Events represent system activities, alerts, and notifications.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves event information. If an identifier is provided, fetches a specific event; otherwise, lists all events.

**Parameters:**
- `identifier` (Optional[str]): Event UUID or name to fetch a specific event
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Event information or a list of events

##### `clear(monitor_task=True, task_timeout_seconds=120)`
Clears all events.

**Parameters:**
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Clear operation result or task ID

##### `get_summary(**kwargs)`
Gets a summary of events.

**Parameters:**
- `**kwargs`: Optional query parameters for filtering and aggregation

**Returns:**
- Event summary information

##### `update_event(identifier, event_data, monitor_task=True, task_timeout_seconds=300)`
Updates an event.

**Parameters:**
- `identifier` (str): Event UUID or name
- `event_data` (Dict[str, Any]): Updated event data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated event information or task ID

### File Snapshots (file_snapshots.py)

The `file_snapshots.py` module provides functionality for managing file-level snapshots in the Hammerspace system. This includes creating, listing, updating, and deleting snapshots, as well as restoring files from snapshots and cloning files.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves file snapshot information. If an identifier is provided, fetches a specific snapshot; otherwise, lists all snapshots.

**Parameters:**
- `identifier` (Optional[str]): Snapshot UUID or name to fetch a specific snapshot
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Snapshot information or a list of snapshots

##### `create_file_snapshot_with_body(snapshot_data, monitor_task=True, task_timeout_seconds=300)`
Creates a file snapshot using the provided snapshot data.

**Parameters:**
- `snapshot_data` (Dict[str, Any]): Snapshot configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created snapshot information or task ID

##### `create_snapshot_with_filename_expression(expression, monitor_task=True, task_timeout_seconds=300)`
Creates a snapshot using a filename expression to match files.

**Parameters:**
- `expression` (str): Filename expression to match files
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created snapshot information or task ID

##### `delete_snapshot_with_expressions(expressions, monitor_task=True, task_timeout_seconds=300)`
Deletes snapshots matching the provided expressions.

**Parameters:**
- `expressions` (List[str]): List of expressions to match snapshots
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Operation result or task ID

##### `list_snapshots_with_filename_expression(expression, **kwargs)`
Lists snapshots matching a filename expression.

**Parameters:**
- `expression` (str): Filename expression to match snapshots
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- List of matching snapshots

##### `restore_file_from_snapshot(restore_data, monitor_task=True, task_timeout_seconds=300)`
Restores a file from a snapshot.

**Parameters:**
- `restore_data` (Dict[str, Any]): Restore configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Restore operation result or task ID

##### `clone_file(clone_data, monitor_task=True, task_timeout_seconds=300)`
Clones a file using the provided configuration.

**Parameters:**
- `clone_data` (Dict[str, Any]): Clone configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Clone operation result or task ID

##### `get_file_snapshot(identifier, **kwargs)`
Retrieves a specific file snapshot by its identifier.

**Parameters:**
- `identifier` (str): Snapshot UUID or name
- `**kwargs`: Optional query parameters

**Returns:**
- Snapshot information

##### `update_file_snapshot(identifier, snapshot_data, monitor_task=True, task_timeout_seconds=300)`
Updates a file snapshot.

**Parameters:**
- `identifier` (str): Snapshot UUID or name
- `snapshot_data` (Dict[str, Any]): Updated snapshot configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated snapshot information or task ID

##### `delete_file_snapshot(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a file snapshot.

**Parameters:**
- `identifier` (str): Snapshot UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Operation result or task ID

### Files (files.py)

The `files.py` module provides functionality for managing files and directories in the Hammerspace system. This includes browsing, downloading, uploading, creating, deleting, moving, and copying files and directories.

#### Key Functions

##### `browse_files(path, **kwargs)`
Browses files at a specific path.

**Parameters:**
- `path` (str): Path to browse
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- List of files and directories at the specified path

##### `download_file(path, local_path)`
Downloads a file from Hammerspace to a local path.

**Parameters:**
- `path` (str): Path of the file to download
- `local_path` (str): Local path to save the file

**Returns:**
- Download operation result

##### `upload_file(path, local_path)`
Uploads a file from a local path to Hammerspace.

**Parameters:**
- `path` (str): Path to upload the file to
- `local_path` (str): Local path of the file to upload

**Returns:**
- Upload operation result

##### `create_directory(path, monitor_task=True, task_timeout_seconds=300)`
Creates a new directory.

**Parameters:**
- `path` (str): Path of the directory to create
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Directory creation result or task ID

##### `delete_file_or_directory(path, monitor_task=True, task_timeout_seconds=300)`
Deletes a file or directory.

**Parameters:**
- `path` (str): Path of the file or directory to delete
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

##### `move_file_or_directory(source, destination, monitor_task=True, task_timeout_seconds=300)`
Moves a file or directory from source to destination.

**Parameters:**
- `source` (str): Source path
- `destination` (str): Destination path
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Move operation result or task ID

##### `copy_file_or_directory(source, destination, monitor_task=True, task_timeout_seconds=300)`
Copies a file or directory from source to destination.

**Parameters:**
- `source` (str): Source path
- `destination` (str): Destination path
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Copy operation result or task ID

### Gateways (gateways.py)

The `gateways.py` module provides functionality for managing gateways in the Hammerspace system. Gateways are used to connect to external systems and services.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves gateway information. If an identifier is provided, fetches a specific gateway; otherwise, lists all gateways.

**Parameters:**
- `identifier` (Optional[str]): Gateway UUID or name to fetch a specific gateway
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Gateway information or a list of gateways

##### `create_gateway(gateway_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new gateway.

**Parameters:**
- `gateway_data` (Dict[str, Any]): Gateway configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created gateway information or task ID

##### `update(identifier, gateway_data, monitor_task=True, task_timeout_seconds=300)`
Updates a gateway.

**Parameters:**
- `identifier` (str): Gateway UUID or name
- `gateway_data` (Dict[str, Any]): Updated gateway configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated gateway information or task ID

##### `delete(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a gateway.

**Parameters:**
- `identifier` (str): Gateway UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Heartbeat (heartbeat.py)

The `heartbeat.py` module provides functionality for checking the heartbeat of the Hammerspace system. This is useful for monitoring the health and availability of the system.

#### Key Functions

##### `get_heartbeat(**kwargs)`
Retrieves heartbeat information from the Hammerspace system.

**Parameters:**
- `**kwargs`: Optional query parameters

**Returns:**
- Heartbeat information

### Internationalization (i18n.py)

The `i18n.py` module provides functionality for managing internationalization messages in the Hammerspace system.

#### Key Functions

##### `list_i18n_messages()`
Lists all internationalization messages.

**Returns:**
- Dictionary of internationalization messages

##### `get_i18n_messages_by_locale_name(locale_name)`
Gets internationalization messages for a specific locale.

**Parameters:**
- `locale_name` (str): Name of the locale

**Returns:**
- Dictionary of internationalization messages for the specified locale

### Identity Group Mappings (identity_group_mappings.py)

The `identity_group_mappings.py` module provides functionality for managing identity group mappings in the Hammerspace system. These mappings are used to map external identity groups to internal Hammerspace groups.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves identity group mapping information. If an identifier is provided, fetches a specific mapping; otherwise, lists all mappings.

**Parameters:**
- `identifier` (Optional[str]): Mapping UUID or name to fetch a specific mapping
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Mapping information or a list of mappings

##### `create_identity_group_mapping(mapping_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new identity group mapping.

**Parameters:**
- `mapping_data` (Dict[str, Any]): Mapping configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created mapping information or task ID

##### `update(identifier, mapping_data, monitor_task=True, task_timeout_seconds=300)`
Updates an identity group mapping.

**Parameters:**
- `identifier` (str): Mapping UUID or name
- `mapping_data` (Dict[str, Any]): Updated mapping configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated mapping information or task ID

##### `delete(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes an identity group mapping.

**Parameters:**
- `identifier` (str): Mapping UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Identity (identity.py)

The `identity.py` module provides functionality for managing identities in the Hammerspace system.

#### Key Functions

##### `get(identifier)`
Retrieves identity information by identifier.

**Parameters:**
- `identifier` (str): Identity UUID or name

**Returns:**
- Identity information

### Identity Provider (idp.py)

The `idp.py` module provides functionality for managing identity providers in the Hammerspace system. Identity providers are used for authentication and authorization.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves identity provider information. If an identifier is provided, fetches a specific provider; otherwise, lists all providers.

**Parameters:**
- `identifier` (Optional[str]): Provider UUID or name to fetch a specific provider
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- Provider information or a list of providers

##### `create_idp_configuration(idp_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new identity provider configuration.

**Parameters:**
- `idp_data` (Dict[str, Any]): Provider configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created provider information or task ID

##### `update(identifier, idp_data, monitor_task=True, task_timeout_seconds=300)`
Updates an identity provider.

**Parameters:**
- `identifier` (str): Provider UUID or name
- `idp_data` (Dict[str, Any]): Updated provider configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated provider information or task ID

##### `delete(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes an identity provider.

**Parameters:**
- `identifier` (str): Provider UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

### Key Management Services (kmses.py)

The `kmses.py` module provides functionality for managing Key Management Services (KMS) in the Hammerspace system. KMS is used for encryption key management.

#### Key Functions

##### `get(identifier=None, **kwargs)`
Retrieves KMS information. If an identifier is provided, fetches a specific KMS; otherwise, lists all KMS configurations.

**Parameters:**
- `identifier` (Optional[str]): KMS UUID or name to fetch a specific KMS
- `**kwargs`: Optional query parameters for filtering and pagination

**Returns:**
- KMS information or a list of KMS configurations

##### `create_kms(kms_data, monitor_task=True, task_timeout_seconds=300)`
Creates a new KMS.

**Parameters:**
- `kms_data` (Dict[str, Any]): KMS configuration data
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Created KMS information or task ID

##### `update(identifier, kms_data, monitor_task=True, task_timeout_seconds=300)`
Updates a KMS.

**Parameters:**
- `identifier` (str): KMS UUID or name
- `kms_data` (Dict[str, Any]): Updated KMS configuration
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Updated KMS information or task ID

##### `delete(identifier, monitor_task=True, task_timeout_seconds=300)`
Deletes a KMS.

**Parameters:**
- `identifier` (str): KMS UUID or name
- `monitor_task` (bool): Whether to monitor the task until completion
- `task_timeout_seconds` (int): Task timeout in seconds

**Returns:**
- Delete operation result or task ID

