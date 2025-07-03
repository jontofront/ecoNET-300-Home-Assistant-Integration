@echo off
REM Setup script for pre-commit hooks (Windows)

echo 🔧 Setting up pre-commit hooks for ecoNET300 integration...

REM Install pre-commit if not already installed
python -c "import pre_commit" 2>nul
if errorlevel 1 (
    echo 📦 Installing pre-commit...
    pip install pre-commit
) else (
    echo ✅ pre-commit already installed
)

REM Install pre-commit hooks
echo 🔗 Installing pre-commit hooks...
pre-commit install

REM Run initial validation
echo 🧪 Running initial validation...
python tests/validation/check_translations.py

echo ✅ Pre-commit setup complete!
echo.
echo 📋 Next time you commit, the following checks will run automatically:
echo    - Translation validation
echo    - Python syntax checks
echo    - JSON syntax checks
echo    - Code formatting (Ruff)
echo    - General code quality checks
echo.
echo 💡 To run checks manually: pre-commit run --all-files
pause 