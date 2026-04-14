@echo off
echo 🎵 Spotify Analytics Pipeline Runner
echo ====================================

REM Activate virtual environment
call venv\Scripts\activate

REM Run the pipeline
python src/main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Ready to view dashboard!
    echo Run: run_dashboard.bat
) else (
    echo ❌ Pipeline failed. Check errors above.
    exit /b 1
)