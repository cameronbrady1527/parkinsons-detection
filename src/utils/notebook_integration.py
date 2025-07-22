"""
Integration functions for Jupyter notebook outlier detection.
Copy these functions into your notebook for easy outlier detection.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional

def quick_outlier_check(df: pd.DataFrame, 
                       exclude_columns: List[str] = ['name', 'status']) -> Dict:
    """
    Quick outlier check for your Parkinson's dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Your Parkinson's dataset
    exclude_columns : List[str]
        Columns to exclude from outlier detection (e.g., ID and target columns)
    
    Returns:
    --------
    Dict
        Dictionary with outlier detection results
    """
    # Get numerical columns, excluding specified columns
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_columns = [col for col in numerical_columns if col not in exclude_columns]
    
    print(f"Checking outliers in {len(numerical_columns)} numerical columns...")
    
    # Simple IQR-based outlier detection
    outlier_results = {}
    
    for col in numerical_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outliers.sum()
        outlier_percentage = (outlier_count / len(df)) * 100
        
        outlier_results[col] = {
            'outlier_count': outlier_count,
            'outlier_percentage': outlier_percentage,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_indices': df[outliers].index.tolist()
        }
    
    return outlier_results

def plot_outliers_summary(df: pd.DataFrame, outlier_results: Dict):
    """
    Create a summary plot of outliers found.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Your dataset
    outlier_results : Dict
        Results from quick_outlier_check function
    """
    # Create summary data
    summary_data = []
    for col, results in outlier_results.items():
        if results['outlier_count'] > 0:
            summary_data.append({
                'column': col,
                'outlier_count': results['outlier_count'],
                'outlier_percentage': results['outlier_percentage']
            })
    
    if not summary_data:
        print("No outliers detected!")
        return
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Outlier counts
    summary_df.plot(x='column', y='outlier_count', kind='bar', ax=ax1)
    ax1.set_title('Number of Outliers by Column')
    ax1.set_xlabel('Column')
    ax1.set_ylabel('Number of Outliers')
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Outlier percentages
    summary_df.plot(x='column', y='outlier_percentage', kind='bar', ax=ax2)
    ax2.set_title('Outlier Percentage by Column')
    ax2.set_xlabel('Column')
    ax2.set_ylabel('Outlier Percentage (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\nOutlier Summary:")
    print(summary_df.sort_values('outlier_percentage', ascending=False))

def remove_outliers_simple(df: pd.DataFrame, 
                          outlier_results: Dict,
                          threshold_percentage: float = 5.0) -> pd.DataFrame:
    """
    Remove outliers from dataframe based on percentage threshold.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Your dataset
    outlier_results : Dict
        Results from quick_outlier_check function
    threshold_percentage : float
        Only remove outliers if percentage is above this threshold
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataset
    """
    df_clean = df.copy()
    removed_rows = set()
    
    for col, results in outlier_results.items():
        if results['outlier_percentage'] > threshold_percentage:
            outlier_indices = results['outlier_indices']
            removed_rows.update(outlier_indices)
            print(f"Removing {len(outlier_indices)} outliers from {col} ({results['outlier_percentage']:.1f}%)")
    
    if removed_rows:
        df_clean = df_clean.drop(index=list(removed_rows))
        print(f"\nRemoved {len(removed_rows)} total rows with outliers")
        print(f"Original shape: {df.shape} -> Cleaned shape: {df_clean.shape}")
    else:
        print("No outliers removed (all percentages below threshold)")
    
    return df_clean

# Example usage for your notebook:
def example_notebook_usage():
    """
    Example usage - copy this into your notebook cell:
    """
    # Load your data
    # df = pd.read_csv('data/parkinsons.data')
    
    # Quick outlier check
    outlier_results = quick_outlier_check(df, exclude_columns=['name', 'status'])
    
    # Plot summary
    plot_outliers_summary(df, outlier_results)
    
    # Remove outliers (optional)
    # df_clean = remove_outliers_simple(df, outlier_results, threshold_percentage=5.0)
    
    return outlier_results

# Simple one-liner function for your notebook
def detect_outliers_parkinsons(df: pd.DataFrame) -> Dict:
    """
    One-liner outlier detection for Parkinson's dataset.
    Just call this function with your dataframe!
    """
    return quick_outlier_check(df, exclude_columns=['name', 'status']) 