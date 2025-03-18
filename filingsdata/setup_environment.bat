@echo off
REM Netflix Theme Extraction Environment Setup Script for Windows
REM This script sets up a Python virtual environment and installs the required dependencies

echo Setting up Netflix Theme Extraction environment...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in your PATH
    echo Please install Python and try again
    exit /b 1
)

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv netflix-themes-env

REM Check if virtual environment was created successfully
if not exist "netflix-themes-env" (
    echo Error: Failed to create virtual environment
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call netflix-themes-env\Scripts\activate.bat

REM Check if activation was successful
if "%VIRTUAL_ENV%"=="" (
    echo Error: Failed to activate virtual environment
    exit /b 1
)

REM Install dependencies
echo Installing required dependencies...
pip install -r requirements.txt

REM Check if installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo.
echo Environment setup completed successfully!
echo.
echo To activate the virtual environment in the future, run:
echo   netflix-themes-env\Scripts\activate.bat
echo.
echo To run the theme extraction script, use:
echo   python theme_extractor.py --api-key YOUR_OPENAI_API_KEY
echo.
echo To deactivate the virtual environment when you're done, run:
echo   deactivate
