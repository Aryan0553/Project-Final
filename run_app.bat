@echo off
title HHS Care Forecasting
echo ========================================
echo   HHS Care Forecasting - Streamlit App
echo ========================================
echo.
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Installing required packages...
python -m pip install -r requirements.txt
echo.
echo Starting Streamlit...
python -m streamlit run app.py
pause
