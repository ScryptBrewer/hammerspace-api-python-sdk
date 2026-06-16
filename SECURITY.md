# Security Policy

## Supported Versions

| Version | Supported Until |
|---------|----------------|
| 1.x.x   | Current        |
| 0.1.x   | Until 1.0.0    |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Email**: Send an email to security@hammerspace.com
2. **Include Details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

3. **Response Time**:
   - Initial response: Within 48 hours
   - Detailed assessment: Within 7 days
   - Fix timeline: Based on severity

### What to Expect

- We will acknowledge receipt of your report
- We will provide regular updates on our progress
- We will credit you in the fix announcement (if desired)
- We will coordinate disclosure with you

## Security Best Practices for Users

### Credential Management

**DO:**
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

**DON'T:**
```python
# NEVER hardcode credentials
client = HammerspaceApiClient(
    base_url="https://server:8443/mgmt/v1.2/rest",
    username="admin",
    password="hardcoded_password"  # INSECURE!
)
```

### SSL/TLS Configuration

**For Development Only:**
```python
client = HammerspaceApiClient(
    ...,
    verify_ssl=False  # Only for testing!
)
```

**For Production:**
```python
client = HammerspaceApiClient(
    ...,
    verify_ssl=True  # Always in production!
)
```

### Environment Variables

Create a `.env` file (never commit this):
```env
HS_BASE_URL=https://your-server:8443/mgmt/v1.2/rest
HS_USERNAME=your_username
HS_PASSWORD=your_password
VERIFY_SSL=True
```

Add to `.gitignore`:
```gitignore
.env
.env.local
*.key
*.pem
credentials.json
```

### Error Handling

Handle authentication errors properly:
```python
from hammerspace.exceptions import AuthenticationError

try:
    result = client.shares.get()
except AuthenticationError as e:
    # Log without exposing credentials
    logger.error(f"Authentication failed: {e.status_code}")
    # Don't log passwords or tokens!
```

## Security Features in the SDK

### Built-in Protections

1. **Credential Protection**
   - Environment variable support
   - No credential logging
   - Secure credential storage

2. **Connection Security**
   - SSL/TLS verification enabled by default
   - Configurable SSL options
   - Warning suppression only when explicitly requested

3. **Error Handling**
   - No sensitive data in error messages
   - Generic error messages for authentication failures
   - Detailed logging only at debug level

4. **Session Management**
   - Automatic session cleanup
   - Secure cookie handling
   - Proper resource cleanup

## Dependency Security

### Vulnerability Scanning

We regularly scan dependencies for vulnerabilities:
- **Tools**: safety, bandit, pip-audit
- **Frequency**: Every PR and scheduled daily
- **Reporting**: Security advisories for critical issues

### Dependency Updates

- **Security patches**: Immediate update required
- **Bug fixes**: Update within 1 week
- **Features**: Update in next minor version

## Security Testing

### Automated Tests

- **Unit tests**: Security-focused test cases
- **Integration tests**: Authentication and authorization
- **Static analysis**: Security scanners in CI/CD

### Manual Review

- Code review for security best practices
- Penetration testing on major releases
- Third-party security audits

## Common Security Issues

### 1. Hardcoded Credentials

**Issue**: Passwords in source code
**Fix**: Use environment variables

### 2. Insecure SSL Configuration

**Issue**: `verify_ssl=False` in production
**Fix**: Always use `verify_ssl=True` in production

### 3. Logging Sensitive Data

**Issue**: Logging passwords or tokens
**Fix**: Use proper logging levels and message formatting

### 4. Insufficient Error Handling

**Issue**: Exposing system details in errors
**Fix**: Use custom exceptions and generic error messages

### 5. Dependency Vulnerabilities

**Issue**: Outdated or vulnerable dependencies
**Fix**: Regular dependency updates and scanning

## Security Audits

We welcome security audits and penetration testing.

### Coordinated Disclosure

If you plan to conduct security testing:
1. Contact us first at security@hammerspace.com
2. Provide details about your testing scope
3. Coordinate timing and disclosure
4. Follow responsible disclosure guidelines

## Security Metrics

- **Vulnerability Response Time**: < 48 hours
- **Security Patch Deployment**: < 7 days for critical issues
- **Dependency Scanning**: Continuous
- **Security Testing**: Every major release

## Additional Resources

- **OWASP Python Security**: https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html
- **Python Security Guidelines**: https://docs.python.org/3/library/security_warnings.html
- **CWE Top 25**: https://cwe.mitre.org/top25/

## Questions?

For security questions or concerns:
- Email: security@hammerspace.com
- GitHub Issues: Use `security` label
- Emergency: Contact through official support channels

Thank you for helping keep the Hammerspace API Python SDK secure!