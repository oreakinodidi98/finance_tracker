# Security Guide for Finance Tracker

## Overview
This document outlines the security measures implemented in the Finance Tracker application and provides instructions for vulnerability scanning and security best practices.

## Security Features Implemented

### Backend Security (Flask/Python)

1. **Production WSGI Server**
   - Using Gunicorn instead of Flask development server
   - 4 worker processes for better performance
   - Timeout configuration for request handling

2. **Non-Root User**
   - Application runs as `appuser` (non-root)
   - Minimizes damage potential from container breakouts

3. **Dependency Management**
   - Pinned versions in requirements.txt
   - No cache during pip install
   - Minimal system dependencies

4. **Environment Variables**
   - Sensitive data (passwords, API keys) in .env file
   - Never commit .env to version control

5. **Python Optimization**
   - `PYTHONDONTWRITEBYTECODE=1` - No .pyc files
   - `PYTHONUNBUFFERED=1` - Real-time logging

### Frontend Security (React/Nginx)

1. **Multi-Stage Build**
   - Build stage discarded after compilation
   - Only production artifacts in final image
   - Reduced attack surface

2. **Security Headers**
   - X-Frame-Options: Prevents clickjacking
   - X-XSS-Protection: Cross-site scripting protection
   - X-Content-Type-Options: MIME type sniffing protection
   - Content-Security-Policy: Controls resource loading
   - Strict-Transport-Security: Forces HTTPS
   - Permissions-Policy: Restricts browser features

3. **Static Asset Optimization**
   - Long-term caching for immutable assets
   - Gzip compression enabled

### Database Security (PostgreSQL)

1. **Network Isolation**
   - Database not exposed to host network
   - Only accessible from backend container

2. **Credentials Management**
   - Strong passwords in environment variables
   - No hardcoded credentials

## Vulnerability Scanning

### Option 1: Docker Scout (Recommended)

Docker Scout is built into Docker Desktop and provides comprehensive vulnerability analysis.

#### Enable Docker Scout
```powershell
# Login to Docker (if not already)
docker login

# Docker Scout is enabled by default in Docker Desktop
```

#### Scan Images
```powershell
# Scan backend image
docker scout cves finance_tracker-backend:latest

# Scan frontend image
docker scout cves finance_tracker-frontend:latest

# Scan database image
docker scout cves postgres:15-alpine

# Get recommendations
docker scout recommendations finance_tracker-backend:latest
```

#### View Detailed Report
```powershell
# Generate detailed CVE report with SBOM (Software Bill of Materials)
docker scout cves --format sarif --output backend-report.json finance_tracker-backend:latest

# View in human-readable format
docker scout cves --format markdown --output backend-report.md finance_tracker-backend:latest
```

### Option 2: Trivy (Open Source Alternative)

Trivy is a comprehensive vulnerability scanner for containers.

#### Install Trivy (Windows)
```powershell
# Using Chocolatey
choco install trivy

# Or download from GitHub releases
# https://github.com/aquasecurity/trivy/releases
```

#### Scan with Trivy
```powershell
# Scan backend image
trivy image finance_tracker-backend:latest

# Scan with severity filtering (only HIGH and CRITICAL)
trivy image --severity HIGH,CRITICAL finance_tracker-backend:latest

# Generate JSON report
trivy image --format json --output backend-trivy.json finance_tracker-backend:latest

# Scan for misconfigurations
trivy config ./backend/Dockerfile

# Scan for secrets
trivy fs --scanners secret ./
```

### Option 3: Snyk (Commercial with Free Tier)

#### Install Snyk CLI
```powershell
npm install -g snyk

# Authenticate
snyk auth
```

#### Scan with Snyk
```powershell
# Scan Docker images
snyk container test finance_tracker-backend:latest

# Scan dependencies
cd backend
snyk test --file=requirements.txt

cd ../frontend
snyk test
```

## Security Scanning Workflow

### 1. Pre-Deployment Scan
Before deploying to production, run a complete security scan:

```powershell
# Build images
docker-compose build

# Scan all images
docker scout cves finance_tracker-backend:latest > backend-scan.txt
docker scout cves finance_tracker-frontend:latest > frontend-scan.txt
trivy image --severity HIGH,CRITICAL finance_tracker-backend:latest
trivy image --severity HIGH,CRITICAL finance_tracker-frontend:latest

# Review results
cat backend-scan.txt
cat frontend-scan.txt
```

### 2. Regular Monitoring
Set up automated scanning in your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Security Scan
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build images
        run: docker-compose build
      
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'finance_tracker-backend:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

## Common Vulnerabilities and Remediation

### 1. Outdated Base Images
**Problem**: Using old Python/Node/Nginx versions with known CVEs

**Solution**:
```dockerfile
# Update base images regularly
FROM python:3.11-slim  # Check for 3.12 or newer
FROM node:20-alpine    # Check for newer LTS versions
FROM nginx:alpine      # Alpine is regularly updated
```

### 2. Vulnerable Python Packages
**Problem**: Dependencies with security issues

**Solution**:
```powershell
# Update packages
pip list --outdated
pip install --upgrade <package-name>

# Check for security advisories
pip-audit

# Or use safety
pip install safety
safety check -r requirements.txt
```

### 3. Vulnerable npm Packages
**Problem**: Frontend dependencies with CVEs

**Solution**:
```powershell
cd frontend

# Audit dependencies
npm audit

# Auto-fix where possible
npm audit fix

# For breaking changes
npm audit fix --force

# Update specific package
npm update <package-name>
```

### 4. Exposed Secrets
**Problem**: API keys or passwords in code

**Solution**:
- Use environment variables exclusively
- Add .env to .gitignore
- Use Azure Key Vault for production
- Rotate credentials regularly

## Security Best Practices

### 1. Docker Image Optimization
```dockerfile
# Use specific versions, not 'latest'
FROM python:3.11.9-slim

# Minimize layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    package1 package2 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Use .dockerignore
# Add: .git, .env, __pycache__, *.pyc, node_modules
```

### 2. Network Security
```yaml
# docker-compose.yml - Use internal networks
networks:
  backend:
    internal: true  # No external access
  frontend:
    # Frontend can access internet
```

### 3. Secrets Management
```powershell
# Use Docker secrets (Docker Swarm) or Azure Key Vault
# Never use environment variables for production secrets
```

### 4. Health Checks
```dockerfile
# Backend health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Frontend health check  
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost/ || exit 1
```

### 5. Resource Limits
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Security Checklist

Before production deployment:

- [ ] All images scanned with Docker Scout or Trivy
- [ ] No HIGH or CRITICAL vulnerabilities
- [ ] .env file not in version control
- [ ] Strong passwords (16+ characters)
- [ ] HTTPS enabled (use reverse proxy like Traefik/Nginx)
- [ ] Database backups configured
- [ ] Logging and monitoring enabled
- [ ] Rate limiting implemented
- [ ] CORS configured properly
- [ ] Security headers verified
- [ ] Non-root users in all containers
- [ ] Resource limits configured
- [ ] Health checks working
- [ ] Secrets in Azure Key Vault (production)

## Incident Response

If a vulnerability is found:

1. **Assess Severity**
   - Review CVSS score and exploit availability
   - Determine if systems are affected

2. **Immediate Actions**
   - Take affected services offline if critical
   - Review logs for exploitation attempts

3. **Remediation**
   - Update vulnerable packages
   - Rebuild Docker images
   - Redeploy services

4. **Verification**
   - Re-scan images
   - Test functionality
   - Monitor for issues

5. **Documentation**
   - Record incident details
   - Update security procedures
   - Share lessons learned

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Contact

For security concerns, contact: oreakinodidi@microsoft.com
