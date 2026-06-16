# API Reference

## HammerspaceApiClient

The main client class for interacting with the Hammerspace API.

### Initialization

```python
HammerspaceApiClient(
    base_url: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: int = 60,
    verify_ssl: bool = True,
    max_retries: int = 3,
    retry_backoff_factor: float = 0.5,
    max_connections: int = 10,
    rate_limit_per_second: int = 100,
    enable_caching: bool = True,
    cache_ttl: int = 300
)
```

#### Parameters

- **base_url** (str): The base URL of the Hammerspace API server
- **username** (Optional[str]): Username for authentication
- **password** (Optional[str]): Password for authentication
- **timeout** (int): Request timeout in seconds (default: 60)
- **verify_ssl** (bool): Whether to verify SSL certificates (default: True)
- **max_retries** (int): Maximum number of retry attempts (default: 3)
- **retry_backoff_factor** (float): Exponential backoff factor (default: 0.5)
- **max_connections** (int): Maximum connection pool size (default: 10)
- **rate_limit_per_second** (int): Maximum requests per second (default: 100, 0 = no limit)
- **enable_caching** (bool): Enable response caching for GET requests (default: True)
- **cache_ttl** (int): Cache time-to-live in seconds (default: 300)

#### Methods

##### `make_rest_call()`

Makes a REST API call to the Hammerspace server.

```python
make_rest_call(
    path: str,
    method: str = "GET",
    json_data: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, IO]] = None,
    stream: bool = False,
    data: Optional[Dict[str, Any]] = None,
    is_login: bool = False,
    is_absolute_url: bool = False,
    custom_headers: Optional[Dict[str, str]] = None,
    _is_retry_after_relogin: bool = False
) -> requests.Response
```

##### `execute_and_monitor_task()`

Executes an API call and monitors the resulting task until completion.

```python
execute_and_monitor_task(
    path: str,
    method: str = "POST",
    initial_json_data: Optional[Dict[str, Any]] = None,
    initial_query_params: Optional[Dict[str, Any]] = None,
    initial_headers: Optional[Dict[str, str]] = None,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300,
    poll_interval_seconds: int = 5
) -> Union[Optional[str], Optional[Dict[str, Any]], Optional[List[Any]]]
```

##### `clear_cache()`

Clears the entire response cache.

```python
clear_cache() -> None
```

##### `close()`

Closes the session and cleans up resources.

```python
close() -> None
```

##### `session_context()`

Context manager for the client session.

```python
@contextmanager
def session_context(self) -> None
```

## SharesClient

Manages shares in the Hammerspace system.

### Methods

#### `get()`

Retrieves share information.

```python
get(
    identifier: Optional[str] = None,
    simple: bool = False,
    **kwargs
) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]
```

**Parameters:**
- **identifier** (Optional[str]): Share UUID or name to fetch specific share
- **simple** (bool): If True, returns only uuid, name, and path fields
- **\*\*kwargs**: Optional query parameters (spec, page, page_size, page_sort, page_sort_dir)

**Returns:** Share information or list of shares

#### `create()`

Creates a new share.

```python
create(
    share_data: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    path: Optional[str] = None,
    comment: Optional[str] = None,
    export_options: Optional[List[Dict[str, Any]]] = None,
    share_objectives: Optional[List[Dict[str, Any]]] = None,
    share_size_limit: Optional[int] = None,
    warn_utilization_percent_threshold: Optional[int] = None,
    smb_browsable: Optional[bool] = None,
    create_snapshots: bool = False,
    snapshot_schedules: Optional[List[Dict[str, Any]]] = None,
    use_default_snapshot_plans: bool = True,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `update()`

Updates a specific share.

```python
update(
    identifier: str,
    share_data: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    path: Optional[str] = None,
    comment: Optional[str] = None,
    export_options: Optional[List[Dict[str, Any]]] = None,
    share_objectives: Optional[List[Dict[str, Any]]] = None,
    share_size_limit: Optional[int] = None,
    warn_utilization_percent_threshold: Optional[int] = None,
    smb_browsable: Optional[bool] = None,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `delete()`

Deletes a specific share.

```python
delete(
    identifier: str,
    delete_snapshots: bool = True,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300,
    **kwargs
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `create_export_option()`

Helper method to create export option dictionary.

```python
create_export_option(
    subnet: str = "*",
    access_permissions: str = "RW",
    root_squash: bool = False,
    insecure: bool = False
) -> Dict[str, Any]
```

#### `create_share_objective()`

Helper method to create share objective dictionary.

```python
create_share_objective(
    objective_name: str,
    applicability: str = "TRUE",
    removable: bool = True
) -> Dict[str, Any]
```

## FileSnapshotsClient

Manages file-level snapshots.

### Methods

#### `get()`

Retrieves file snapshot information.

```python
get(
    identifier: Optional[str] = None,
    **kwargs
) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]
```

#### `create_file_snapshot_with_body()`

Creates a file snapshot using provided snapshot data.

```python
create_file_snapshot_with_body(
    snapshot_data: Dict[str, Any],
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `create_snapshot_with_filename_expression()`

Creates a snapshot using a filename expression.

```python
create_snapshot_with_filename_expression(
    expression: str,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `delete_snapshot_with_expressions()`

Deletes snapshots matching expressions.

```python
delete_snapshot_with_expressions(
    expressions: List[str],
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `restore_file_from_snapshot()`

Restores a file from a snapshot.

```python
restore_file_from_snapshot(
    restore_data: Dict[str, Any],
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

## FilesClient

Manages files and directories.

### Methods

#### `browse_files()`

Browses files at a specific path.

```python
browse_files(
    path: str,
    **kwargs
) -> List[Dict[str, Any]]
```

#### `download_file()`

Downloads a file from Hammerspace to a local path.

```python
download_file(
    path: str,
    local_path: str
) -> Dict[str, Any]
```

#### `upload_file()`

Uploads a file from a local path to Hammerspace.

```python
upload_file(
    path: str,
    local_path: str
) -> Dict[str, Any]
```

#### `create_directory()`

Creates a new directory.

```python
create_directory(
    path: str,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `delete_file_or_directory()`

Deletes a file or directory.

```python
delete_file_or_directory(
    path: str,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `move_file_or_directory()`

Moves a file or directory.

```python
move_file_or_directory(
    source: str,
    destination: str,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `copy_file_or_directory()`

Copies a file or directory.

```python
copy_file_or_directory(
    source: str,
    destination: str,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

## BackupClient

Manages backup operations.

### Methods

#### `get()`

Retrieves backup configurations.

```python
get(**kwargs) -> List[Dict[str, Any]]
```

#### `create_backup_schedule()`

Creates a new backup schedule.

```python
create_backup_schedule(
    backup_data: Dict[str, Any],
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `update_backup_schedule()`

Updates a backup schedule.

```python
update_backup_schedule(
    identifier: str,
    backup_data: Dict[str, Any],
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `delete_backup_schedule()`

Deletes a backup schedule.

```python
delete_backup_schedule(
    identifier: str,
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `create_immediate_backup()`

Creates an immediate backup.

```python
create_immediate_backup(
    backup_data: Dict[str, Any],
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `list_backups()`

Lists all backups.

```python
list_backups(**kwargs) -> List[Dict[str, Any]]
```

#### `restore_latest_backup()`

Restores the latest backup.

```python
restore_latest_backup(
    monitor_task: bool = True,
    task_timeout_seconds: int = 300
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

## TasksClient

Manages task operations.

### Methods

#### `get()`

Retrieves task information.

```python
get(
    identifier: Optional[str] = None,
    **kwargs
) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]
```

#### `monitor_task()`

Monitors a specific task.

```python
monitor_task(
    task_id: str,
    timeout_seconds: int = 300,
    poll_interval_seconds: int = 5
) -> Dict[str, Any]
```

## EventsClient

Manages system events.

### Methods

#### `get()`

Retrieves event information.

```python
get(
    identifier: Optional[str] = None,
    **kwargs
) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]
```

#### `clear()`

Clears all events.

```python
clear(
    monitor_task: bool = True,
    task_timeout_seconds: int = 120
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

#### `get_summary()`

Gets a summary of events.

```python
get_summary(**kwargs) -> Dict[str, Any]
```

## AdClient

Manages Active Directory integration.

### Methods

#### `get()`

Retrieves Active Directory configuration.

```python
get(
    identifier: Optional[str] = None,
    **kwargs
) -> Union[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]
```

#### `discover_ad_realm_info_by_domain()`

Discovers Active Directory realm information.

```python
discover_ad_realm_info_by_domain(
    domain: str,
    **kwargs
) -> Dict[str, Any]
```

#### `flush_ad_cache()`

Flushes the Active Directory cache.

```python
flush_ad_cache(
    monitor_task: bool = True,
    task_timeout_seconds: int = 120
) -> Union[Optional[str], Optional[Dict[str, Any]]]
```

## Additional Resource Clients

The SDK includes many more resource clients:

- `AntivirusClient` - Antivirus service management
- `BaseStorageVolumesClient` - Base storage volume management
- `CntlClient` - Cluster control operations
- `DataAnalyticsClient` - Data analytics queries
- `DataCopyToObjectClient` - Data copy to object storage
- `DataPortalsClient` - Data portal management
- `DiskDrivesClient` - Physical disk drive information
- `DnssClient` - DNS server configuration
- `DomainIdmapsClient` - Domain ID mapping management
- `GatewaysClient` - Gateway management
- `HeartbeatClient` - System health checks
- `I18nClient` - Internationalization messages
- `IdentityGroupMappingsClient` - Identity group mapping
- `IdentityClient` - Identity management
- `IdpClient` - Identity provider configuration
- `KmsesClient` - Key management services
- `LabelsClient` - Label management
- `LdapsClient` - LDAP configuration
- `LicenseServerClient` - License server management
- `LicensesClient` - License management
- `LogicalVolumesClient` - Logical volume management
- `LoginPolicyClient` - Login policy management
- `LoginClient` - Login operations
- `MailsmtpClient` - SMTP configuration
- `MetricsClient` - System metrics
- `ModelerClient` - Data modeling operations
- `NetworkInterfacesClient` - Network interface configuration
- `NisClient` - NIS configuration
- `NodesClient` - Node management
- `NotificationRulesClient` - Notification rule management
- `NtpsClient` - NTP server configuration
- `ObjectStorageVolumesClient` - Object storage volume management
- `ObjectStoreLogicalVolumesClient` - Object store logical volumes
- `ObjectStoresClient` - Object store management
- `ObjectivesClient` - Storage objective management
- `PdNodeCntlClient` - Platform node control
- `PdSupportClient` - Platform support operations
- `ProcessorClient` - Processor management
- `ReportsClient` - Report generation
- `RolesClient` - Role management
- `S3ServerClient` - S3 server configuration
- `SchedulesClient` - Schedule management
- `ShareParticipantsClient` - Share participant management
- `ShareReplicationsClient` - Share replication management
- `ShareSnapshotsClient` - Share snapshot management
- `SitesClient` - Site management
- `SnapshotRetentionsClient` - Snapshot retention management
- `SnmpClient` - SNMP configuration
- `StaticRoutesClient` - Static route configuration
- `StorageVolumesClient` - Storage volume management
- `SubnetGatewaysClient` - Subnet gateway management
- `SwUpdateClient` - Software update management
- `SyslogClient` - Syslog configuration
- `SystemInfoClient` - System information
- `SystemClient` - System management
- `UserGroupsClient` - User group management
- `UsersClient` - User management
- `VersionsClient` - Version information
- `VolumeGroupsClient` - Volume group management

## Exception Reference

### Base Exception

#### `HammerspaceApiError`

Base exception for all Hammerspace API errors.

```python
HammerspaceApiError(
    message: str,
    status_code: int = None,
    response_text: str = None,
    error_code: str = None
)
```

**Attributes:**
- `message` (str): Error message
- `status_code` (int): HTTP status code
- `response_text` (str): Raw response text
- `error_code` (str): API error code

### Authentication & Authorization

#### `AuthenticationError`

Authentication failures (HTTP 401).

```python
AuthenticationError(
    message: str = "Authentication failed",
    status_code: int = 401,
    response_text: str = None
)
```

#### `AuthorizationError`

Authorization failures (HTTP 403).

```python
AuthorizationError(
    message: str = "Authorization failed - insufficient permissions",
    status_code: int = 403,
    response_text: str = None
)
```

### Resource Errors

#### `ResourceNotFoundError`

Resource not found (HTTP 404).

```python
ResourceNotFoundError(
    message: str = "Resource not found",
    status_code: int = 404,
    response_text: str = None
)
```

#### `ValidationError`

Request validation failures (HTTP 400).

```python
ValidationError(
    message: str = "Request validation failed",
    status_code: int = 400,
    response_text: str = None,
    validation_errors: list = None
)
```

**Additional Attributes:**
- `validation_errors` (list): List of validation error details

### Rate Limiting & Server Errors

#### `RateLimitError`

Rate limit exceeded (HTTP 429).

```python
RateLimitError(
    message: str = "Rate limit exceeded",
    status_code: int = 429,
    response_text: str = None,
    retry_after: int = None
)
```

**Additional Attributes:**
- `retry_after` (int): Seconds to wait before retrying

#### `ServerError`

Server errors (HTTP 500+).

```python
ServerError(
    message: str = "Server error occurred",
    status_code: int = 500,
    response_text: str = None
)
```

### Connection & Configuration

#### `ConnectionError`

Connection failures.

```python
ConnectionError(
    message: str = "Connection to API server failed",
    original_error: Exception = None
)
```

**Additional Attributes:**
- `original_error` (Exception): Original exception that caused the connection error

#### `ConfigurationError`

Invalid client configuration.

```python
ConfigurationError(
    message: str = "Invalid client configuration"
)
```

### Task Management

#### `TaskTimeoutError`

Task monitoring timeout.

```python
TaskTimeoutError(
    message: str = "Task monitoring timed out",
    task_id: str = None,
    timeout_seconds: int = None
)
```

**Additional Attributes:**
- `task_id` (str): ID of the timed-out task
- `timeout_seconds` (int): Timeout duration in seconds

#### `TaskFailedError`

Task execution failure.

```python
TaskFailedError(
    message: str = "Task failed",
    task_details: dict = None,
    status_code: int = None,
    response_text: str = None
)
```

**Additional Attributes:**
- `task_details` (dict): Detailed task information
- `task_id` (str): Extracted task ID from task_details

### Retry Errors

#### `RetryExhaustedError`

All retry attempts exhausted.

```python
RetryExhaustedError(
    message: str = "All retry attempts exhausted",
    total_attempts: int = None,
    last_error: Exception = None
)
```

**Additional Attributes:**
- `total_attempts` (int): Total number of retry attempts
- `last_error` (Exception): The last error that occurred

## Error Handling Examples

### Basic Error Handling

```python
from hammerspace.exceptions import (
    HammerspaceApiError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError
)

try:
    share = client.shares.create(name="test", path="/test")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print(f"Status code: {e.status_code}")
except ResourceNotFoundError as e:
    print(f"Resource not found: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
    for error in e.validation_errors:
        print(f"  - {error}")
except HammerspaceApiError as e:
    print(f"API error: {e}")
    print(f"Error code: {e.error_code}")
```

### Task Error Handling

```python
from hammerspace.exceptions import TaskFailedError, TaskTimeoutError

try:
    result = client.shares.create(
        name="large-share",
        path="/large",
        monitor_task=True,
        task_timeout_seconds=600
    )
except TaskTimeoutError as e:
    print(f"Task timed out after {e.timeout_seconds} seconds")
    print(f"Task ID: {e.task_id}")
except TaskFailedError as e:
    print(f"Task failed: {e}")
    print(f"Task details: {e.task_details}")
    print(f"Error message: {e.task_details.get('errorMessage', 'Unknown')}")
```

### Retry Error Handling

```python
from hammerspace.exceptions import RetryExhaustedError

try:
    result = client.shares.get(identifier="large-share")
except RetryExhaustedError as e:
    print(f"Failed after {e.total_attempts} attempts")
    print(f"Last error: {e.last_error}")
    # Implement fallback logic
```

### Connection Error Handling

```python
from hammerspace.exceptions import ConnectionError

try:
    result = client.shares.get()
except ConnectionError as e:
    print(f"Connection error: {e}")
    print(f"Original error: {e.original_error}")
    # Implement retry logic or fallback
```