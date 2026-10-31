
@echo off
title JanSetu AI Launcher

cd /d "%~dp0"

echo Starting JanSetu AI...

docker compose up -d

if errorlevel 1 (
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)

start "JanSetu AI Frontend" cmd /k "cd /d ""%~dp0frontend"" && npm.cmd run dev"

echo.
echo Open http://localhost:5173/
pause
