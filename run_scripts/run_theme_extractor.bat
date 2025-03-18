@echo off
REM Netflix Theme Extraction Script Runner for Windows
REM This script runs the theme_extractor.py script with the necessary arguments

REM Check if running in a virtual environment
if "%VIRTUAL_ENV%"=="" (
    echo Warning: It is recommended to run this script in a Python virtual environment.
    echo See the README.md file for instructions on setting up a virtual environment.
    set /p continue_without_venv="Continue without a virtual environment? (y/n): "
    if /i not "%continue_without_venv%"=="y" (
        echo Exiting. Please set up a virtual environment before running this script.
        exit /b 1
    )
    echo.
)

REM Check if OpenAI API key is provided
if "%~1"=="" (
    echo Error: OpenAI API key is required
    echo Usage: run_theme_extractor.bat YOUR_OPENAI_API_KEY [input_dir] [output_dir]
    exit /b 1
)

REM Set default values
set API_KEY=%~1
if "%~2"=="" (
    set INPUT_DIR=trackedcompanies\Netflix
) else (
    set INPUT_DIR=%~2
)
if "%~3"=="" (
    set OUTPUT_DIR=output
) else (
    set OUTPUT_DIR=%~3
)

REM Print information
echo Running Netflix Theme Extraction Script
echo Input directory: %INPUT_DIR%
echo Output directory: %OUTPUT_DIR%
echo.

REM Run the script
python theme_extractor.py --api-key "%API_KEY%" --input-dir "%INPUT_DIR%" --output-dir "%OUTPUT_DIR%"

REM Check if the script ran successfully
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Theme extraction completed successfully!
    echo Results are available in: %OUTPUT_DIR%\netflix_themes.md
) else (
    echo.
    echo Error: Theme extraction failed
    exit /b 1
)
