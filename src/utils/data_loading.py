"""
Data loading utilities for Parkinson's disease detection.

This module contains simple functions for loading and basic data inspection.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import os

def load_parkinsons_data(data_path: str = 'data/parkinsons.data') -> pd.DataFrame:
    """
    Load the Parkinson's disease dataset.
    
    Parameters:
    -----------
    data_path : str
        Path to the data file
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    """
    try:
        df = pd.read_csv(data_path)
        print(f"Dataset loaded successfully from {data_path}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {data_path}")
        print("Please ensure the data file exists in the correct location.")
        return None
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def load_processed_data(data_path: str) -> pd.DataFrame:
    """
    Load processed/cleaned dataset.
    
    Parameters:
    -----------
    data_path : str
        Path to the processed data file
    
    Returns:
    --------
    pd.DataFrame
        Loaded processed dataset
    """
    try:
        df = pd.read_csv(data_path)
        print(f"Processed dataset loaded from {data_path}")
        print(f"Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Processed data not found at {data_path}")
        return None

def basic_data_info(df: pd.DataFrame) -> None:
    """
    Display basic information about the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to analyze
    """
    print("=" * 50)
    print("BASIC DATASET INFORMATION")
    print("=" * 50)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Number of samples: {df.shape[0]}")
    print(f"Number of features: {df.shape[1]}")
    
    print("\nData types:")
    print(df.dtypes.value_counts())
    
    print("\nMissing values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values found")
    
    print("\nFirst few rows:")
    print(df.head())
    
    print("\nBasic statistics:")
    print(df.describe())

def check_data_quality(df: pd.DataFrame) -> dict:
    """
    Perform basic data quality checks.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to check
    
    Returns:
    --------
    dict
        Dictionary with quality check results
    """
    quality_report = {}
    
    # Check for missing values
    missing_values = df.isnull().sum()
    quality_report['missing_values'] = missing_values.to_dict()
    quality_report['total_missing'] = missing_values.sum()
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    quality_report['duplicate_rows'] = duplicates
    
    # Check data types
    quality_report['data_types'] = df.dtypes.to_dict()
    
    # Check for infinite values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    infinite_values = {}
    for col in numeric_cols:
        infinite_count = np.isinf(df[col]).sum()
        if infinite_count > 0:
            infinite_values[col] = infinite_count
    
    quality_report['infinite_values'] = infinite_values
    
    # Check for negative values in features that shouldn't be negative
    negative_values = {}
    for col in numeric_cols:
        if 'jitter' in col.lower() or 'shimmer' in col.lower():
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                negative_values[col] = negative_count
    
    quality_report['negative_values'] = negative_values
    
    return quality_report

def save_processed_data(df: pd.DataFrame, 
                       filepath: str, 
                       description: str = "") -> bool:
    """
    Save processed dataset with metadata.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to save
    filepath : str
        Path where to save the file
    description : str
        Description of the processing performed
    
    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the data
        df.to_csv(filepath, index=False)
        
        # Save metadata
        metadata_path = filepath.replace('.csv', '_metadata.txt')
        with open(metadata_path, 'w') as f:
            f.write(f"Dataset: {os.path.basename(filepath)}\n")
            f.write(f"Shape: {df.shape}\n")
            f.write(f"Created: {pd.Timestamp.now()}\n")
            f.write(f"Description: {description}\n")
            f.write(f"Columns: {list(df.columns)}\n")
        
        print(f"Data saved successfully to {filepath}")
        print(f"Metadata saved to {metadata_path}")
        return True
        
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        return False 