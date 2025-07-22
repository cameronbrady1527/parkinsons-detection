"""
Visualization utilities for Parkinson's disease detection.

This module contains simple plotting functions for data exploration and results visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Dict
import warnings

def plot_correlation_matrix(df: pd.DataFrame, 
                          method: str = 'pearson',
                          figsize: tuple = (12, 10),
                          save_path: Optional[str] = None) -> None:
    """
    Plot correlation matrix heatmap.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to analyze
    method : str
        Correlation method ('pearson', 'spearman', 'kendall')
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the plot
    """
    # Calculate correlation matrix
    corr_matrix = df.corr(method=method)
    
    # Create heatmap
    plt.figure(figsize=figsize)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(corr_matrix, 
                mask=mask,
                annot=True, 
                cmap='coolwarm', 
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={"shrink": .8})
    
    plt.title(f'Correlation Matrix ({method.capitalize()})')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Correlation matrix saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_feature_importance(importance_dict: Dict[str, float],
                          top_n: int = 15,
                          figsize: tuple = (10, 8),
                          save_path: Optional[str] = None) -> None:
    """
    Plot feature importance from dictionary.
    
    Parameters:
    -----------
    importance_dict : Dict[str, float]
        Dictionary with feature names and importance scores
    top_n : int
        Number of top features to display
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the plot
    """
    # Convert to DataFrame and sort
    importance_df = pd.DataFrame(list(importance_dict.items()), 
                                columns=['feature', 'importance'])
    importance_df = importance_df.sort_values('importance', ascending=False).head(top_n)
    
    # Create plot
    plt.figure(figsize=figsize)
    bars = plt.barh(range(len(importance_df)), importance_df['importance'])
    plt.yticks(range(len(importance_df)), importance_df['feature'])
    plt.xlabel('Feature Importance')
    plt.title(f'Top {top_n} Feature Importances')
    plt.gca().invert_yaxis()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.3f}', ha='left', va='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Feature importance plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_model_comparison(results_df: pd.DataFrame,
                         metrics: List[str] = ['accuracy', 'f1', 'precision', 'recall'],
                         figsize: tuple = (15, 10),
                         save_path: Optional[str] = None) -> None:
    """
    Plot model comparison across multiple metrics.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with model results
    metrics : List[str]
        List of metrics to plot
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the plot
    """
    n_metrics = len(metrics)
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        if i < len(axes):
            results_df.plot(x='model', y=metric, kind='bar', ax=axes[i])
            axes[i].set_title(f'{metric.capitalize()} Comparison')
            axes[i].set_ylabel(metric.capitalize())
            axes[i].tick_params(axis='x', rotation=45)
            axes[i].grid(True, alpha=0.3)
    
    # Hide unused subplots
    for i in range(n_metrics, len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Model comparison plot saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_distribution_comparison(df: pd.DataFrame,
                               feature: str,
                               target_column: str = 'status',
                               figsize: tuple = (12, 5),
                               save_path: Optional[str] = None) -> None:
    """
    Plot distribution comparison between classes for a feature.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    feature : str
        Feature to plot
    target_column : str
        Target variable column
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram
    for target_value in df[target_column].unique():
        subset = df[df[target_column] == target_value]
        ax1.hist(subset[feature], alpha=0.7, label=f'Class {target_value}', bins=20)
    
    ax1.set_xlabel(feature)
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'Distribution of {feature} by Class')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    df.boxplot(column=feature, by=target_column, ax=ax2)
    ax2.set_xlabel(target_column)
    ax2.set_ylabel(feature)
    ax2.set_title(f'Box Plot of {feature} by Class')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle(f'Feature Analysis: {feature}')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Distribution comparison saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_learning_curves(train_sizes: List[int],
                        train_scores: List[float],
                        val_scores: List[float],
                        title: str = 'Learning Curves',
                        figsize: tuple = (10, 6),
                        save_path: Optional[str] = None) -> None:
    """
    Plot learning curves for model training.
    
    Parameters:
    -----------
    train_sizes : List[int]
        Training set sizes
    train_scores : List[float]
        Training scores
    val_scores : List[float]
        Validation scores
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the plot
    """
    plt.figure(figsize=figsize)
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    plt.plot(train_sizes, train_mean, 'o-', color='r', label='Training score')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')
    
    plt.plot(train_sizes, val_mean, 'o-', color='g', label='Cross-validation score')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='g')
    
    plt.xlabel('Training Examples')
    plt.ylabel('Score')
    plt.title(title)
    plt.legend(loc='best')
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Learning curves saved to {save_path}")
    else:
        plt.show()
    
    plt.close()

def create_summary_plots(df: pd.DataFrame,
                        target_column: str = 'status',
                        save_dir: Optional[str] = None) -> None:
    """
    Create a comprehensive set of summary plots.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to analyze
    target_column : str
        Target variable column
    save_dir : str, optional
        Directory to save plots
    """
    # Target distribution
    plt.figure(figsize=(8, 6))
    df[target_column].value_counts().plot(kind='bar')
    plt.title('Target Variable Distribution')
    plt.xlabel('Class')
    plt.ylabel('Count')
    if save_dir:
        plt.savefig(f'{save_dir}/target_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Correlation matrix
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    plot_correlation_matrix(df[numeric_cols], save_path=f'{save_dir}/correlation_matrix.png' if save_dir else None)
    
    # Feature distributions for top correlated features
    corr_with_target = df[numeric_cols].corr()[target_column].abs().sort_values(ascending=False)
    top_features = corr_with_target.head(6).index.tolist()
    
    for feature in top_features:
        if feature != target_column:
            plot_distribution_comparison(df, feature, target_column, 
                                       save_path=f'{save_dir}/{feature}_distribution.png' if save_dir else None)
    
    print("Summary plots completed!") 