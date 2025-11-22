@echo off
REM Simple script to run PDF Table Title Fixer
REM Make sure dependencies are installed: pip install -r requirements.txt

echo Starting PDF Table Title Fixer...
echo.
python src/main.py

if errorlevel 1 (
    echo.
    echo Error occurred. Check the output above.
    echo Make sure dependencies are installed: pip install -r requirements.txt
    pause
)

