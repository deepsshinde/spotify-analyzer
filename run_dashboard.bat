@echo off
echo 🎵 Starting Spotify Analytics Dashboard
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate

REM Run Streamlit
streamlit run src/dashboard/app.py