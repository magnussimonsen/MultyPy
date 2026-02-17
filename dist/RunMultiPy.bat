@echo off
echo Starting MultiPy...
echo.
MultiPy.exe
if errorlevel 1 (
    echo.
    echo An error occurred. Exit code: %errorlevel%
)
echo.
pause
