@echo off
REM Netflix Theme Question-Answering Script Runner for Windows
REM This script runs the theme_qa.py script with the necessary arguments

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

REM Parse command line arguments
setlocal EnableDelayedExpansion

set API_KEY=
set QUESTION=
set INPUT_DIR=trackedcompanies\Netflix
set OUTPUT_DIR=output
set CACHE_DIR=
set INVALIDATE_CACHE=false

REM Function to display usage
:usage
if "%~1"=="show" (
    echo Usage: run_theme_qa.bat [OPTIONS]
    echo.
    echo Required options:
    echo   -k, --api-key KEY       OpenAI API key
    echo   -q, --question TEXT     Question to answer
    echo.
    echo Optional options:
    echo   -i, --input-dir DIR     Input directory containing documents (default: trackedcompanies\Netflix)
    echo   -o, --output-dir DIR    Output directory for themes and cache (default: output)
    echo   -c, --cache-dir DIR     Directory to store cache files (default: output\cache)
    echo   -r, --refresh           Invalidate cache and reprocess all documents
    echo   -h, --help              Display this help message
    exit /b 1
)

REM Parse arguments
:parse_args
if "%~1"=="" goto :check_args

if /i "%~1"=="-k" (
    set API_KEY=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--api-key" (
    set API_KEY=%~2
    shift
    shift
    goto :parse_args
)

if /i "%~1"=="-q" (
    set QUESTION=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--question" (
    set QUESTION=%~2
    shift
    shift
    goto :parse_args
)

if /i "%~1"=="-i" (
    set INPUT_DIR=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--input-dir" (
    set INPUT_DIR=%~2
    shift
    shift
    goto :parse_args
)

if /i "%~1"=="-o" (
    set OUTPUT_DIR=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--output-dir" (
    set OUTPUT_DIR=%~2
    shift
    shift
    goto :parse_args
)

if /i "%~1"=="-c" (
    set CACHE_DIR=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--cache-dir" (
    set CACHE_DIR=%~2
    shift
    shift
    goto :parse_args
)

if /i "%~1"=="-r" (
    set INVALIDATE_CACHE=true
    shift
    goto :parse_args
)
if /i "%~1"=="--refresh" (
    set INVALIDATE_CACHE=true
    shift
    goto :parse_args
)

if /i "%~1"=="-h" (
    goto :usage show
)
if /i "%~1"=="--help" (
    goto :usage show
)

echo Unknown option: %~1
goto :usage show

:check_args
REM Check required arguments
if "!API_KEY!"=="" (
    echo Error: OpenAI API key is required
    goto :usage show
)

if "!QUESTION!"=="" (
    echo Error: Question is required
    goto :usage show
)

REM Build command
set CMD=python theme_qa.py --api-key "!API_KEY!" --question "!QUESTION!" --input-dir "!INPUT_DIR!" --output-dir "!OUTPUT_DIR!"

REM Add optional arguments
if not "!CACHE_DIR!"=="" (
    set CMD=!CMD! --cache-dir "!CACHE_DIR!"
)

if "!INVALIDATE_CACHE!"=="true" (
    set CMD=!CMD! --invalidate-cache
)

REM Print information
echo Running Netflix Theme Question-Answering Script
echo Question: !QUESTION!
echo Input directory: !INPUT_DIR!
echo Output directory: !OUTPUT_DIR!
if not "!CACHE_DIR!"=="" (
    echo Cache directory: !CACHE_DIR!
)
if "!INVALIDATE_CACHE!"=="true" (
    echo Cache will be invalidated
)
echo.
echo Loading documents and generating answer... (this may take a few minutes)
echo.

REM Run the script
%CMD%

REM Check if the script ran successfully
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Question answered successfully!
) else (
    echo.
    echo Error: Failed to answer question
    exit /b 1
)
