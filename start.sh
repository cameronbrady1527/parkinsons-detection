#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

echo "=== Starting Parkinson's Disease Detection API ==="
echo "Environment: PORT=$PORT"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Pip list:"
pip list

echo "=== Testing Python import ==="
python -c "import api_prod; print('Import successful')" || {
    echo "ERROR: Failed to import api_prod"
    echo "Checking for missing dependencies..."
    python -c "import fastapi; print('FastAPI available')" || echo "FastAPI missing"
    python -c "import pandas; print('Pandas available')" || echo "Pandas missing"
    python -c "import numpy; print('NumPy available')" || echo "NumPy missing"
    python -c "import joblib; print('Joblib available')" || echo "Joblib missing"
    exit 1
}

echo "=== Testing data loading ==="
python -c "
from src.utils.data_loading import load_parkinsons_data
df = load_parkinsons_data()
print(f'Data loaded: {df.shape if df is not None else None}')
" || {
    echo "WARNING: Data loading test failed, but continuing..."
}

echo "=== Starting uvicorn ==="
# Start the application with proper error handling
exec uvicorn api_prod:app --host 0.0.0.0 --port $PORT --log-level info 