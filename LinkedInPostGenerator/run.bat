@echo off
REM LinkedIn Post Generator - Windows Run Script

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the program with all arguments
python main.py %*

REM Keep window open if there's an error
if errorlevel 1 pause
