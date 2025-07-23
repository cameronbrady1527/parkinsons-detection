#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

echo "=== Starting Parkinson's Disease Detection API ==="
echo "Environment: PORT=$PORT"
echo "Current directory: $(pwd)"

echo "=== Testing Python import ==="
python -c "import api_prod; print('Import successful')" || {
    echo "ERROR: Failed to import api_prod"
    exit 1
}

echo "=== Starting uvicorn ==="
# Start the application with proper error handling
exec uvicorn api_prod:app --host 0.0.0.0 --port $PORT --log-level info 