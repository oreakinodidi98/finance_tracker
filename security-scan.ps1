# Security Scanning Script for Finance Tracker
# Run this script to perform comprehensive security scans

Write-Host "=== Finance Tracker Security Scanner ===" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Build images
Write-Host ""
Write-Host "Building Docker images..." -ForegroundColor Yellow
docker-compose build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Images built successfully" -ForegroundColor Green

# Create reports directory
$reportsDir = "security-reports"
if (!(Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Path $reportsDir | Out-Null
}

Write-Host ""
Write-Host "=== Scanning Backend Image ===" -ForegroundColor Cyan

# Docker Scout scan for backend
Write-Host "Running Docker Scout scan on backend..." -ForegroundColor Yellow
docker scout cves finance_tracker-backend:latest > "$reportsDir/backend-scout.txt" 2>&1

if (Test-Path "$reportsDir/backend-scout.txt") {
    Write-Host "✓ Backend Docker Scout scan completed" -ForegroundColor Green
    
    # Check for critical vulnerabilities
    $backendContent = Get-Content "$reportsDir/backend-scout.txt" -Raw
    if ($backendContent -match "CRITICAL") {
        Write-Host "⚠ CRITICAL vulnerabilities found in backend!" -ForegroundColor Red
    } elseif ($backendContent -match "HIGH") {
        Write-Host "⚠ HIGH vulnerabilities found in backend" -ForegroundColor Yellow
    } else {
        Write-Host "✓ No critical vulnerabilities in backend" -ForegroundColor Green
    }
}

# Get recommendations
Write-Host "Getting Docker Scout recommendations for backend..." -ForegroundColor Yellow
docker scout recommendations finance_tracker-backend:latest > "$reportsDir/backend-recommendations.txt" 2>&1

Write-Host ""
Write-Host "=== Scanning Frontend Image ===" -ForegroundColor Cyan

# Docker Scout scan for frontend
Write-Host "Running Docker Scout scan on frontend..." -ForegroundColor Yellow
docker scout cves finance_tracker-frontend:latest > "$reportsDir/frontend-scout.txt" 2>&1

if (Test-Path "$reportsDir/frontend-scout.txt") {
    Write-Host "✓ Frontend Docker Scout scan completed" -ForegroundColor Green
    
    # Check for critical vulnerabilities
    $frontendContent = Get-Content "$reportsDir/frontend-scout.txt" -Raw
    if ($frontendContent -match "CRITICAL") {
        Write-Host "⚠ CRITICAL vulnerabilities found in frontend!" -ForegroundColor Red
    } elseif ($frontendContent -match "HIGH") {
        Write-Host "⚠ HIGH vulnerabilities found in frontend" -ForegroundColor Yellow
    } else {
        Write-Host "✓ No critical vulnerabilities in frontend" -ForegroundColor Green
    }
}

# Get recommendations
Write-Host "Getting Docker Scout recommendations for frontend..." -ForegroundColor Yellow
docker scout recommendations finance_tracker-frontend:latest > "$reportsDir/frontend-recommendations.txt" 2>&1

Write-Host ""
Write-Host "=== Scanning Database Image ===" -ForegroundColor Cyan

# Docker Scout scan for database
Write-Host "Running Docker Scout scan on PostgreSQL..." -ForegroundColor Yellow
docker scout cves postgres:15-alpine > "$reportsDir/database-scout.txt" 2>&1

if (Test-Path "$reportsDir/database-scout.txt") {
    Write-Host "✓ Database Docker Scout scan completed" -ForegroundColor Green
}

# Check if Trivy is installed
Write-Host ""
Write-Host "=== Trivy Scans ===" -ForegroundColor Cyan
$trivyInstalled = Get-Command trivy -ErrorAction SilentlyContinue

if ($trivyInstalled) {
    Write-Host "✓ Trivy is installed" -ForegroundColor Green
    
    Write-Host "Running Trivy scan on backend (HIGH and CRITICAL only)..." -ForegroundColor Yellow
    trivy image --severity HIGH,CRITICAL finance_tracker-backend:latest > "$reportsDir/backend-trivy.txt" 2>&1
    
    Write-Host "Running Trivy scan on frontend (HIGH and CRITICAL only)..." -ForegroundColor Yellow
    trivy image --severity HIGH,CRITICAL finance_tracker-frontend:latest > "$reportsDir/frontend-trivy.txt" 2>&1
    
    Write-Host "✓ Trivy scans completed" -ForegroundColor Green
} else {
    Write-Host "⚠ Trivy not installed. Install with: choco install trivy" -ForegroundColor Yellow
}

# Scan for secrets in codebase
Write-Host ""
Write-Host "=== Secret Scanning ===" -ForegroundColor Cyan
if ($trivyInstalled) {
    Write-Host "Scanning for exposed secrets..." -ForegroundColor Yellow
    trivy fs --scanners secret . > "$reportsDir/secrets-scan.txt" 2>&1
    
    $secretsContent = Get-Content "$reportsDir/secrets-scan.txt" -Raw
    if ($secretsContent -match "Total: 0") {
        Write-Host "✓ No secrets found" -ForegroundColor Green
    } else {
        Write-Host "⚠ Potential secrets detected! Review secrets-scan.txt" -ForegroundColor Red
    }
}

# Scan Python dependencies
Write-Host ""
Write-Host "=== Dependency Scanning ===" -ForegroundColor Cyan

# Check if pip-audit is available
$pipAudit = Get-Command pip-audit -ErrorAction SilentlyContinue

if ($pipAudit) {
    Write-Host "Running pip-audit on Python dependencies..." -ForegroundColor Yellow
    Push-Location backend
    pip-audit -r requirements.txt > "../$reportsDir/python-dependencies.txt" 2>&1
    Pop-Location
    Write-Host "✓ Python dependency scan completed" -ForegroundColor Green
} else {
    Write-Host "⚠ pip-audit not installed. Install with: pip install pip-audit" -ForegroundColor Yellow
}

# Scan npm dependencies
Write-Host "Checking npm dependencies..." -ForegroundColor Yellow
Push-Location frontend
npm audit --json > "../$reportsDir/npm-audit.json" 2>&1
npm audit > "../$reportsDir/npm-audit.txt" 2>&1
Pop-Location
Write-Host "✓ npm audit completed" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "=== Scan Summary ===" -ForegroundColor Cyan
Write-Host "All scan reports saved to: $reportsDir/" -ForegroundColor Green
Write-Host ""
Write-Host "Files generated:" -ForegroundColor Yellow
Get-ChildItem $reportsDir | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Review all scan reports in the $reportsDir/ folder" -ForegroundColor White
Write-Host "2. Address CRITICAL and HIGH vulnerabilities first" -ForegroundColor White
Write-Host "3. Update dependencies with known vulnerabilities" -ForegroundColor White
Write-Host "4. Re-run this script after fixes to verify" -ForegroundColor White
Write-Host "5. See SECURITY.md for detailed remediation guidance" -ForegroundColor White

Write-Host ""
Write-Host "=== Quick View Commands ===" -ForegroundColor Cyan
Write-Host "View backend vulnerabilities:" -ForegroundColor Yellow
Write-Host "  cat $reportsDir/backend-scout.txt | Select-String 'CRITICAL|HIGH'" -ForegroundColor White
Write-Host ""
Write-Host "View frontend vulnerabilities:" -ForegroundColor Yellow
Write-Host "  cat $reportsDir/frontend-scout.txt | Select-String 'CRITICAL|HIGH'" -ForegroundColor White
Write-Host ""
Write-Host "View recommendations:" -ForegroundColor Yellow
Write-Host "  cat $reportsDir/backend-recommendations.txt" -ForegroundColor White
Write-Host ""

# Open summary in notepad
Write-Host "Opening backend scan summary..." -ForegroundColor Yellow
Start-Process notepad "$reportsDir/backend-scout.txt"

Write-Host ""
Write-Host "✓ Security scan completed!" -ForegroundColor Green
