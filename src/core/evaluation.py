"""
Model evaluation and reporting functions for Parkinson's disease detection.

This module contains functions for comprehensive model evaluation,
performance comparison, and report generation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, 
                           roc_auc_score, confusion_matrix, classification_report, roc_curve)
from typing import Dict, List, Tuple, Optional
import warnings
import os
from datetime import datetime

def evaluate_models(models_dict: Dict, 
                   X_test: pd.DataFrame, 
                   y_test: pd.Series) -> pd.DataFrame:
    """
    Evaluate multiple models and return comparison DataFrame.
    
    Parameters:
    -----------
    models_dict : Dict
        Dictionary containing trained models
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test target
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with evaluation metrics for all models
    """
    results = []
    
    for model_name, model_info in models_dict.items():
        model = model_info['model']
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        metrics = {
            'model': model_name,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
        
        if y_pred_proba is not None:
            metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
        
        # Add cross-validation info if available
        if 'cv_mean' in model_info:
            metrics['cv_mean'] = model_info['cv_mean']
            metrics['cv_std'] = model_info['cv_std']
        
        results.append(metrics)
    
    return pd.DataFrame(results)

def create_evaluation_report(models_dict: Dict,
                           X_test: pd.DataFrame,
                           y_test: pd.Series,
                           save_path: Optional[str] = None) -> Dict:
    """
    Create comprehensive evaluation report with visualizations.
    
    Parameters:
    -----------
    models_dict : Dict
        Dictionary containing trained models
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test target
    save_path : str, optional
        Path to save the report
    
    Returns:
    --------
    Dict
        Dictionary containing evaluation results and plots
    """
    # Create timestamped output directory inside a dedicated outputs folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputs_base_dir = "outputs"
    output_dir = os.path.join(outputs_base_dir, f"output_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Evaluate all models
    evaluation_df = evaluate_models(models_dict, X_test, y_test)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Model Evaluation Report', fontsize=16)
    
    # Plot 1: Accuracy comparison
    evaluation_df.plot(x='model', y='accuracy', kind='bar', ax=axes[0, 0])
    axes[0, 0].set_title('Accuracy Comparison')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot 2: F1 Score comparison
    evaluation_df.plot(x='model', y='f1', kind='bar', ax=axes[0, 1])
    axes[0, 1].set_title('F1 Score Comparison')
    axes[0, 1].set_ylabel('F1 Score')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Plot 3: ROC Curves
    for model_name, model_info in models_dict.items():
        model = model_info['model']
        if hasattr(model, 'predict_proba'):
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            auc = roc_auc_score(y_test, y_pred_proba)
            axes[1, 0].plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.3f})')
    
    axes[1, 0].plot([0, 1], [0, 1], 'k--', label='Random')
    axes[1, 0].set_xlabel('False Positive Rate')
    axes[1, 0].set_ylabel('True Positive Rate')
    axes[1, 0].set_title('ROC Curves')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Plot 4: Confusion Matrix for best model
    best_model_name = evaluation_df.loc[evaluation_df['f1'].idxmax(), 'model']
    best_model = models_dict[best_model_name]['model']
    y_pred_best = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best)
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1])
    axes[1, 1].set_title(f'Confusion Matrix - {best_model_name}')
    axes[1, 1].set_xlabel('Predicted')
    axes[1, 1].set_ylabel('Actual')
    
    plt.tight_layout()
    
    # Save to timestamped directory
    evaluation_report_path = os.path.join(output_dir, "evaluation_report.png")
    plt.savefig(evaluation_report_path, dpi=300, bbox_inches='tight')
    print(f"Evaluation report saved to {evaluation_report_path}")
    
    plt.close()
    
    return {
        'evaluation_df': evaluation_df,
        'best_model': best_model_name,
        'best_model_object': best_model,
        'output_dir': output_dir
    }

def plot_feature_importance(model, 
                          feature_names: List[str],
                          top_n: int = 10,
                          save_path: Optional[str] = None):
    """
    Plot feature importance for models that support it.
    
    Parameters:
    -----------
    model : sklearn estimator
        Trained model with feature_importances_ attribute
    feature_names : List[str]
        List of feature names
    top_n : int
        Number of top features to display
    save_path : str, optional
        Path to save the plot
    """
    if not hasattr(model, 'feature_importances_'):
        print("Model does not support feature importance")
        return
    
    # Get feature importance
    importance = model.feature_importances_
    
    # Create DataFrame
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    # Plot top features
    plt.figure(figsize=(10, 8))
    top_features = feature_importance_df.head(top_n)
    
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Feature Importance')
    plt.title(f'Top {top_n} Feature Importances')
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Feature importance plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()
    
    return feature_importance_df 