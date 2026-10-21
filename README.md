# HHS Care Forecasting - VS Code + Streamlit

## Files
- app.py - Streamlit application
- requirements.txt - Python packages
- run_app.bat - one-click Windows launcher
- HHS_Unaccompanied_Alien_Children_Program.csv - place your original dataset here

## Manual VS Code setup

Open this folder in VS Code, then open Terminal and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501 if the browser does not open automatically.

## Easiest method

Put your CSV in this folder and double-click `run_app.bat`.

## Stop

Press Ctrl+C in the terminal.

## Dashboard pages

1. Dashboard
2. Data Overview
3. Trend Analysis
4. ML Forecasting
5. Feature Importance
6. Capacity Risk
7. Export CSV / Excel
