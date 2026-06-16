# Contributing to Hammerspace API Python SDK

Thank you for your interest in contributing to the Hammerspace API Python SDK! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We want to maintain a welcoming and inclusive community for all contributors.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/hammerspace-api-python-sdk.git
   cd hammerspace-api-python-sdk
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Development Workflow

### 1. Create a Branch

Create a new branch for your contribution:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Follow the existing code style
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests and Linters

Before committing, run the following checks:
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=hammerspace

# Run linters
black --check hammerspace/
isort --check-only hammerspace/
flake8 hammerspace/
mypy hammerspace/

# Run pre-commit hooks
pre-commit run --all-files
```

### 4. Commit Your Changes

Use descriptive commit messages:
```bash
git add .
git commit -m "Add rate limiting feature to API client"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots for UI changes (if applicable)

## Coding Standards

### Code Style

We use **Black** for code formatting with the following settings:
- Line length: 100 characters
- Target Python version: 3.8+

### Type Hints

All functions and methods should have type hints:
```python
def create_share(
    self,
    name: str,
    path: str,
    comment: Optional[str] = None,
    export_options: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
```

### Documentation

All public functions and classes should have docstrings:
```python
def get_shares(
    self,
    identifier: Optional[str] = None,
    simple: bool = False
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Retrieves share information from the Hammerspace system.
    
    Args:
        identifier: Share UUID or name to fetch specific share
        simple: If True, returns only uuid, name, and path fields
        
    Returns:
        Share information or list of shares
        
    Raises:
        AuthenticationError: If authentication fails
        ResourceNotFoundError: If share not found
        
    Example:
        >>> shares = client.shares.get(simple=True)
        >>> for share in shares:
        ...     print(share['name'])
    """
```

### Error Handling

Use specific exception types:
```python
try:
    result = self.api_client.make_rest_call(path)
except AuthenticationError as e:
    logger.error(f"Authentication failed: {e}")
    raise
except ConnectionError as e:
    logger.warning(f"Connection error, retrying: {e}")
    # Implement retry logic
```

### Security

- Never commit credentials or sensitive data
- Use environment variables for configuration
- Follow security best practices
- Run security scanners before committing

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── test_client.py
│   ├── test_shares.py
│   └── test_exceptions.py
└── integration/
    ├── test_api_integration.py
    └── test_task_monitoring.py
```

### Writing Tests

```python
import pytest
from hammerspace import HammerspaceApiClient
from hammerspace.exceptions import AuthenticationError

class TestSharesClient:
    """Test cases for SharesClient."""
    
    def test_get_shares_simple(self, client):
        """Test getting shares in simple format."""
        shares = client.shares.get(simple=True)
        assert isinstance(shares, list)
        for share in shares:
            assert 'uuid' in share
            assert 'name' in share
            assert 'path' in share
    
    def test_create_share_validation(self, client):
        """Test share creation validation."""
        with pytest.raises(ValidationError):
            client.shares.create(name="", path="/test")
    
    def test_get_nonexistent_share(self, client):
        """Test getting a non-existent share."""
        with pytest.raises(ResourceNotFoundError):
            client.shares.get(identifier="nonexistent-share")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run with coverage
pytest --cov=hammerspace --cov-report=html

# Run specific test
pytest tests/test_shares.py::TestSharesClient::test_get_shares_simple

# Run with verbose output
pytest -v
```

## Documentation

### Updating Documentation

1. **API Changes**: Update `API_REFERENCE.md` with new methods/parameters
2. **New Features**: Add examples to `USER_GUIDE.md`
3. **Breaking Changes**: Update `CHANGELOG.md` with migration guide
4. **Bug Fixes**: Update `CHANGELOG.md` with fix details

### Documentation Format

Use clear, consistent formatting:
```markdown
### Method Name

Brief description of what the method does.

```python
method_name(
    param1: type,
    param2: Optional[type] = default_value
) -> return_type
```

**Parameters:**
- `param1` (type): Description
- `param2` (Optional[type]): Description

**Returns:** Description of return value

**Raises:** List of exceptions that can be raised

**Example:**
```python
result = client.method_name(param1="value")
```
```

## Pull Request Guidelines

### PR Title Format

Use conventional commit format:
- `feat: Add rate limiting to API client`
- `fix: Handle connection timeout errors`
- `docs: Update API reference documentation`
- `test: Add unit tests for share creation`
- `refactor: Simplify error handling logic`

### PR Description Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Tests

## Related Issues
Fixes #123
Related to #456

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Commented complex code sections
- [ ] Updated documentation
- [ ] No new warnings generated
- [ ] Added tests for new functionality
- [ ] All tests passing
- [ ] Updated CHANGELOG.md
```

## Release Process

### Version Bumping

1. Update version in `hammerspace/__init__.py`
2. Update `CHANGELOG.md` with release notes
3. Create release commit
4. Create Git tag

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number updated
- [ ] Security scans passed
- [ ] Integration tests passed
- [ ] Release notes prepared

## Questions and Support

If you have questions:
- Check existing issues and discussions
- Read the documentation
- Start a new discussion for questions
- Create an issue for bugs or feature requests

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the Hammerspace API Python SDK!