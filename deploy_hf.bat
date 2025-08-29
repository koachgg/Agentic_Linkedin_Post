@echo off
echo ========================================
echo HUGGING FACE SPACES DEPLOYMENT PREP
echo ========================================
echo.

echo Running deployment readiness check...
python deploy_huggingface.py

echo.
echo ========================================
echo.
echo Next: Read HUGGINGFACE_DEPLOYMENT.md for complete instructions
echo.
pause
