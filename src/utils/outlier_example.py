"""
Example usage of outlier detection functions with Parkinson's dataset.
This script demonstrates how to integrate outlier detection into your project.
"""

import pandas as pd
import numpy as np
from outlier_detection import detect_and_report_outliers, get_outlier_summary, remove_outliers

def main():
    """
    Main function to demonstrate outlier detection on Parkinson's dataset.
    """
    print("Loading Parkinson's dataset...")
    
    # Load the dataset
    try:
        df = pd.read_csv('../data/parkinsons.data')
        print(f"Dataset loaded successfully. Shape: {df.shape}")
    except FileNotFoundError:
        print("Dataset not found. Creating sample data for demonstration...")
        # Create sample data if dataset is not available
        np.random.seed(42)
        data = {
            'MDVP:Fo(Hz)': np.random.normal(120, 20, 200),
            'MDVP:Fhi(Hz)': np.random.normal(150, 30, 200),
            'MDVP:Flo(Hz)': np.random.normal(80, 15, 200),
            'MDVP:Jitter(%)': np.random.normal(0.01, 0.005, 200),
            'status': np.random.choice([0, 1], 200)
        }
        df = pd.DataFrame(data)
        
        # Add some outliers for demonstration
        df.loc[0, 'MDVP:Fo(Hz)'] = 300  # Extreme outlier
        df.loc[1, 'MDVP:Fhi(Hz)'] = 50   # Extreme outlier
        df.loc[2, 'MDVP:Jitter(%)'] = 0.1  # Extreme outlier
    
    # Remove non-numerical columns for outlier detection
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove 'status' column as it's the target variable
    if 'status' in numerical_columns:
        numerical_columns.remove('status')
    
    print(f"Numerical columns for outlier detection: {numerical_columns}")
    
    # Detect outliers using multiple methods
    print("\n" + "="*50)
    print("DETECTING OUTLIERS")
    print("="*50)
    
    results = detect_and_report_outliers(
        df=df,
        numerical_columns=numerical_columns,
        methods=['iqr', 'zscore'],
        iqr_multiplier=1.5,
        zscore_threshold=3.0,
        create_plots=True,
        plot_save_path='../notebooks/outlier_boxplots.png',
        verbose=True
    )
    
    # Get summary statistics
    print("\n" + "="*50)
    print("OUTLIER SUMMARY")
    print("="*50)
    
    summary_df = get_outlier_summary(results)
    print(summary_df)
    
    # Show columns with most outliers
    if not summary_df.empty:
        print("\nColumns with highest outlier percentages:")
        high_outliers = summary_df[summary_df['outlier_percentage'] > 5].sort_values('outlier_percentage', ascending=False)
        if not high_outliers.empty:
            print(high_outliers[['column', 'method', 'outlier_percentage']])
        else:
            print("No columns with >5% outliers found")
    
    # Ask user if they want to remove outliers
    print("\n" + "="*50)
    print("OUTLIER REMOVAL OPTIONS")
    print("="*50)
    
    print("Options:")
    print("1. Remove outliers using IQR method")
    print("2. Remove outliers using Z-score method")
    print("3. Keep all data (no outlier removal)")
    print("4. View detailed outlier information")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        print("\nRemoving outliers using IQR method...")
        df_clean = remove_outliers(df, results, method='iqr')
        
        # Save cleaned dataset
        df_clean.to_csv('../data/parkinsons_clean_iqr.csv', index=False)
        print("Cleaned dataset saved as 'parkinsons_clean_iqr.csv'")
        
    elif choice == '2':
        print("\nRemoving outliers using Z-score method...")
        df_clean = remove_outliers(df, results, method='zscore')
        
        # Save cleaned dataset
        df_clean.to_csv('../data/parkinsons_clean_zscore.csv', index=False)
        print("Cleaned dataset saved as 'parkinsons_clean_zscore.csv'")
        
    elif choice == '3':
        print("\nKeeping all data. No outliers removed.")
        df_clean = df.copy()
        
    elif choice == '4':
        print("\nDetailed outlier information:")
        for method, method_results in results['detailed_results'].items():
            print(f"\n{method.upper()} METHOD DETAILS:")
            for col, col_data in method_results.items():
                stats = col_data['stats']
                if stats['outlier_count'] > 0:
                    print(f"  {col}:")
                    print(f"    - Outliers: {stats['outlier_count']} ({stats['outlier_percentage']:.2f}%)")
                    if method == 'iqr':
                        print(f"    - Bounds: [{stats['lower_bound']:.4f}, {stats['upper_bound']:.4f}]")
                        print(f"    - IQR: {stats['IQR']:.4f}")
                    elif method == 'zscore':
                        print(f"    - Threshold: {stats['threshold']}")
                        print(f"    - Max Z-score: {stats['max_zscore']:.2f}")
    
    else:
        print("Invalid choice. Keeping all data.")
        df_clean = df.copy()
    
    # Final summary
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(f"Original dataset shape: {df.shape}")
    print(f"Final dataset shape: {df_clean.shape}")
    print(f"Rows removed: {len(df) - len(df_clean)}")
    
    return df, df_clean, results

if __name__ == "__main__":
    df, df_clean, results = main() 