@echo off
REM This script helps you push your project to GitHub
REM Usage: Run this file from the image-enhancer directory

echo.
echo ============================================
echo  Image Enhancer - GitHub Push Helper
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize git if not already done
if not exist .git (
    echo Initializing git repository...
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
) else (
    echo Git repository already initialized
)

REM Add all files
echo.
echo Adding all files to git...
git add .

REM Commit
echo Committing files...
git commit -m "Initial Commit"

REM Show instructions for GitHub
echo.
echo ============================================
echo  Next Steps:
echo ============================================
echo.
echo 1. Go to https://github.com/new
echo 2. Create a new repository called "image-enhancer"
echo 3. Copy the repository URL
echo.
echo 4. Run this command:
echo    git remote add origin [PASTE_YOUR_URL_HERE]
echo.
echo 5. Then run:
echo    git push -u origin main
echo.
echo OR run this complete command:
echo    git remote add origin https://github.com/YOUR_USERNAME/image-enhancer.git ^&^& git push -u origin main
echo.
echo ============================================
echo.

REM Ask if user wants to proceed
set /p GITHUB_URL="Enter your GitHub repository URL (or press Enter to skip): "

if not "%GITHUB_URL%"=="" (
    echo.
    echo Adding remote origin...
    git remote add origin %GITHUB_URL%
    
    echo Pushing to GitHub...
    git push -u origin main
    
    if %errorlevel% equ 0 (
        echo.
        echo SUCCESS! Your project is now on GitHub!
        echo Access it at: %GITHUB_URL%
    ) else (
        echo.
        echo ERROR: Push failed. Check your URL and permissions.
    )
) else (
    echo.
    echo Skipped GitHub push.
    echo You can do it manually whenever ready.
)

echo.
pause
