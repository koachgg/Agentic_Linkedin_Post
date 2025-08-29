@echo off
echo 🚀 Setting up Git repository for LinkedIn Post Generator
echo.

REM Navigate to project directory
cd /d "c:\Users\abhig\Documents\Belo\Nugget\linkedin-post-generator"

REM Initialize git repository
echo 📁 Initializing git repository...
git init

REM Add all files (respecting .gitignore)
echo 📝 Adding files to git...
git add .

REM Show status
echo 📊 Git status:
git status

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "Initial commit: LinkedIn Post Generator with agentic AI workflow"

echo.
echo ✅ Git repository initialized successfully!
echo.
echo 🔗 Next steps to push to GitHub:
echo 1. Go to https://github.com/new and create a new repository named 'linkedin-post-generator'
echo 2. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/linkedin-post-generator.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 📖 For detailed instructions, see GITHUB_SETUP.md
echo.
pause
