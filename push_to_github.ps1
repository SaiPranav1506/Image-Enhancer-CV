#!/usr/bin/env pwsh
# Image Enhancer - GitHub Push Helper (PowerShell Version)
# Usage: ./push_to_github.ps1

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Image Enhancer - GitHub Push Helper" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize git if not already done
if (!(Test-Path .git)) {
    Write-Host "Initializing git repository..." -ForegroundColor Green
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
} else {
    Write-Host "Git repository already initialized" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "Adding all files to git..." -ForegroundColor Green
git add .

# Commit
Write-Host "Committing files..." -ForegroundColor Green
git commit -m "Initial Commit"

# Show instructions
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://github.com/new" -ForegroundColor Yellow
Write-Host "2. Create a new repository called 'image-enhancer'" -ForegroundColor Yellow
Write-Host "3. Copy the repository URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Run this command:" -ForegroundColor Yellow
Write-Host "   git remote add origin [PASTE_YOUR_URL_HERE]" -ForegroundColor White
Write-Host ""
Write-Host "5. Then run:" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ask for GitHub URL
$GITHUB_URL = Read-Host "Enter your GitHub repository URL (or press Enter to skip)"

if ($GITHUB_URL) {
    Write-Host ""
    Write-Host "Adding remote origin..." -ForegroundColor Green
    git remote add origin $GITHUB_URL
    
    Write-Host "Pushing to GitHub..." -ForegroundColor Green
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS! Your project is now on GitHub!" -ForegroundColor Green
        Write-Host "Access it at: $GITHUB_URL" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "ERROR: Push failed. Check your URL and permissions." -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "Skipped GitHub push." -ForegroundColor Yellow
    Write-Host "You can do it manually whenever ready." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"
