#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-8000}

echo "Starting Parkinson's Disease Detection API on port $PORT"
echo "Environment: PORT=$PORT"

# Start the application with proper error handling
exec uvicorn api_prod:app --host 0.0.0.0 --port $PORT --log-level info 