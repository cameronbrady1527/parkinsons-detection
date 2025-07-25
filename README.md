# Parkinson's Disease Detection Using Machine Learning

## Overview
This project aims to develop a machine learning model to detect Parkinson's Disease using voice measurements. The project features a comprehensive, modular architecture with automated data processing, outlier detection, feature selection, model training, and evaluation pipelines.

## Project Structure
```
parkinsons-detection/
├── data/                           # Dataset from UCI Machine Learning Repository
│   └── parkinsons.data
├── src/                            # Source code with modular architecture
│   ├── core/                       # Heavy computational functions
│   │   ├── data_processing.py      # Data preprocessing and feature selection
│   │   ├── outlier_detection.py    # Comprehensive outlier detection
│   │   ├── model_training.py       # Model training and hyperparameter tuning
│   │   └── evaluation.py           # Model evaluation and reporting
│   ├── utils/                      # Simple helper functions
│   │   ├── data_loading.py         # Data loading utilities
│   │   ├── visualization.py        # Plotting and visualization
│   │   └── notebook_integration.py # Notebook-specific functions
│   ├── models/                     # Model configurations
│   │   └── model_configs.py        # Model parameters and hyperparameter grids
│   └── example_usage.py            # Complete example demonstrating all functionality
├── static/                         # Frontend web interface
│   ├── index.html                  # Main HTML page
│   ├── styles.css                  # Modern CSS styling
│   ├── script.js                   # JavaScript functionality
│   ├── sample_data.csv             # Sample data for testing
│   └── README.md                   # Frontend documentation
├── notebooks/                      # Jupyter notebooks for exploration
│   └── exploratory_analysis.ipynb
├── outputs/                        # Generated output files (timestamped)
│   └── output_YYYYMMDD_HHMMSS/     # Individual run outputs
├── venv/                           # Virtual environment files
├── api_prod.py                     # Production FastAPI server
├── requirements-prod.txt           # Production dependencies
└── README.md                       # Project documentation
```

## Features

### 🔍 **Comprehensive Data Analysis**
- **Data Loading**: Automated loading with basic information display
- **Outlier Detection**: Multiple methods (IQR, Z-Score) with detailed reporting
- **Data Preprocessing**: Standardization, train/test splitting, missing value handling
- **Feature Selection**: Random Forest-based feature importance selection

### 🤖 **Machine Learning Pipeline**
- **Multiple Models**: Logistic Regression, Random Forest, SVM
- **Cross-Validation**: Automated cross-validation with performance metrics
- **Model Evaluation**: Comprehensive evaluation with accuracy, precision, recall, F1-score, and ROC-AUC
- **Hyperparameter Tuning**: Grid search optimization capabilities

### 📊 **Automated Visualization**
- **Evaluation Reports**: Multi-panel plots with model comparisons
- **Correlation Matrices**: Feature correlation analysis
- **Feature Importance**: Top feature visualization
- **Outlier Plots**: Box plots for outlier detection

### 📁 **Organized Output Management**
- **Timestamped Directories**: Each run creates a unique output directory
- **Centralized Storage**: All outputs saved to `outputs/` directory
- **Git Integration**: Output directories ignored, structure preserved

### 🌐 **Web Interface**
- **Modern Frontend**: Beautiful, responsive web interface for easy data upload and analysis
- **Real-time API**: FastAPI backend with RESTful endpoints
- **Drag & Drop**: Intuitive file upload with drag and drop support
- **Live Status**: Real-time API health monitoring and model information display

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd parkinsons-detection
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🚀 **Quick Start - Complete Pipeline**

Run the complete analysis pipeline with a single command:

```bash
python src/example_usage.py
```

**What to expect:**
```
============================================================
PARKINSON'S DISEASE DETECTION PROJECT
============================================================

1. Loading data...
Dataset loaded successfully from data/parkinsons.data
Shape: (195, 24)
Columns: ['name', 'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', ...]

2. Basic data inspection...
==================================================
BASIC DATASET INFORMATION
==================================================
Dataset shape: (195, 24)
Number of samples: 195
Number of features: 24
...

3. Quick outlier check...
Checking outliers in 22 numerical columns...

4. Comprehensive outlier detection...
============================================================
OUTLIER DETECTION REPORT
============================================================
--- IQR METHOD ---
MDVP:Fhi(Hz): 11 outliers (5.64%)
...
Total outliers detected: 221
Columns with outliers: 20

5. Data preprocessing...
Training set shape: (156, 22)
Test set shape: (39, 22)

6. Feature selection...
Selected 15 features
Selected features: ['PPE', 'spread1', 'MDVP:Fo(Hz)', ...]

7. Training models...
Training logistic...
logistic - CV Accuracy: 0.8335 (+/- 0.1100)
Training random_forest...
random_forest - CV Accuracy: 0.9171 (+/- 0.1019)
Training svm...
svm - CV Accuracy: 0.8718 (+/- 0.0409)

8. Evaluating models...
Model Evaluation Results:
           model  accuracy  precision    recall        f1   roc_auc
0       logistic  0.923077   0.933333  0.965517  0.949153  0.910345
1  random_forest  0.948718   0.965517  0.965517  0.965517  0.953448
2            svm  0.923077   0.906250  1.000000  0.950820  0.955172

9. Creating evaluation report...
Evaluation report saved to outputs/output_20250722_182134/evaluation_report.png

10. Creating visualizations...
Correlation matrix saved to outputs/output_20250722_182134/correlation_matrix.png
Feature importance plot saved to outputs/output_20250722_182134/feature_importance.png

============================================================
PROJECT EXECUTION COMPLETED
============================================================
Best model: random_forest
Selected features: 15
Check the outputs/output_20250722_182134/ folder for generated plots and reports.
```

### 📊 **Generated Outputs**

Each run creates a timestamped directory containing:
- **`evaluation_report.png`**: Comprehensive model evaluation with 4 panels:
  - Accuracy comparison across models
  - F1-score comparison
  - ROC curves for all models
  - Confusion matrix for best model
- **`correlation_matrix.png`**: Feature correlation heatmap
- **`feature_importance.png`**: Top feature importance plot

### 📓 **Jupyter Notebooks**

For interactive exploration and development:

```bash
jupyter notebook
```

Then open `notebooks/exploratory_analysis.ipynb` for:
- Interactive data exploration
- Custom model development
- Experimentation with different parameters

### 🌐 **Web Interface Usage**

For the easiest way to use the application, deploy the web interface:

```bash
# Run the production server
python api_prod.py
```

Then visit `http://localhost:8000` in your browser to access the modern web interface.

**Features:**
- Upload CSV files via drag & drop
- Real-time API health monitoring
- Beautiful results visualization
- Model performance metrics
- Responsive design for all devices

### 🔧 **Modular Usage**

Import specific modules for custom analysis:

```python
# Data loading
from utils.data_loading import load_parkinsons_data
df = load_parkinsons_data()

# Outlier detection
from core.outlier_detection import detect_and_report_outliers
outliers = detect_and_report_outliers(df, methods=['iqr', 'zscore'])

# Data preprocessing
from core.data_processing import preprocess_data
X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

# Model training
from core.model_training import train_models
models = train_models(X_train, y_train, models=['random_forest', 'svm'])

# Evaluation
from core.evaluation import evaluate_models
results = evaluate_models(models, X_test, y_test)
```

## Model Performance

Based on the current implementation, typical performance metrics:

| Model | Accuracy | F1-Score | ROC-AUC |
|-------|----------|----------|---------|
| Random Forest | 94.9% | 96.6% | 95.3% |
| SVM | 92.3% | 95.1% | 95.5% |
| Logistic Regression | 92.3% | 94.9% | 91.0% |

## Dependencies
- Python 3.x
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- jupyter

## License
[Apache license 2.0](license/license.txt)

## Acknowledgments
Dataset is sourced from the UCI Machine Learning Repository:

    Max A. Little, Patrick E. McSharry, Eric J. Hunter, Lorraine O. Ramig (2008), 'Suitability of 
    dysphonia measurements for telemonitoring of Parkinson's disease', IEEE Transactions on 
    Biomedical Engineering (to appear).