import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Union
import warnings

def create_box_plot(df: pd.DataFrame, 
                   numerical_columns: Optional[List[str]] = None,
                   figsize: Tuple[int, int] = (15, 10),
                   title: str = "Box Plots for Numerical Features",
                   save_path: Optional[str] = None) -> None:
    """
    Create box plots for numerical features to visualize outliers.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    numerical_columns : List[str], optional
        List of numerical column names. If None, automatically detects numerical columns.
    figsize : Tuple[int, int]
        Figure size (width, height)
    title : str
        Title for the plot
    save_path : str, optional
        Path to save the plot. If None, plot is displayed.
    """
    if numerical_columns is None:
        numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numerical_columns:
        print("No numerical columns found in the dataframe.")
        return
    
    # Calculate number of subplots
    n_cols = 3
    n_rows = (len(numerical_columns) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    fig.suptitle(title, fontsize=16, y=0.95)
    
    # Flatten axes if there's only one row
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    
    for idx, col in enumerate(numerical_columns):
        row = idx // n_cols
        col_idx = idx % n_cols
        
        # Create box plot
        sns.boxplot(data=df, y=col, ax=axes[row, col_idx])
        axes[row, col_idx].set_title(f'{col}')
        axes[row, col_idx].tick_params(axis='x', rotation=45)
    
    # Hide empty subplots
    for idx in range(len(numerical_columns), n_rows * n_cols):
        row = idx // n_cols
        col_idx = idx % n_cols
        axes[row, col_idx].set_visible(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Box plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def apply_iqr(df: pd.DataFrame, 
              column: str, 
              multiplier: float = 1.5) -> Tuple[pd.Series, Dict]:
    """
    Apply IQR method to detect outliers in a specific column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to check for outliers
    multiplier : float
        IQR multiplier (default: 1.5)
    
    Returns:
    --------
    Tuple[pd.Series, Dict]
        Boolean series indicating outliers and statistics dictionary
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataframe")
    
    # Calculate quartiles and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    # Identify outliers
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    
    # Create statistics dictionary
    stats = {
        'column': column,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'multiplier': multiplier,
        'outlier_count': outliers.sum(),
        'outlier_percentage': (outliers.sum() / len(df)) * 100,
        'min_value': df[column].min(),
        'max_value': df[column].max(),
        'mean': df[column].mean(),
        'std': df[column].std()
    }
    
    return outliers, stats

def detect_outliers_zscore(df: pd.DataFrame, 
                          column: str, 
                          threshold: float = 3.0) -> Tuple[pd.Series, Dict]:
    """
    Detect outliers using Z-score method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to check for outliers
    threshold : float
        Z-score threshold (default: 3.0)
    
    Returns:
    --------
    Tuple[pd.Series, Dict]
        Boolean series indicating outliers and statistics dictionary
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataframe")
    
    # Calculate z-scores
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    
    # Identify outliers
    outliers = z_scores > threshold
    
    # Create statistics dictionary
    stats = {
        'column': column,
        'method': 'z_score',
        'threshold': threshold,
        'outlier_count': outliers.sum(),
        'outlier_percentage': (outliers.sum() / len(df)) * 100,
        'mean': df[column].mean(),
        'std': df[column].std(),
        'min_zscore': z_scores.min(),
        'max_zscore': z_scores.max()
    }
    
    return outliers, stats

def detect_outliers_isolation_forest(df: pd.DataFrame, 
                                   column: str, 
                                   contamination: float = 0.1) -> Tuple[pd.Series, Dict]:
    """
    Detect outliers using Isolation Forest method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to check for outliers
    contamination : float
        Expected proportion of outliers (default: 0.1)
    
    Returns:
    --------
    Tuple[pd.Series, Dict]
        Boolean series indicating outliers and statistics dictionary
    """
    try:
        from sklearn.ensemble import IsolationForest
    except ImportError:
        warnings.warn("scikit-learn not available. Skipping Isolation Forest method.")
        return pd.Series([False] * len(df)), {}
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in dataframe")
    
    # Reshape data for sklearn
    X = df[column].values.reshape(-1, 1)
    
    # Fit Isolation Forest
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    predictions = iso_forest.fit_predict(X)
    
    # -1 indicates outliers, 1 indicates normal points
    outliers = predictions == -1
    
    # Create statistics dictionary
    stats = {
        'column': column,
        'method': 'isolation_forest',
        'contamination': contamination,
        'outlier_count': outliers.sum(),
        'outlier_percentage': (outliers.sum() / len(df)) * 100
    }
    
    return outliers, stats

def detect_and_report_outliers(df: pd.DataFrame,
                              numerical_columns: Optional[List[str]] = None,
                              methods: List[str] = ['iqr', 'zscore'],
                              iqr_multiplier: float = 1.5,
                              zscore_threshold: float = 3.0,
                              create_plots: bool = True,
                              plot_save_path: Optional[str] = None,
                              verbose: bool = True) -> Dict:
    """
    Comprehensive outlier detection and reporting function.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    numerical_columns : List[str], optional
        List of numerical column names. If None, automatically detects numerical columns.
    methods : List[str]
        List of outlier detection methods to use ('iqr', 'zscore', 'isolation_forest')
    iqr_multiplier : float
        IQR multiplier for IQR method
    zscore_threshold : float
        Z-score threshold for Z-score method
    create_plots : bool
        Whether to create box plots
    plot_save_path : str, optional
        Path to save box plots
    verbose : bool
        Whether to print detailed reports
    
    Returns:
    --------
    Dict
        Dictionary containing outlier detection results
    """
    if numerical_columns is None:
        numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numerical_columns:
        print("No numerical columns found in the dataframe.")
        return {}
    
    # Initialize results dictionary
    results = {
        'summary': {},
        'detailed_results': {},
        'outlier_indices': {},
        'recommendations': []
    }
    
    if verbose:
        print("=" * 60)
        print("OUTLIER DETECTION REPORT")
        print("=" * 60)
        print(f"Dataset shape: {df.shape}")
        print(f"Numerical columns: {len(numerical_columns)}")
        print(f"Methods used: {methods}")
        print()
    
    # Create box plots if requested
    if create_plots:
        if verbose:
            print("Creating box plots for visual outlier inspection...")
        create_box_plot(df, numerical_columns, save_path=plot_save_path)
    
    # Detect outliers using each method
    for method in methods:
        if verbose:
            print(f"\n--- {method.upper()} METHOD ---")
        
        method_results = {}
        total_outliers = 0
        
        for col in numerical_columns:
            try:
                if method == 'iqr':
                    outliers, stats = apply_iqr(df, col, iqr_multiplier)
                elif method == 'zscore':
                    outliers, stats = detect_outliers_zscore(df, col, zscore_threshold)
                elif method == 'isolation_forest':
                    outliers, stats = detect_outliers_isolation_forest(df, col)
                else:
                    warnings.warn(f"Unknown method: {method}")
                    continue
                
                method_results[col] = {
                    'outliers': outliers,
                    'stats': stats
                }
                
                total_outliers += stats['outlier_count']
                
                if verbose and stats['outlier_count'] > 0:
                    print(f"{col}: {stats['outlier_count']} outliers ({stats['outlier_percentage']:.2f}%)")
                
            except Exception as e:
                if verbose:
                    print(f"Error processing {col} with {method}: {str(e)}")
                continue
        
        results['detailed_results'][method] = method_results
        
        # Summary for this method
        results['summary'][method] = {
            'total_outliers': total_outliers,
            'columns_with_outliers': sum(1 for col_data in method_results.values() 
                                       if col_data['stats']['outlier_count'] > 0)
        }
        
        if verbose:
            print(f"Total outliers detected: {total_outliers}")
            print(f"Columns with outliers: {results['summary'][method]['columns_with_outliers']}")
    
    # Generate recommendations
    recommendations = []
    
    # Check for columns with high outlier percentages
    for method, method_results in results['detailed_results'].items():
        for col, col_data in method_results.items():
            outlier_pct = col_data['stats']['outlier_percentage']
            if outlier_pct > 10:
                recommendations.append(f"High outlier percentage in {col} ({outlier_pct:.1f}%) - consider investigation")
            elif outlier_pct > 5:
                recommendations.append(f"Moderate outlier percentage in {col} ({outlier_pct:.1f}%) - review if expected")
    
    # Add general recommendations
    if len(recommendations) == 0:
        recommendations.append("No significant outlier issues detected")
    
    recommendations.append("Consider domain knowledge when deciding to remove outliers")
    recommendations.append("For medical data, consult with domain experts before outlier removal")
    
    results['recommendations'] = recommendations
    
    if verbose:
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    
    return results

def get_outlier_summary(results: Dict) -> pd.DataFrame:
    """
    Create a summary DataFrame from outlier detection results.
    
    Parameters:
    -----------
    results : Dict
        Results from detect_and_report_outliers function
    
    Returns:
    --------
    pd.DataFrame
        Summary DataFrame with outlier statistics
    """
    summary_data = []
    
    for method, method_results in results['detailed_results'].items():
        for col, col_data in method_results.items():
            stats = col_data['stats']
            summary_data.append({
                'column': col,
                'method': method,
                'outlier_count': stats['outlier_count'],
                'outlier_percentage': stats['outlier_percentage'],
                'total_values': len(col_data['outliers'])
            })
    
    return pd.DataFrame(summary_data)

def remove_outliers(df: pd.DataFrame, 
                   outlier_results: Dict,
                   method: str = 'iqr',
                   columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove outliers from dataframe based on detection results.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    outlier_results : Dict
        Results from detect_and_report_outliers function
    method : str
        Method to use for outlier removal
    columns : List[str], optional
        Specific columns to process. If None, uses all columns with outliers.
    
    Returns:
    --------
    pd.DataFrame
        Dataframe with outliers removed
    """
    if method not in outlier_results['detailed_results']:
        raise ValueError(f"Method '{method}' not found in results")
    
    df_clean = df.copy()
    removed_count = 0
    
    method_results = outlier_results['detailed_results'][method]
    
    if columns is None:
        columns = list(method_results.keys())
    
    for col in columns:
        if col in method_results:
            outliers = method_results[col]['outliers']
            df_clean = df_clean[~outliers]
            removed_count += outliers.sum()
    
    print(f"Removed {removed_count} outliers using {method} method")
    print(f"Original shape: {df.shape} -> Cleaned shape: {df_clean.shape}")
    
    return df_clean

# Example usage function
def example_usage():
    """
    Example usage of the outlier detection functions.
    """
    # Create sample data with outliers
    np.random.seed(42)
    data = {
        'normal_feature': np.random.normal(0, 1, 1000),
        'feature_with_outliers': np.concatenate([
            np.random.normal(0, 1, 950),
            np.random.normal(10, 1, 50)  # Outliers
        ]),
        'categorical_feature': np.random.choice(['A', 'B', 'C'], 1000)
    }
    
    df = pd.DataFrame(data)
    
    # Add some extreme outliers
    df.loc[0, 'normal_feature'] = 100
    df.loc[1, 'normal_feature'] = -100
    
    print("Sample dataset created with known outliers")
    print(f"Dataset shape: {df.shape}")
    
    # Detect outliers
    results = detect_and_report_outliers(
        df=df,
        methods=['iqr', 'zscore'],
        create_plots=True,
        verbose=True
    )
    
    # Get summary
    summary_df = get_outlier_summary(results)
    print("\nOutlier Summary:")
    print(summary_df)
    
    # Remove outliers
    df_clean = remove_outliers(df, results, method='iqr')
    
    return df, df_clean, results

if __name__ == "__main__":
    # Run example
    df, df_clean, results = example_usage() 