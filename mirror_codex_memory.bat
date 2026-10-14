@echo off
setlocal
cd /d "%~dp0"
call custom_sync.bat mirror-memory %*
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" pause
exit /b %RESULT%
