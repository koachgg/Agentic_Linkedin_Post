@echo off
echo 🚀 LinkedIn Post Generator - GitHub Deployment
echo.
echo This script will help you push to GitHub
echo.

REM Check if git is configured
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Configuring git user...
    set /p username="Enter your GitHub username: "
    set /p email="Enter your email: "
    git config --global user.name "%username%"
    git config --global user.email "%email%"
)

echo.
echo Current git status:
git status

echo.
echo Adding all files...
git add .

echo.
echo Committing changes...
git commit -m "feat: Complete LinkedIn Post Generator with Nugget.com-inspired UI and streaming API"

echo.
echo Repository is ready for GitHub!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub.com
echo 2. Copy the repository URL
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/linkedin-post-generator.git
echo    git branch -M main
echo    git push -u origin main
echo.
pause
