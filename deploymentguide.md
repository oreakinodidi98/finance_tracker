# Finance Tracker - Deployment Guide with Security

## Overview

This guide walks you through deploying the Finance Tracker application with all security enhancements in place.

## Prerequisites

- Docker Desktop installed and running
- PowerShell (Windows) or Bash (Linux/macOS)
- 4GB RAM minimum
- 10GB disk space

## Pre-Deployment Security Checklist

Before deploying, ensure all security measures are in place:

### 1. Verify Security Configuration

Run the verification script:

```powershell
.\verify-security.ps1
```

Expected output: `✓ ALL SECURITY CHECKS PASSED!`

If any checks fail, review and fix them before proceeding.

### 2. Update Base Images

Rebuild images to get the latest security updates:

```powershell
# Pull latest base images
docker pull python:3.11-slim
docker pull node:20-alpine
docker pull nginx:1-alpine
docker pull postgres:15-alpine

# Rebuild application images
docker-compose build --no-cache
```

### 3. Run Security Scan

Execute comprehensive security scanning:

```powershell
.\security-scan.ps1
```

This will:
- Build all images with security optimizations
- Scan for vulnerabilities using Docker Scout
- Check for exposed secrets
- Audit all dependencies
- Generate detailed reports

Review the generated reports in `security-reports/`:

```powershell
# Quick check for critical issues
Get-Content security-reports\backend-scout.txt | Select-String "CRITICAL"
Get-Content security-reports\frontend-scout.txt | Select-String "CRITICAL"
```

### 4. Address Critical Vulnerabilities

If any CRITICAL vulnerabilities are found:

1. Review the CVE details in the scan reports
2. Update affected packages:
   ```powershell
   # For Python packages
   cd backend
   pip install --upgrade <package-name>
   pip freeze > requirements.txt
   
   # For npm packages
   cd ../frontend
   npm update <package-name>
   ```
3. Rebuild and re-scan
4. Repeat until no CRITICAL vulnerabilities remain

## Deployment Steps

### Development Environment

For local development and testing:

```powershell
# 1. Configure environment variables
Copy-Item .env.example .env

# 2. Edit .env file with your settings
notepad .env

# Update these values:
# - POSTGRES_PASSWORD (use a strong password)
# - AZURE_OPENAI_API_KEY (your Azure API key)
# - SECRET_KEY (generate a random string)

# 3. Build and start services
docker-compose build
docker-compose up -d

# 4. Verify services are running
docker-compose ps

# 5. Check logs
docker-compose logs -f

# 6. Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:5000
# Health check: http://localhost:5000/health
```

### Production Environment

For production deployment with enhanced security:

#### 1. Environment Configuration

Create a production `.env` file:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<STRONG_PASSWORD_16+_CHARS>
POSTGRES_DB=finance_tracker
DATABASE_URL=postgresql://postgres:<PASSWORD>@database:5432/finance_tracker

# Flask Configuration
SECRET_KEY=<RANDOM_SECRET_KEY_32+_CHARS>
FLASK_ENV=production

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=<YOUR_API_KEY>
AZURE_OPENAI_ENDPOINT=<YOUR_ENDPOINT>
AZURE_OPENAI_DEPLOYMENT_NAME=<YOUR_DEPLOYMENT>

# CORS Configuration (restrict to your domain)
CORS_ORIGINS=https://yourdomain.com
```

**Important**: Generate strong passwords and secrets:

```powershell
# Generate random password (PowerShell)
-join ((33..126) | Get-Random -Count 32 | % {[char]$_})

# Or use a password manager
```

#### 2. Configure HTTPS

In production, always use HTTPS. Options:

**Option A: Use a reverse proxy (Recommended)**

Create a `docker-compose.prod.yml` with Traefik or Nginx reverse proxy:

```yaml
version: '3.8'

services:
  reverse-proxy:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=your@email.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    labels:
      - "traefik.enable=true"

  frontend:
    build: ./frontend
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`yourdomain.com`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=myresolver"
    depends_on:
      - backend

  # ... rest of services
```

**Option B: Use cloud provider's load balancer**

Deploy to Azure Container Instances, AWS ECS, or Google Cloud Run with built-in HTTPS.

#### 3. Resource Limits

Add resource limits to `docker-compose.prod.yml`:

```yaml
services:
  backend:
    # ... existing configuration
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  frontend:
    # ... existing configuration
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M

  database:
    # ... existing configuration
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
```

#### 4. Database Backups

Configure automated backups:

```yaml
services:
  database:
    # ... existing configuration
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups

  backup:
    image: postgres:15-alpine
    environment:
      - PGHOST=database
      - PGUSER=postgres
      - PGPASSWORD=${POSTGRES_PASSWORD}
      - PGDATABASE=finance_tracker
    volumes:
      - ./backups:/backups
    entrypoint: |
      sh -c 'while true; do
        pg_dump -h database -U postgres finance_tracker > /backups/backup_$$(date +%Y%m%d_%H%M%S).sql
        find /backups -name "backup_*.sql" -mtime +7 -delete
        sleep 86400
      done'
    depends_on:
      - database
```

#### 5. Logging and Monitoring

Configure log aggregation:

```yaml
services:
  backend:
    # ... existing configuration
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Add log aggregation (optional)
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

#### 6. Deploy to Production

```powershell
# 1. Stop development environment
docker-compose down

# 2. Deploy production stack
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 3. Verify deployment
docker-compose ps
docker-compose logs -f

# 4. Test health endpoints
curl https://yourdomain.com/api/health
```

## Post-Deployment Security

### 1. Enable Docker Content Trust

Sign and verify images:

```powershell
# Enable content trust
$env:DOCKER_CONTENT_TRUST=1

# Tag and push images
docker tag finance_tracker-backend:latest yourregistry/finance_tracker-backend:1.0
docker push yourregistry/finance_tracker-backend:1.0
```

### 2. Configure Secrets Management

Use Azure Key Vault for production secrets:

```powershell
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login

# Create Key Vault
az keyvault create --name finance-tracker-kv --resource-group finance-tracker-rg

# Store secrets
az keyvault secret set --vault-name finance-tracker-kv --name db-password --value <password>
az keyvault secret set --vault-name finance-tracker-kv --name openai-api-key --value <api-key>

# Grant access to container identity
az keyvault set-policy --name finance-tracker-kv \
  --object-id <CONTAINER_IDENTITY> \
  --secret-permissions get list
```

### 3. Set Up Monitoring

Configure Azure Monitor or Prometheus:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
```

### 4. Regular Security Scans

Schedule automated scanning:

```powershell
# Create a scheduled task (Windows)
$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-File C:\finance_tracker\security-scan.ps1'
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Finance Tracker Security Scan"
```

Or use CI/CD (GitHub Actions example):

```yaml
name: Weekly Security Scan
on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build images
        run: docker-compose build
      
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'finance_tracker-backend:latest'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

## Troubleshooting

### Issue: Containers fail to start

**Solution**:
```powershell
# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database

# Verify environment variables
docker-compose config

# Rebuild images
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Database connection errors

**Solution**:
```powershell
# Check database is running
docker-compose ps database

# Verify DATABASE_URL in .env
cat .env | Select-String "DATABASE_URL"

# Connect to database manually
docker-compose exec database psql -U postgres -d finance_tracker

# Reset database
docker-compose down -v
docker-compose up -d
```

### Issue: High vulnerability count

**Solution**:
```powershell
# Update base images
docker pull python:3.11-slim
docker pull nginx:1-alpine
docker pull node:20-alpine

# Update dependencies
cd backend
pip list --outdated
pip install --upgrade <package>

cd ../frontend
npm audit
npm audit fix

# Rebuild
docker-compose build --no-cache
```

## Maintenance Schedule

### Daily
- Review application logs
- Check for service availability

### Weekly
- Run security scans
- Review vulnerability reports
- Update dependencies if needed

### Monthly
- Full security audit
- Disaster recovery test
- Backup verification
- Update base images

### Quarterly
- Security penetration testing
- Review and update security policies
- Infrastructure review
- Performance optimization

## Security Incident Response

If a security incident occurs:

1. **Immediate Actions**
   - Take affected services offline
   - Preserve logs and evidence
   - Notify stakeholders

2. **Investigation**
   - Review logs for unauthorized access
   - Check for data exfiltration
   - Identify root cause

3. **Remediation**
   - Apply security patches
   - Change all credentials
   - Update security measures

4. **Recovery**
   - Restore from clean backups
   - Redeploy services
   - Verify integrity

5. **Post-Incident**
   - Document incident details
   - Update security procedures
   - Conduct team retrospective

## Support

For deployment assistance:
- Email: oreakinodidi@microsoft.com
- Documentation: See SECURITY.md for detailed security information

---

**Remember**: Security is an ongoing process. Regular updates, monitoring, and vigilance are essential for maintaining a secure application.
