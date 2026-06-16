# Hammerspace API Python SDK

Comprehensive Python library for interacting with the Hammerspace data management platform API.

## Features

- **Complete API Coverage**: Access to all Hammerspace resources and endpoints
- **Secure Authentication**: Built-in session management with automatic re-authentication
- **Advanced Error Handling**: Comprehensive exception hierarchy for easy error management
- **Automatic Retry Logic**: Intelligent retry mechanism with exponential backoff
- **Rate Limiting**: Built-in rate limiting to prevent API abuse
- **Connection Pooling**: Optimized connection management for better performance
- **Response Caching**: Optional caching for GET requests to reduce API calls
- **Task Monitoring**: Built-in support for monitoring asynchronous operations
- **Type Hints**: Full type annotations for better IDE support
- **Context Managers**: Clean resource management with context managers

## Installation

```bash
pip install hammerspace-api-client
```

## Quick Start

### Basic Configuration

```python
import os
from dotenv import load_dotenv
from hammerspace import HammerspaceApiClient

# Load environment variables
load_dotenv()

# Initialize the API client
client = HammerspaceApiClient(
    base_url=os.getenv("HS_BASE_URL"),
    username=os.getenv("HS_USERNAME"),
    password=os.getenv("HS_PASSWORD"),
    verify_ssl=os.getenv("VERIFY_SSL", "True").lower() == "true"
)
```

### Using as Context Manager

```python
with HammerspaceApiClient(
    base_url=os.getenv("HS_BASE_URL"),
    username=os.getenv("HS_USERNAME"),
    password=os.getenv("HS_PASSWORD")
) as client:
    # Your operations here
    shares = client.shares.get()
    print(f"Found {len(shares)} shares")
```

### Environment Variables

Create a `.env` file in your project root:

```env
HS_BASE_URL=https://your-hammerspace-server:8443/mgmt/v1.2/rest
HS_USERNAME=your_username
HS_PASSWORD=your_password
VERIFY_SSL=True
API_TIMEOUT=60
TASK_TIMEOUT=300
```

## Usage Examples

### Working with Shares

```python
# List all shares
all_shares = client.shares.get(simple=True)
for share in all_shares:
    print(f"Share: {share['name']} at {share['path']}")

# Create a new share
new_share = client.shares.create(
    name="marketing-data",
    path="/data/marketing",
    comment="Marketing department data",
    export_options=[
        client.shares.create_export_option(
            subnet="192.168.1.0/24",
            access_permissions="RW"
        )
    ]
)

# Update a share
updated_share = client.shares.update(
    identifier="marketing-data",
    comment="Updated comment",
    warn_utilization_percent_threshold=80
)

# Delete a share
client.shares.delete(identifier="marketing-data")
```

### Working with Snapshots

```python
# Create a file snapshot
snapshot = client.file_snapshots.create_snapshot_with_filename_expression(
    expression="/data/marketing/*"
)

# List snapshots
snapshots = client.file_snapshots.get()

# Restore from snapshot
restore_result = client.file_snapshots.restore_file_from_snapshot({
    "sourceSnapshotUuid": snapshot_uuid,
    "destinationPath": "/restored-data/"
})
```

### Task Monitoring

```python
# Create a share with task monitoring
result = client.shares.create(
    name="large-share",
    path="/data/large",
    comment="Large share with monitoring",
    monitor_task=True,
    task_timeout_seconds=600  # 10 minutes timeout
)

if result and result.get('state') == 'COMPLETED':
    print("Share created successfully!")
elif result and result.get('state') == 'FAILED':
    print(f"Share creation failed: {result.get('errorMessage')}")
```

### Error Handling

```python
from hammerspace.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    TaskFailedError
)

try:
    share = client.shares.get(identifier="nonexistent-share")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ResourceNotFoundError as e:
    print(f"Share not found: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
    for error in e.validation_errors:
        print(f"  - {error}")
except TaskFailedError as e:
    print(f"Task failed: {e}")
    print(f"Task details: {e.task_details}")
```

### Configuration Options

```python
client = HammerspaceApiClient(
    base_url="https://server:8443/mgmt/v1.2/rest",
    username="admin",
    password="password",
    timeout=60,                      # Request timeout in seconds
    verify_ssl=True,                 # SSL verification
    max_retries=3,                   # Maximum retry attempts
    retry_backoff_factor=0.5,        # Exponential backoff factor
    max_connections=10,              # Maximum connection pool size
    rate_limit_per_second=100,       # Rate limit (0 = no limit)
    enable_caching=True,             # Enable response caching
    cache_ttl=300                    # Cache TTL in seconds
)
```

### Advanced Usage

#### Connection Pooling and Rate Limiting

```python
# Configure for high-volume operations
client = HammerspaceApiClient(
    base_url=os.getenv("HS_BASE_URL"),
    username=os.getenv("HS_USERNAME"),
    password=os.getenv("HS_PASSWORD"),
    max_connections=20,              # Larger connection pool
    rate_limit_per_second=200,       # Higher rate limit
    enable_caching=True              # Enable caching
)

# Clear cache when needed
client.clear_cache()
```

#### Bulk Operations

```python
# Create multiple shares efficiently
share_configs = [
    {"name": f"share-{i}", "path": f"/data/share-{i}", "comment": f"Share {i}"}
    for i in range(10)
]

results = []
for config in share_configs:
    try:
        result = client.shares.create(
            name=config["name"],
            path=config["path"],
            comment=config["comment"],
            monitor_task=True,
            task_timeout_seconds=300
        )
        results.append({"name": config["name"], "success": True, "result": result})
    except Exception as e:
        results.append({"name": config["name"], "success": False, "error": str(e)})
```

#### Working with Files

```python
# Browse files
files = client.files.browse_files(path="/data/marketing")
for file in files:
    print(f"File: {file['name']} ({file['size']} bytes)")

# Download a file
client.files.download_file(
    path="/data/marketing/report.pdf",
    local_path="./downloaded_report.pdf"
)

# Upload a file
client.files.upload_file(
    path="/data/marketing/new_report.pdf",
    local_path="./local_report.pdf"
)

# Create directories
client.files.create_directory(path="/data/new/project")
```

### Working with Object Storage

```python
# List object storage buckets
buckets = client.data_copy_to_object.list_object_storage_buckets()
for bucket in buckets:
    print(f"Bucket: {bucket['name']}")

# Start data copy to object storage
task_data = {
    "sourcePath": "/data/backup",
    "bucketName": "my-backup-bucket",
    "prefix": "backups/"
}

result = client.data_copy_to_object.start_data_copy_to_object_task(
    task_data=task_data,
    monitor_task=True,
    task_timeout_seconds=3600  # 1 hour
)
```

## Exception Reference

The SDK provides specific exception types for different error scenarios:

- `HammerspaceApiError` - Base exception for all API errors
- `AuthenticationError` - Authentication failures (401)
- `AuthorizationError` - Authorization failures (403)
- `ResourceNotFoundError` - Resource not found (404)
- `ValidationError` - Request validation failures (400)
- `RateLimitError` - Rate limit exceeded (429)
- `ServerError` - Server errors (500+)
- `ConnectionError` - Connection failures
- `ConfigurationError` - Invalid client configuration
- `TaskTimeoutError` - Task monitoring timeout
- `TaskFailedError` - Task execution failure
- `RetryExhaustedError` - All retry attempts exhausted

## Resource Clients

The SDK provides dedicated clients for all Hammerspace resources:

- `client.ad` - Active Directory management
- `client.shares` - Share management
- `client.snapshots` - Snapshot management
- `client.files` - File operations
- `client.users` - User management
- `client.tasks` - Task management
- `client.backup` - Backup operations
- `client.events` - Event management
- And many more...

## Best Practices

### 1. Environment Variables
Always use environment variables for credentials:
```python
import os
from dotenv import load_dotenv

load_dotenv()
client = HammerspaceApiClient(
    base_url=os.getenv("HS_BASE_URL"),
    username=os.getenv("HS_USERNAME"),
    password=os.getenv("HS_PASSWORD")
)
```

### 2. Error Handling
Always implement proper error handling:
```python
try:
    result = client.shares.create(name="test", path="/test")
except ValidationError as e:
    print(f"Validation failed: {e}")
except AuthenticationError:
    print("Please check your credentials")
except TaskFailedError as e:
    print(f"Task failed: {e}")
```

### 3. Resource Management
Use context managers for proper cleanup:
```python
with HammerspaceApiClient(...) as client:
    # Your operations
    pass  # Resources automatically cleaned up
```

### 4. Task Monitoring
Always use task monitoring for long-running operations:
```python
result = client.shares.create(
    name="large-share",
    path="/large",
    monitor_task=True,
    task_timeout_seconds=600  # Set appropriate timeout
)
```

### 5. Caching
Enable caching for read-heavy workloads:
```python
client = HammerspaceApiClient(
    ...,
    enable_caching=True,
    cache_ttl=300  # Cache for 5 minutes
)
```

## Performance Tips

1. **Connection Pooling**: Increase `max_connections` for high-volume operations
2. **Caching**: Enable caching for frequently accessed data
3. **Rate Limiting**: Adjust `rate_limit_per_second` based on your API limits
4. **Timeouts**: Set appropriate timeouts based on network conditions
5. **Batch Operations**: Group operations where possible to reduce API calls

## Troubleshooting

### Common Issues

**SSL Certificate Errors**:
```python
# For development/testing only (not production)
client = HammerspaceApiClient(..., verify_ssl=False)
```

**Authentication Failures**:
- Verify credentials are correct
- Check that the user has appropriate permissions
- Ensure the base URL is correct

**Connection Timeouts**:
```python
# Increase timeout for slow networks
client = HammerspaceApiClient(..., timeout=120)
```

**Rate Limiting**:
```python
# Increase rate limit if you have API capacity
client = HammerspaceApiClient(..., rate_limit_per_second=200)
```

## Development Setup

```bash
# Clone the repository
git clone https://github.com/hammerspace/hammerspace-api-python-sdk
cd hammerspace-api-python-sdk

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black hammerspace/
isort hammerspace/
flake8 hammerspace/
mypy hammerspace/
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/hammerspace/hammerspace-api-python-sdk/issues
- Documentation: https://hammerspace-api-python-sdk.readthedocs.io
- Email: support@hammerspace.com

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.