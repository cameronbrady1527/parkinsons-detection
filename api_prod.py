"""
Production FastAPI application for Parkinson's Disease Detection

This module provides a REST API for the Parkinson's disease detection
machine learning pipeline with endpoints for data upload, analysis, and prediction.
Optimized for production deployment without visualization dependencies.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from typing import Dict, List, Optional

# Import our project modules (core functionality only)
from src.core.data_processing import preprocess_data, feature_selection
from src.core.outlier_detection import detect_and_report_outliers
from src.core.model_training import train_models
from src.core.evaluation import evaluate_models
from src.utils.data_loading import load_parkinsons_data

# Global variables for model and scaler
trained_models = None
scaler = None
selected_features = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global trained_models, scaler, selected_features
    
    # Startup
    print("Initializing Parkinson's Disease Detection API...")
    
    try:
        print("Step 1: Loading training data...")
        # Load and preprocess the training data
        df = load_parkinsons_data()
        if df is None:
            raise Exception("Failed to load training data")
        print(f"Data loaded successfully: {df.shape}")
        
        print("Step 2: Preprocessing data...")
        # Preprocess data
        X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
        print(f"Data preprocessed: train={X_train.shape}, test={X_test.shape}")
        
        print("Step 3: Feature selection...")
        # Feature selection
        X_train_selected, X_test_selected, selected_features = feature_selection(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            method='random_forest',
            n_features=15
        )
        print(f"Features selected: {len(selected_features)}")
        
        print("Step 4: Training models...")
        # Train models
        trained_models = train_models(
            X_train=X_train_selected,
            y_train=y_train,
            models=['logistic', 'random_forest', 'svm']
        )
        
        print(f"API initialized successfully with {len(trained_models)} models")
        print(f"Selected features: {selected_features}")
        
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        import traceback
        traceback.print_exc()
        # Initialize with None values but don't crash
        trained_models = None
        scaler = None
        selected_features = None
        print("Starting API with limited functionality - models will be loaded on first request...")
    
    yield
    
    # Shutdown
    print("Shutting down Parkinson's Disease Detection API...")

# Initialize FastAPI app
app = FastAPI(
    title="Parkinson's Disease Detection API",
    description="Machine learning API for Parkinson's disease detection using voice measurements",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Parkinson's Disease Detection API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "predict": "/predict",
            "analyze": "/analyze",
            "train": "/train"
        }
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint for basic health checks"""
    return {"status": "ok", "message": "pong"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        models_status = trained_models is not None
        scaler_status = scaler is not None
        features_status = selected_features is not None
        
        # Determine overall status
        if models_status and scaler_status and features_status:
            status = "healthy"
        elif models_status or scaler_status or features_status:
            status = "degraded"
        else:
            status = "starting"
        
        return {
            "status": status,
            "models_loaded": models_status,
            "scaler_loaded": scaler_status,
            "features_loaded": features_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/info")
async def get_info():
    """Get information about the trained models"""
    if trained_models is None:
        return {
            "status": "models_not_loaded",
            "message": "Models are being loaded. Try again in a moment.",
            "timestamp": datetime.now().isoformat()
        }
    
    model_info = {}
    for name, model_data in trained_models.items():
        model_info[name] = {
            "cv_accuracy": model_data.get('cv_mean', 0),
            "cv_std": model_data.get('cv_std', 0),
            "features_count": len(selected_features) if selected_features else 0
        }
    
    return {
        "status": "ready",
        "models": model_info,
        "selected_features": selected_features,
        "total_features": len(selected_features) if selected_features else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Make predictions on uploaded data
    
    Expected CSV format with the same columns as the training data
    """
    global trained_models, scaler, selected_features
    
    # Lazy load models if not already loaded
    if trained_models is None or scaler is None:
        try:
            print("Loading models on first request...")
            df = load_parkinsons_data()
            if df is None:
                raise HTTPException(status_code=503, detail="Failed to load training data")
            
            X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
            X_train_selected, X_test_selected, selected_features = feature_selection(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                method='random_forest',
                n_features=15
            )
            trained_models = train_models(
                X_train=X_train_selected,
                y_train=y_train,
                models=['logistic', 'random_forest', 'svm']
            )
            print("Models loaded successfully!")
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Failed to load models: {str(e)}")
    
    try:
        # Read uploaded file
        df = pd.read_csv(file.file)
        
        # Validate columns (should match training data)
        expected_columns = ['name', 'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 
                           'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 
                           'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 
                           'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 
                           'status', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']
        
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {list(missing_cols)}"
            )
        
        # Preprocess the data
        feature_columns = [col for col in df.columns if col not in ['name', 'status']]
        X = df[feature_columns]
        
        # Scale features
        X_scaled = scaler.transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        # Select features
        X_selected = X_scaled_df[selected_features]
        
        # Make predictions with all models
        predictions = {}
        probabilities = {}
        
        for model_name, model_data in trained_models.items():
            model = model_data['model']
            
            # Make prediction
            pred = model.predict(X_selected)
            predictions[model_name] = pred.tolist()
            
            # Get probabilities if available
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X_selected)[:, 1]
                probabilities[model_name] = proba.tolist()
        
        return {
            "predictions": predictions,
            "probabilities": probabilities,
            "sample_count": len(df),
            "features_used": selected_features
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    """
    Perform comprehensive data analysis including outlier detection
    """
    try:
        # Read uploaded file
        df = pd.read_csv(file.file)
        
        # Basic info
        basic_info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict()
        }
        
        # Outlier detection (without plots)
        outlier_results = detect_and_report_outliers(
            df=df,
            methods=['iqr', 'zscore'],
            create_plots=False,
            verbose=False
        )
        
        # Preprocess for feature analysis
        try:
            X_train, X_test, y_train, y_test, _ = preprocess_data(df)
            X_train_selected, X_test_selected, selected_features = feature_selection(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                method='random_forest',
                n_features=15
            )
            
            # Train models for analysis
            models = train_models(
                X_train=X_train_selected,
                y_train=y_train,
                models=['random_forest']
            )
            
            # Evaluate
            evaluation_results = evaluate_models(models, X_test_selected, y_test)
            
            analysis_results = {
                "basic_info": basic_info,
                "outlier_detection": outlier_results,
                "selected_features": selected_features,
                "model_performance": evaluation_results.to_dict('records')
            }
            
        except Exception as e:
            # If preprocessing fails, return basic analysis only
            analysis_results = {
                "basic_info": basic_info,
                "outlier_detection": outlier_results,
                "error": f"Advanced analysis failed: {str(e)}"
            }
        
        return analysis_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/train")
async def retrain_models(file: UploadFile = File(...)):
    """
    Retrain models with new data
    """
    global trained_models, scaler, selected_features
    
    try:
        # Read uploaded file
        df = pd.read_csv(file.file)
        
        # Preprocess data
        X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
        
        # Feature selection
        X_train_selected, X_test_selected, selected_features = feature_selection(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            method='random_forest',
            n_features=15
        )
        
        # Train models
        trained_models = train_models(
            X_train=X_train_selected,
            y_train=y_train,
            models=['logistic', 'random_forest', 'svm']
        )
        
        # Evaluate
        evaluation_results = evaluate_models(trained_models, X_test_selected, y_test)
        
        return {
            "message": "Models retrained successfully",
            "performance": evaluation_results.to_dict('records'),
            "selected_features": selected_features,
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 