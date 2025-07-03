#!/bin/bash

# Setup script for pre-commit hooks

echo "🔧 Setting up pre-commit hooks for ecoNET300 integration..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
else
    echo "✅ pre-commit already installed"
fi

# Install pre-commit hooks
echo "🔗 Installing pre-commit hooks..."
pre-commit install

# Run initial validation
echo "🧪 Running initial validation..."
python tests/validation/check_translations.py

echo "✅ Pre-commit setup complete!"
echo ""
echo "📋 Next time you commit, the following checks will run automatically:"
echo "   - Translation validation"
echo "   - Python syntax checks"
echo "   - JSON syntax checks"
echo "   - Code formatting (Ruff)"
echo "   - General code quality checks"
echo ""
echo "💡 To run checks manually: pre-commit run --all-files" 