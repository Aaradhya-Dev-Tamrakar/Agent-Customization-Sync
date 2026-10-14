@echo off
setlocal
cd /d "%~dp0"
call custom_sync.bat mirror-memory %*
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
