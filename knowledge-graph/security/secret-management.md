# Security Best Practice: Secret Management

## Overview

Proper secret management is critical to maintaining the security of applications and infrastructure. Secrets include API keys, database passwords, encryption keys, OAuth tokens, and any other sensitive credentials that must be protected from unauthorized access.

## The Golden Rules

### Rule 1: Never Commit Secrets to Version Control

Secrets should never be stored in Git repositories, even private ones. Once a secret is committed, it exists in the Git history forever unless you rewrite history (which is risky and disruptive).

**What to do instead:**
- Use environment variables for secrets.
- Use secret management services (AWS Secrets Manager, HashiCorp Vault, etc.).
- Use `.env` files locally (and add `.env` to `.gitignore`).

### Rule 2: Use Pydantic's SecretStr and SecretBytes

In the Sovereign Forge ecosystem, all secrets must be wrapped in Pydantic's `SecretStr` or `SecretBytes` types. This ensures that secrets are not accidentally logged or printed.

**Example:**

```python
from pydantic import BaseModel, SecretStr

class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr  # This will be masked in logs

config = DatabaseConfig(
    host="localhost",
    port=5432,
    username="admin",
    password="super_secret_password"
)

print(config)
# Output: host='localhost' port=5432 username='admin' password=SecretStr('**********')
```

### Rule 3: Rotate Secrets Regularly

Secrets should be rotated on a regular schedule (e.g., every 90 days) to limit the window of opportunity for attackers if a secret is compromised.

**Rotation Strategy:**
- Automate secret rotation using secret management services.
- Implement a grace period where both old and new secrets are valid during rotation.
- Log all secret rotation events for audit purposes.

### Rule 4: Limit Secret Scope and Access

Follow the principle of least privilege:
- Grant access to secrets only to the services and users that need them.
- Use separate secrets for different environments (dev, staging, production).
- Implement role-based access control (RBAC) for secret management systems.

### Rule 5: Encrypt Secrets at Rest and in Transit

- **At Rest:** Secrets stored in databases or files should be encrypted using strong encryption algorithms (AES-256).
- **In Transit:** Secrets transmitted over networks should use TLS 1.3 or higher.

## Common Vulnerabilities

### Hardcoded Secrets

**Bad:**
```python
API_KEY = "sk-1234567890abcdef"  # Never do this!
```

**Good:**
```python
import os
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### Secrets in Logs

**Bad:**
```python
logger.info(f"Connecting to database with password: {password}")
```

**Good:**
```python
logger.info("Connecting to database")
# Password is never logged
```

### Secrets in Error Messages

**Bad:**
```python
raise Exception(f"Failed to connect with password: {password}")
```

**Good:**
```python
raise Exception("Failed to connect to database")
# Log the error internally without exposing the secret
```

## Secret Management Tools

### For Local Development
- **python-dotenv:** Load secrets from `.env` files.
- **direnv:** Automatically load environment variables based on directory.

### For Production
- **AWS Secrets Manager:** Managed secret storage and rotation for AWS.
- **HashiCorp Vault:** Open-source secret management with advanced features.
- **Google Secret Manager:** Managed secret storage for Google Cloud.
- **Azure Key Vault:** Managed secret storage for Microsoft Azure.

## Sovereign Forge Implementation

In the Sovereign Forge ecosystem:

1. All secrets are defined using `SecretStr` or `SecretBytes` in Pydantic models.
2. The **Security Sentinel** Guru Agent is responsible for auditing secret usage.
3. The **Vulnerability Scanner** Sub-Agent scans for hardcoded secrets in code.
4. Secrets are loaded from environment variables or secret management services, never from code.

## Checklist

Before deploying any code, verify:

- [ ] No secrets are hardcoded in the codebase.
- [ ] All secrets use `SecretStr` or `SecretBytes`.
- [ ] `.env` files are in `.gitignore`.
- [ ] Environment variables are set in the deployment environment.
- [ ] Secrets are encrypted at rest and in transit.
- [ ] Access to secrets is limited by RBAC.
- [ ] Secret rotation is automated or scheduled.

---

*If it's sensitive, we don't show it. Real recognize real.*
