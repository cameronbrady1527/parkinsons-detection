# Use Python 3.11 slim image for better compatibility
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy production requirements first for better caching
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .

# Create outputs directory
RUN mkdir -p outputs

# Make startup script executable
COPY start.sh .
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:${PORT:-8000}/ping || exit 1

# Run the production application
CMD ["./start.sh"] 