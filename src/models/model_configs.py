"""
Model configurations for Parkinson's disease detection.

This module contains model parameter configurations and hyperparameter grids
for different machine learning models.
"""

from typing import Dict, List, Any

def get_model_configs() -> Dict[str, Dict[str, Any]]:
    """
    Get default model configurations.
    
    Returns:
    --------
    Dict[str, Dict[str, Any]]
        Dictionary containing model configurations
    """
    configs = {
        'logistic_regression': {
            'model_class': 'LogisticRegression',
            'default_params': {
                'C': 1.0,
                'penalty': 'l2',
                'solver': 'liblinear',
                'max_iter': 1000,
                'random_state': 42
            },
            'description': 'Linear classification model with L2 regularization'
        },
        
        'support_vector_machine': {
            'model_class': 'SVC',
            'default_params': {
                'C': 1.0,
                'kernel': 'rbf',
                'gamma': 'scale',
                'probability': True,
                'random_state': 42
            },
            'description': 'Support Vector Classification with RBF kernel'
        },
        
        'random_forest': {
            'model_class': 'RandomForestClassifier',
            'default_params': {
                'n_estimators': 100,
                'max_depth': None,
                'min_samples_split': 2,
                'min_samples_leaf': 1,
                'random_state': 42
            },
            'description': 'Ensemble of decision trees with bagging'
        },
        
        'k_nearest_neighbors': {
            'model_class': 'KNeighborsClassifier',
            'default_params': {
                'n_neighbors': 5,
                'weights': 'uniform',
                'metric': 'euclidean'
            },
            'description': 'K-Nearest Neighbors classification'
        },
        
        'gradient_boosting': {
            'model_class': 'GradientBoostingClassifier',
            'default_params': {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 3,
                'random_state': 42
            },
            'description': 'Gradient Boosting ensemble method'
        },
        
        'naive_bayes': {
            'model_class': 'GaussianNB',
            'default_params': {
                'var_smoothing': 1e-9
            },
            'description': 'Gaussian Naive Bayes classifier'
        }
    }
    
    return configs

def get_hyperparameter_grids() -> Dict[str, Dict[str, List[Any]]]:
    """
    Get hyperparameter grids for grid search.
    
    Returns:
    --------
    Dict[str, Dict[str, List[Any]]]
        Dictionary containing hyperparameter grids
    """
    grids = {
        'logistic_regression': {
            'C': [0.1, 1, 10, 100],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear', 'saga'],
            'max_iter': [1000]
        },
        
        'support_vector_machine': {
            'C': [0.1, 1, 10, 100],
            'kernel': ['rbf', 'linear'],
            'gamma': ['scale', 'auto', 0.1, 0.01],
            'probability': [True]
        },
        
        'random_forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        
        'k_nearest_neighbors': {
            'n_neighbors': [3, 5, 7, 9, 11],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan']
        },
        
        'gradient_boosting': {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7],
            'subsample': [0.8, 0.9, 1.0]
        }
    }
    
    return grids

def get_feature_selection_configs() -> Dict[str, Dict[str, Any]]:
    """
    Get feature selection configurations.
    
    Returns:
    --------
    Dict[str, Dict[str, Any]]
        Dictionary containing feature selection configurations
    """
    configs = {
        'kbest': {
            'method': 'SelectKBest',
            'score_func': 'f_classif',
            'k_options': [10, 15, 20, 25]
        },
        
        'rfe': {
            'method': 'RFE',
            'estimator': 'RandomForestClassifier',
            'n_features_options': [10, 15, 20, 25]
        },
        
        'random_forest_importance': {
            'method': 'RandomForestImportance',
            'n_estimators': 100,
            'threshold': 0.01
        },
        
        'correlation_based': {
            'method': 'CorrelationBased',
            'threshold': 0.8,
            'target_correlation_threshold': 0.1
        }
    }
    
    return configs

def get_evaluation_configs() -> Dict[str, Any]:
    """
    Get evaluation configurations.
    
    Returns:
    --------
    Dict[str, Any]
        Dictionary containing evaluation configurations
    """
    configs = {
        'cv_folds': 5,
        'scoring_metrics': ['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
        'test_size': 0.2,
        'random_state': 42,
        'stratify': True,
        'n_jobs': -1
    }
    
    return configs

def get_preprocessing_configs() -> Dict[str, Any]:
    """
    Get preprocessing configurations.
    
    Returns:
    --------
    Dict[str, Any]
        Dictionary containing preprocessing configurations
    """
    configs = {
        'scaling_methods': ['standard', 'minmax', 'robust', 'none'],
        'outlier_methods': ['iqr', 'zscore', 'isolation_forest'],
        'missing_value_strategies': ['drop', 'fill_mean', 'fill_median', 'fill_mode'],
        'feature_engineering': {
            'polynomial_features': False,
            'interaction_features': False,
            'feature_aggregation': False
        }
    }
    
    return configs 