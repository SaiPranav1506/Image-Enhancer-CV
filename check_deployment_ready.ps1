#!/usr/bin/env pwsh
# Deployment Readiness Checker
# Verifies all files are ready for Render deployment

Write-Host ""
Write-Host "═════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📋 Deployment Readiness Checker" -ForegroundColor Cyan
Write-Host "═════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check essential files
$essentialFiles = @(
    "requirements.txt",
    "config.py",
    ".gitignore",
    "src/interfaces/streamlit_app.py",
    "src/interfaces/flask_app.py",
    ".streamlit/config.toml",
    "runtime.txt",
    ".env.example"
)

Write-Host "✓ Checking essential files..." -ForegroundColor Yellow
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ MISSING: $file" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
Write-Host "✓ Checking deployment guides..." -ForegroundColor Yellow
$guides = @("DEPLOYMENT.md", "DEPLOYMENT_CHECKLIST.md")
foreach ($guide in $guides) {
    if (Test-Path $guide) {
        Write-Host "  ✅ $guide" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Optional: $guide" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✓ Checking helper scripts..." -ForegroundColor Yellow
$scripts = @("push_to_github.ps1", "push_to_github.bat")
foreach ($script in $scripts) {
    if (Test-Path $script) {
        Write-Host "  ✅ $script" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Optional: $script" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✓ Checking dependencies in requirements.txt..." -ForegroundColor Yellow
$requiredPackages = @(
    "streamlit",
    "flask",
    "opencv-python",
    "gunicorn",
    "python-dotenv",
    "plotly"
)
$reqContent = Get-Content "requirements.txt" -Raw
foreach ($pkg in $requiredPackages) {
    if ($reqContent -match $pkg) {
        Write-Host "  ✅ $pkg" -ForegroundColor Green
    } else {
        Write-Host "  ❌ MISSING: $pkg in requirements.txt" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
Write-Host "✓ Checking .gitignore configuration..." -ForegroundColor Yellow
$gitignoreItems = @("__pycache__", "*.pyc", ".env", "venv", ".vscode")
$gitignoreContent = Get-Content ".gitignore" -Raw
foreach ($item in $gitignoreItems) {
    if ($gitignoreContent -match $item) {
        Write-Host "  ✅ $item ignored" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $item not in .gitignore" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✓ Checking directories..." -ForegroundColor Yellow
$directories = @("src/modules", "src/interfaces", "data", "output", "temp_images")
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        Write-Host "  ✅ $dir/" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Missing (will be created): $dir/" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "═════════════════════════════════════════════" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✅ All checks passed! Ready for deployment!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Run: .\push_to_github.ps1" -ForegroundColor White
    Write-Host "  2. Go to https://render.com" -ForegroundColor White
    Write-Host "  3. Connect your GitHub repository" -ForegroundColor White
    Write-Host "  4. Deploy!" -ForegroundColor White
} else {
    Write-Host "⚠️  Some issues found. Please address them above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Check DEPLOYMENT.md for more information." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "═════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
