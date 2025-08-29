@echo off
echo Starting LinkedIn Post Generator...
echo.

cd /d "c:\Users\abhig\Documents\Belo\Nugget\linkedin-post-generator"

echo Installing dependencies...
C:/Users/abhig/Documents/Belo/Nugget/.venv/Scripts/python.exe -m pip install -r requirements.txt

echo.
echo Starting server...
echo Web interface will be available at: http://localhost:8000
echo API documentation available at: http://localhost:8000/docs
echo.

C:/Users/abhig/Documents/Belo/Nugget/.venv/Scripts/python.exe main.py

pause
