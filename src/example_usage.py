"""
Example usage of the Parkinson's disease detection project structure.

This script demonstrates how to use the organized modules for your project.
"""

import pandas as pd
import numpy as np
import os

# Import from core modules (heavy computational functions)
from core.outlier_detection import detect_and_report_outliers
from core.data_processing import preprocess_data, feature_selection
from core.model_training import train_models, hyperparameter_tuning
from core.evaluation import evaluate_models, create_evaluation_report

# Import from utils modules (simple helper functions)
from utils.data_loading import load_parkinsons_data, basic_data_info
from utils.visualization import plot_correlation_matrix, plot_feature_importance
from utils.notebook_integration import quick_outlier_check, plot_outliers_summary

# Import from models modules (configurations)
from models.model_configs import get_model_configs, get_hyperparameter_grids

def main():
    """
    Main function demonstrating the project structure usage.
    """
    print("=" * 60)
    print("PARKINSON'S DISEASE DETECTION PROJECT")
    print("=" * 60)
    
    # Step 1: Load data using utils
    print("\n1. Loading data...")
    df = load_parkinsons_data()
    
    if df is None:
        print("Failed to load data. Exiting.")
        return
    
    # Step 2: Basic data inspection using utils
    print("\n2. Basic data inspection...")
    basic_data_info(df)
    
    # Step 3: Quick outlier check using utils (for notebooks)
    print("\n3. Quick outlier check...")
    outlier_results = quick_outlier_check(df, exclude_columns=['name', 'status'])
    
    # Step 4: Comprehensive outlier detection using core
    print("\n4. Comprehensive outlier detection...")
    comprehensive_results = detect_and_report_outliers(
        df=df,
        methods=['iqr', 'zscore'],
        create_plots=True,
        verbose=True
    )
    
    # Step 5: Data preprocessing using core
    print("\n5. Data preprocessing...")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(
        df=df,
        target_column='status',
        exclude_columns=['name'],
        scale_method='standard'
    )
    
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    
    # Step 6: Feature selection using core
    print("\n6. Feature selection...")
    X_train_selected, X_test_selected, selected_features = feature_selection(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        method='random_forest',
        n_features=15
    )
    
    print(f"Selected {len(selected_features)} features")
    print(f"Selected features: {selected_features}")
    
    # Step 7: Model training using core
    print("\n7. Training models...")
    models_results = train_models(
        X_train=X_train_selected,
        y_train=y_train,
        models=['logistic', 'random_forest', 'svm']
    )
    
    # Step 8: Model evaluation using core
    print("\n8. Evaluating models...")
    evaluation_results = evaluate_models(models_results, X_test_selected, y_test)
    print("\nModel Evaluation Results:")
    print(evaluation_results)
    
    # Step 9: Create evaluation report using core
    print("\n9. Creating evaluation report...")
    report_results = create_evaluation_report(
        models_dict=models_results,
        X_test=X_test_selected,
        y_test=y_test
    )
    
    # Step 10: Visualization using utils
    print("\n10. Creating visualizations...")
    
    # Get the output directory from the evaluation report
    output_dir = report_results['output_dir']
    
    # Correlation matrix
    plot_correlation_matrix(
        df[selected_features + ['status']],
        save_path=os.path.join(output_dir, 'correlation_matrix.png')
    )
    
    # Feature importance for best model
    best_model_name = report_results['best_model']
    best_model = models_results[best_model_name]['model']
    
    if hasattr(best_model, 'feature_importances_'):
        importance_dict = dict(zip(selected_features, best_model.feature_importances_))
        plot_feature_importance(
            importance_dict,
            save_path=os.path.join(output_dir, 'feature_importance.png')
        )
    
    print("\n" + "=" * 60)
    print("PROJECT EXECUTION COMPLETED")
    print("=" * 60)
    print(f"Best model: {best_model_name}")
    print(f"Selected features: {len(selected_features)}")
    print(f"Check the {output_dir}/ folder for generated plots and reports.")

def notebook_example():
    """
    Example for use in Jupyter notebooks.
    """
    # Simple one-liner imports for notebooks
    from utils.data_loading import load_parkinsons_data
    from utils.notebook_integration import detect_outliers_parkinsons
    from core.data_processing import preprocess_data
    from core.model_training import train_models
    from utils.visualization import plot_correlation_matrix
    
    # Load data
    df = load_parkinsons_data()
    
    # Quick outlier detection
    outliers = detect_outliers_parkinsons(df)
    
    # Preprocess data
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    
    # Train models
    models = train_models(X_train, y_train)
    
    # Plot correlation matrix
    plot_correlation_matrix(df)
    
    return df, models, (X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main() 