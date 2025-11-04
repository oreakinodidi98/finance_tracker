# Security Verification Script
# Verifies that all security enhancements are properly configured

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        Finance Tracker - Security Verification Tool         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Check 1: Gunicorn in requirements.txt
Write-Host "[1/8] Checking Gunicorn in requirements.txt..." -ForegroundColor Yellow
if (Select-String -Path "backend/requirements.txt" -Pattern "gunicorn" -Quiet) {
    Write-Host "✓ Gunicorn found in requirements.txt" -ForegroundColor Green
} else {
    Write-Host "✗ Gunicorn NOT found in requirements.txt" -ForegroundColor Red
    $allPassed = $false
}

# Check 2: Dockerfile uses Gunicorn
Write-Host "[2/8] Checking Dockerfile uses Gunicorn..." -ForegroundColor Yellow
if (Select-String -Path "backend/Dockerfile" -Pattern "gunicorn" -Quiet) {
    Write-Host "✓ Backend Dockerfile uses Gunicorn" -ForegroundColor Green
} else {
    Write-Host "✗ Backend Dockerfile does NOT use Gunicorn" -ForegroundColor Red
    $allPassed = $false
}

# Check 3: Non-root user in backend
Write-Host "[3/8] Checking non-root user in backend..." -ForegroundColor Yellow
if (Select-String -Path "backend/Dockerfile" -Pattern "USER appuser" -Quiet) {
    Write-Host "✓ Backend runs as non-root user" -ForegroundColor Green
} else {
    Write-Host "✗ Backend does NOT run as non-root user" -ForegroundColor Red
    $allPassed = $false
}

# Check 4: Security headers in nginx.conf
Write-Host "[4/8] Checking security headers in nginx.conf..." -ForegroundColor Yellow
$headers = @(
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Permissions-Policy"
)

$missingHeaders = @()
foreach ($header in $headers) {
    if (-not (Select-String -Path "frontend/nginx.conf" -Pattern $header -Quiet)) {
        $missingHeaders += $header
    }
}

if ($missingHeaders.Count -eq 0) {
    Write-Host "✓ All security headers configured" -ForegroundColor Green
} else {
    Write-Host "✗ Missing headers: $($missingHeaders -join ', ')" -ForegroundColor Red
    $allPassed = $false
}

# Check 5: .dockerignore exists
Write-Host "[5/8] Checking .dockerignore files..." -ForegroundColor Yellow
$dockerignoreOk = $true
if (-not (Test-Path "backend/.dockerignore")) {
    Write-Host "  ✗ backend/.dockerignore NOT found" -ForegroundColor Red
    $dockerignoreOk = $false
}
if (-not (Test-Path "frontend/.dockerignore")) {
    Write-Host "  ✗ frontend/.dockerignore NOT found" -ForegroundColor Red
    $dockerignoreOk = $false
}
if ($dockerignoreOk) {
    Write-Host "✓ .dockerignore files exist" -ForegroundColor Green
} else {
    $allPassed = $false
}

# Check 6: .env not in git
Write-Host "[6/8] Checking .env is not tracked by git..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    if (Select-String -Path ".gitignore" -Pattern "\.env" -Quiet) {
        Write-Host "✓ .env file excluded from git" -ForegroundColor Green
    } else {
        Write-Host "✗ .env NOT in .gitignore!" -ForegroundColor Red
        $allPassed = $false
    }
} else {
    Write-Host "⚠ .gitignore not found" -ForegroundColor Yellow
}

# Check 7: Health checks in docker-compose
Write-Host "[7/8] Checking health checks in docker-compose.yml..." -ForegroundColor Yellow
if (Select-String -Path "docker-compose.yml" -Pattern "healthcheck" -Quiet) {
    Write-Host "✓ Health checks configured" -ForegroundColor Green
} else {
    Write-Host "✗ Health checks NOT configured" -ForegroundColor Red
    $allPassed = $false
}

# Check 8: Documentation exists
Write-Host "[8/8] Checking security documentation..." -ForegroundColor Yellow
$docs = @{
    "SECURITY.md" = "Main security documentation"
    "SECURITY-OPTIMIZATION.md" = "Optimization summary"
    "SECURITY-QUICKSTART.txt" = "Quick reference guide"
    "security-scan.ps1" = "Automated scanning script"
}

$missingDocs = @()
foreach ($doc in $docs.Keys) {
    if (-not (Test-Path $doc)) {
        $missingDocs += "$doc ($($docs[$doc]))"
    }
}

if ($missingDocs.Count -eq 0) {
    Write-Host "✓ All security documentation present" -ForegroundColor Green
} else {
    Write-Host "✗ Missing documentation:" -ForegroundColor Red
    foreach ($missing in $missingDocs) {
        Write-Host "  - $missing" -ForegroundColor Red
    }
    $allPassed = $false
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

if ($allPassed) {
    Write-Host "✓ ALL SECURITY CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Build images: docker-compose build --no-cache" -ForegroundColor White
    Write-Host "2. Run security scan: .\security-scan.ps1" -ForegroundColor White
    Write-Host "3. Review scan reports in security-reports/" -ForegroundColor White
    Write-Host "4. Address any CRITICAL or HIGH vulnerabilities" -ForegroundColor White
    Write-Host ""
    Write-Host "See SECURITY-QUICKSTART.txt for detailed instructions" -ForegroundColor Cyan
} else {
    Write-Host "✗ SOME CHECKS FAILED!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please review the failures above and:" -ForegroundColor Yellow
    Write-Host "1. Fix any missing configurations" -ForegroundColor White
    Write-Host "2. Re-run this verification script" -ForegroundColor White
    Write-Host "3. Check SECURITY.md for guidance" -ForegroundColor White
    exit 1
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
