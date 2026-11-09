@echo off
chcp 65001 >nul
cls
python "%~dp0record_cli.py"
echo.
pause
