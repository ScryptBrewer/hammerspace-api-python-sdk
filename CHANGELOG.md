# CHANGELOG

All notable changes to the Hammerspace API Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive exception hierarchy with 10+ specific exception types
- Automatic retry logic with exponential backoff
- Rate limiting support with configurable limits
- Connection pooling for improved performance
- Response caching for GET requests with configurable TTL
- Context manager support for proper resource management
- Environment variable support for secure credential management
- Enhanced error messages with detailed context
- Session management with automatic re-authentication
- Task monitoring with specific timeout and failure exceptions
- Structured logging with improved debugging information
- Configuration validation in sample scripts
- `.env.example` template for secure credential setup
- Comprehensive API documentation
- User guide with extensive examples
- Setup and usage best practices

### Changed
- Improved security by removing hardcoded credentials from all sample scripts
- Enhanced dependency management with `pyproject.toml`
- Better error handling throughout the codebase
- More descriptive error messages and logging
- Enhanced task monitoring with proper exception handling

### Fixed
- Critical security vulnerabilities (hardcoded credentials)
- Fragile dependency management
- Generic error handling without specific exception types
- Poor error context and debugging information
- Task monitoring errors silently returned

### Security
- Removed all hardcoded credentials from source code
- Added secure credential management with environment variables
- Implemented proper `.gitignore` for sensitive files
- Added credential validation to prevent silent failures

## [0.1.0] - 2024-06-16

### Added
- Initial release of Hammerspace API Python SDK
- Complete API coverage for all Hammerspace resources
- Basic authentication and session management
- Task monitoring for asynchronous operations
- Sample scripts for common operations
- Basic error handling
- Logging support

### Resources Supported
- Active Directory (ad)
- Antivirus (antivirus)
- Backup (backup)
- Base Storage Volumes (base_storage_volumes)
- Cluster Control (cntl)
- Data Analytics (data_analytics)
- Data Copy to Object (data_copy_to_object)
- Data Portals (data_portals)
- Disk Drives (disk_drives)
- DNS Servers (dnss)
- Domain ID Maps (domain_idmaps)
- Events (events)
- File Snapshots (file_snapshots)
- Files (files)
- Gateways (gateways)
- Heartbeat (heartbeat)
- Internationalization (i18n)
- Identity Group Mappings (identity_group_mappings)
- Identity (identity)
- Identity Providers (idp)
- Key Management Services (kmses)
- Labels (labels)
- LDAP (ldaps)
- License Server (license_server)
- Licenses (licenses)
- Logical Volumes (logical_volumes)
- Login Policy (login_policy)
- Login (login)
- Mail SMTP (mailsmtp)
- Metrics (metrics)
- Modeler (modeler)
- Network Interfaces (network_interfaces)
- NIS (nis)
- Nodes (nodes)
- Notification Rules (notification_rules)
- NTP (ntps)
- Object Storage Volumes (object_storage_volumes)
- Object Store Logical Volumes (object_store_logical_volumes)
- Object Stores (object_stores)
- Objectives (objectives)
- Platform Node Control (pd_node_cntl)
- Platform Support (pd_support)
- Processor (processor)
- Reports (reports)
- Roles (roles)
- S3 Server (s3server)
- Schedules (schedules)
- Share Participants (share_participants)
- Share Replications (share_replications)
- Share Snapshots (share_snapshots)
- Shares (shares)
- Sites (sites)
- Snapshot Retentions (snapshot_retentions)
- SNMP (snmp)
- Static Routes (static_routes)
- Storage Volumes (storage_volumes)
- Subnet Gateways (subnet_gateways)
- Software Update (sw_update)
- Syslog (syslog)
- System Info (system_info)
- System (system)
- Tasks (tasks)
- User Groups (user_groups)
- Users (users)
- Versions (versions)
- Volume Groups (volume_groups)

## [Future Versions]

### Planned Features
- Asynchronous API client support
- Webhook support for real-time events
- Advanced caching strategies
- Performance monitoring and metrics
- Plugin system for custom functionality
- CLI tool for common operations
- Additional authentication methods
- Enhanced pagination support
- Bulk operations API
- Streaming file operations

---

## Versioning Scheme

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

For example, version 1.2.3:
- **1** = MAJOR version
- **2** = MINOR version  
- **3** = PATCH version

## Release Categories

### Breaking Changes
Changes that may break existing code and require migration

### New Features
Major new functionality that users will care about

### Enhancements
Improvements to existing features

### Bug Fixes
Resolutions to reported issues

### Security
Security-related changes and improvements

### Documentation
Changes to documentation

### Testing
Improvements to test coverage and quality

### Performance
Performance improvements and optimizations

### Developer Experience
Tools and improvements for developers

## Migration Guides

### From 0.1.0 to 1.0.0 (Planned)

**Exception Handling Changes:**

Old approach:
```python
try:
    result = client.shares.create(name="test", path="/test")
except Exception as e:
    print(f"Error: {e}")
```

New approach:
```python
from hammerspace.exceptions import ValidationError, AuthenticationError

try:
    result = client.shares.create(name="test", path="/test")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
    for error in e.validation_errors:
        print(f"  - {error}")
```

**Credential Management Changes:**

Old approach (INSECURE):
```python
client = HammerspaceApiClient(
    base_url="https://server:8443/mgmt/v1.2/rest",
    username="admin",
    password="your_password"  # Hardcoded - NOT SECURE
)
```

New approach (SECURE):
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

**Task Monitoring Changes:**

Old approach:
```python
result = client.shares.create(name="test", path="/test", monitor_task=True)
if result.get('state') == 'FAILED':
    print(f"Task failed: {result}")
```

New approach:
```python
from hammerspace.exceptions import TaskFailedError, TaskTimeoutError

try:
    result = client.shares.create(name="test", path="/test", monitor_task=True)
except TaskTimeoutError as e:
    print(f"Task timed out after {e.timeout_seconds} seconds")
except TaskFailedError as e:
    print(f"Task failed: {e}")
    print(f"Error details: {e.task_details}")
```

## How to Update

### Using pip
```bash
pip install --upgrade hammerspace-api-client
```

### Using conda
```bash
conda update hammerspace-api-client
```

### From source
```bash
git clone https://github.com/hammerspace/hammerspace-api-python-sdk
cd hammerspace-api-python-sdk
pip install -e .
```

## Support

For questions about specific changes or migration help:
- Check the [Migration Guides](#migration-guides)
- Review [API Reference](API_REFERENCE.md)
- Read [User Guide](USER_GUIDE.md)
- Open a [GitHub Issue](https://github.com/hammerspace/hammerspace-api-python-sdk/issues)

## Contributing

When contributing, please:
1. Add entries to the "Unreleased" section
2. Categorize changes appropriately
3. Include migration guides for breaking changes
4. Update this changelog as part of your pull request