"""
Minimal FastAPI application for testing deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Parkinson's Disease Detection API (Minimal)",
    description="Minimal API for testing deployment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Parkinson's Disease Detection API (Minimal)",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"status": "ok", "message": "pong", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 