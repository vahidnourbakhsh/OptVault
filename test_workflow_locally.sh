#!/bin/bash
# Test GitHub Actions workflow steps locally

set -e  # Exit on any error

echo "🧪 Testing GitHub Actions workflow locally..."

echo "📋 Step 1: Check Python version"
python --version

echo "📋 Step 2: Check if GLPK is available"
python -c "
import subprocess
try:
    result = subprocess.run(['glpsol', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ GLPK found:', result.stdout.split()[0])
    else:
        print('❌ GLPK not working')
except FileNotFoundError:
    print('❌ GLPK not installed - install with: conda install -c conda-forge glpk')
"

echo "📋 Step 3: Install Python dependencies"
pip install -e ".[dev]"

echo "📋 Step 4: Format check with Black"
black --check --verbose src/ tests/

echo "📋 Step 5: Run tests with pytest"
pytest tests/ -v --tb=short

echo "📋 Step 6: Check package installation"
python -c "import optvault; print('✅ OptVault version:', optvault.__version__)"

echo "✅ All workflow steps completed successfully!"
