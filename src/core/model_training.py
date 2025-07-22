"""
Model training functions for Parkinson's disease detection.

This module contains heavy computational functions for model training,
hyperparameter tuning, and model evaluation.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from typing import Dict, List, Tuple, Optional
import warnings

def train_models(X_train: pd.DataFrame, 
                y_train: pd.Series,
                models: Optional[List[str]] = None,
                random_state: int = 42) -> Dict:
    """
    Train multiple models with default parameters.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training target
    models : List[str], optional
        List of models to train ('logistic', 'svm', 'random_forest', 'knn')
    random_state : int
        Random state for reproducibility
    
    Returns:
    --------
    Dict
        Dictionary containing trained models and their basic metrics
    """
    if models is None:
        models = ['logistic', 'svm', 'random_forest', 'knn']
    
    model_configs = {
        'logistic': LogisticRegression(random_state=random_state, max_iter=1000),
        'svm': SVC(random_state=random_state, probability=True),
        'random_forest': RandomForestClassifier(random_state=random_state, n_estimators=100),
        'knn': KNeighborsClassifier(n_neighbors=5)
    }
    
    results = {}
    
    for model_name in models:
        if model_name not in model_configs:
            warnings.warn(f"Unknown model: {model_name}")
            continue
        
        print(f"Training {model_name}...")
        model = model_configs[model_name]
        
        # Train model
        model.fit(X_train, y_train)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        
        results[model_name] = {
            'model': model,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'cv_scores': cv_scores
        }
        
        print(f"{model_name} - CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return results

def hyperparameter_tuning(X_train: pd.DataFrame,
                         y_train: pd.Series,
                         model_name: str,
                         param_grid: Optional[Dict] = None,
                         cv: int = 5,
                         scoring: str = 'f1',
                         n_jobs: int = -1) -> Dict:
    """
    Perform hyperparameter tuning for a specific model.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training target
    model_name : str
        Name of the model to tune
    param_grid : Dict, optional
        Parameter grid for tuning
    cv : int
        Number of cross-validation folds
    scoring : str
        Scoring metric
    n_jobs : int
        Number of jobs for parallel processing
    
    Returns:
    --------
    Dict
        Dictionary containing best model and tuning results
    """
    # Default parameter grids
    default_grids = {
        'logistic': {
            'C': [0.1, 1, 10, 100],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear', 'saga']
        },
        'svm': {
            'C': [0.1, 1, 10, 100],
            'kernel': ['rbf', 'linear'],
            'gamma': ['scale', 'auto', 0.1, 0.01]
        },
        'random_forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        },
        'knn': {
            'n_neighbors': [3, 5, 7, 9, 11],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan']
        }
    }
    
    if param_grid is None:
        param_grid = default_grids.get(model_name, {})
    
    # Get base model
    base_models = {
        'logistic': LogisticRegression(random_state=42, max_iter=1000),
        'svm': SVC(random_state=42, probability=True),
        'random_forest': RandomForestClassifier(random_state=42),
        'knn': KNeighborsClassifier()
    }
    
    if model_name not in base_models:
        raise ValueError(f"Unknown model: {model_name}")
    
    base_model = base_models[model_name]
    
    # Perform grid search
    print(f"Performing hyperparameter tuning for {model_name}...")
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        cv=cv,
        scoring=scoring,
        n_jobs=n_jobs,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    return {
        'best_model': grid_search.best_estimator_,
        'best_params': grid_search.best_params_,
        'best_score': grid_search.best_score_,
        'cv_results': grid_search.cv_results_,
        'grid_search': grid_search
    }

def evaluate_model(model, 
                  X_test: pd.DataFrame, 
                  y_test: pd.Series) -> Dict:
    """
    Evaluate a trained model on test data.
    
    Parameters:
    -----------
    model : sklearn estimator
        Trained model
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test target
    
    Returns:
    --------
    Dict
        Dictionary containing evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred)
    }
    
    if y_pred_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
    
    return metrics 