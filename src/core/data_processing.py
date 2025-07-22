"""
Data processing functions for Parkinson's disease detection.

This module contains heavy computational functions for data preprocessing,
feature engineering, and data cleaning.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, List, Tuple, Optional
import warnings

def preprocess_data(df: pd.DataFrame, 
                   target_column: str = 'status',
                   exclude_columns: List[str] = ['name'],
                   handle_missing: str = 'drop',
                   scale_method: str = 'standard') -> Tuple[pd.DataFrame, pd.DataFrame, object]:
    """
    Comprehensive data preprocessing pipeline.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    target_column : str
        Name of target variable column
    exclude_columns : List[str]
        Columns to exclude from processing
    handle_missing : str
        Method to handle missing values ('drop', 'fill_mean', 'fill_median')
    scale_method : str
        Scaling method ('standard', 'minmax', 'none')
    
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame, object]
        X_train, X_test, y_train, y_test, scaler
    """
    from sklearn.model_selection import train_test_split
    
    # Create copy to avoid modifying original
    df_processed = df.copy()
    
    # Handle missing values
    if handle_missing == 'drop':
        df_processed = df_processed.dropna()
    elif handle_missing == 'fill_mean':
        df_processed = df_processed.fillna(df_processed.mean())
    elif handle_missing == 'fill_median':
        df_processed = df_processed.fillna(df_processed.median())
    
    # Separate features and target
    feature_columns = [col for col in df_processed.columns 
                      if col not in exclude_columns + [target_column]]
    
    X = df_processed[feature_columns]
    y = df_processed[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    if scale_method == 'standard':
        scaler = StandardScaler()
    elif scale_method == 'minmax':
        scaler = MinMaxScaler()
    else:
        scaler = None
    
    if scaler is not None:
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        X_train = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    return X_train, X_test, y_train, y_test, scaler

def feature_selection(X_train: pd.DataFrame, 
                     y_train: pd.Series,
                     X_test: pd.DataFrame = None,
                     method: str = 'kbest',
                     n_features: int = 15,
                     random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    """
    Feature selection using various methods.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training target
    method : str
        Selection method ('kbest', 'rfe', 'random_forest')
    n_features : int
        Number of features to select
    random_state : int
        Random state for reproducibility
    
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame, List[str]]
        Selected features for train and test, feature names
    """
    if method == 'kbest':
        selector = SelectKBest(score_func=f_classif, k=n_features)
    elif method == 'rfe':
        estimator = RandomForestClassifier(n_estimators=100, random_state=random_state)
        selector = RFE(estimator=estimator, n_features_to_select=n_features)
    elif method == 'random_forest':
        # Use Random Forest feature importance
        rf = RandomForestClassifier(n_estimators=100, random_state=random_state)
        rf.fit(X_train, y_train)
        
        # Get top features
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': rf.feature_importances_
        }).sort_values('importance', ascending=False)
        
        selected_features = feature_importance.head(n_features)['feature'].tolist()
        if X_test is not None:
            return X_train[selected_features], X_test[selected_features], selected_features
        else:
            return X_train[selected_features], X_train[selected_features], selected_features
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Fit and transform
    X_train_selected = selector.fit_transform(X_train, y_train)
    selected_features = X_train.columns[selector.get_support()].tolist()
    
    return pd.DataFrame(X_train_selected, columns=selected_features, index=X_train.index), \
           pd.DataFrame(X_train_selected, columns=selected_features, index=X_train.index), \
           selected_features

def scale_features(X_train: pd.DataFrame, 
                  X_test: pd.DataFrame,
                  method: str = 'standard') -> Tuple[pd.DataFrame, pd.DataFrame, object]:
    """
    Scale features using specified method.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    X_test : pd.DataFrame
        Test features
    method : str
        Scaling method ('standard', 'minmax', 'robust')
    
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame, object]
        Scaled features and scaler object
    """
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'robust':
        from sklearn.preprocessing import RobustScaler
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unknown scaling method: {method}")
    
    # Fit and transform
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return (pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index),
            pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index),
            scaler) 