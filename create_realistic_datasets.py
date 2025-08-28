#!/usr/bin/env python3
"""
Create realistic datasets for Parkinson's disease detection demo.

This script generates datasets with realistic disease prevalence rates for different
screening scenarios, based on the original parkinsons.data dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import shutil

def load_original_data():
    """Load the original Parkinson's dataset."""
    data_path = Path(__file__).parent / 'data' / 'parkinsons.data'
    if not data_path.exists():
        print(f"Original dataset not found at {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Original dataset loaded: {len(df)} samples")
    print(f"Positive cases: {df['status'].sum()} ({df['status'].mean()*100:.1f}%)")
    print(f"Negative cases: {len(df) - df['status'].sum()} ({(1-df['status'].mean())*100:.1f}%)")
    return df

def generate_sample_with_variation(base_sample, variation_factor=0.1):
    """
    Generate a new sample by adding realistic variation to a base sample.
    
    Args:
        base_sample: Original sample from the dataset
        variation_factor: Amount of variation to add (0.1 = 10%)
    
    Returns:
        Modified sample with realistic variation
    """
    sample = base_sample.copy()
    
    # Get feature columns (exclude name and status)
    feature_cols = [col for col in sample.index if col not in ['name', 'status']]
    
    for col in feature_cols:
        if pd.notna(sample[col]) and sample[col] != 0:
            # Add Gaussian noise based on the original value
            noise = np.random.normal(0, abs(sample[col]) * variation_factor)
            sample[col] = sample[col] + noise
            
            # Ensure positive values stay positive for measurements
            if sample[col] < 0 and base_sample[col] > 0:
                sample[col] = abs(sample[col])
    
    return sample

def create_balanced_dataset(original_df, total_size, prevalence, name, description):
    """
    Create a balanced dataset with specified prevalence.
    
    Args:
        original_df: Original Parkinson's dataset
        total_size: Total number of samples
        prevalence: Fraction of positive cases (e.g., 0.05 = 5%)
        name: Dataset name
        description: Dataset description
    """
    print(f"\nCreating {name}...")
    print(f"Target size: {total_size:,} samples")
    print(f"Target prevalence: {prevalence*100:.1f}%")
    
    # Calculate target counts
    n_positive = int(total_size * prevalence)
    n_negative = total_size - n_positive
    
    print(f"Positive samples: {n_positive:,}")
    print(f"Negative samples: {n_negative:,}")
    
    # Separate original data by class
    positive_samples = original_df[original_df['status'] == 1]
    negative_samples = original_df[original_df['status'] == 0]
    
    print(f"Available positive samples: {len(positive_samples)}")
    print(f"Available negative samples: {len(negative_samples)}")
    
    # Generate new samples
    new_samples = []
    sample_id = 1
    
    # Generate positive samples
    for i in range(n_positive):
        # Randomly select a base sample
        base_sample = positive_samples.sample(n=1).iloc[0]
        
        # Create variation
        new_sample = generate_sample_with_variation(base_sample, variation_factor=0.12)
        new_sample['name'] = f"{name.lower().replace(' ', '_')}_pos_{sample_id:04d}"
        new_samples.append(new_sample)
        sample_id += 1
    
    # Generate negative samples  
    for i in range(n_negative):
        # Randomly select a base sample
        base_sample = negative_samples.sample(n=1).iloc[0]
        
        # Create variation
        new_sample = generate_sample_with_variation(base_sample, variation_factor=0.12)
        new_sample['name'] = f"{name.lower().replace(' ', '_')}_neg_{sample_id:04d}"
        new_samples.append(new_sample)
        sample_id += 1
    
    # Create DataFrame and shuffle
    new_df = pd.DataFrame(new_samples)
    new_df = new_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save to CSV
    filename = f"demo_{name.lower().replace(' ', '_')}.csv"
    output_path = Path(__file__).parent / 'static' / filename
    new_df.to_csv(output_path, index=False)
    
    # Verify final statistics
    actual_positive_rate = new_df['status'].mean()
    print(f"Saved to: {filename}")
    print(f"Final size: {len(new_df):,} samples")
    print(f"Actual positive rate: {actual_positive_rate*100:.1f}%")
    print(f"Dataset created successfully")
    
    return new_df, filename

def backup_existing_datasets():
    """Backup existing demo datasets."""
    static_path = Path(__file__).parent / 'static'
    backup_path = static_path / 'backup_original_demos'
    backup_path.mkdir(exist_ok=True)
    
    existing_demos = [
        'demo_early_stage.csv',
        'demo_advanced_stage.csv', 
        'demo_mixed_cohort.csv',
        'demo_large_dataset.csv'
    ]
    
    print("Backing up existing demo datasets...")
    for demo_file in existing_demos:
        source = static_path / demo_file
        if source.exists():
            target = backup_path / demo_file
            shutil.copy2(source, target)
            print(f"Backed up: {demo_file}")

def create_all_realistic_datasets():
    """Create all realistic datasets for the demo."""
    print("="*80)
    print("REALISTIC PARKINSON'S DATASET GENERATOR")
    print("="*80)
    
    # Load original data
    original_df = load_original_data()
    if original_df is None:
        return
    
    # Backup existing datasets
    backup_existing_datasets()
    
    print(f"\nGenerating realistic datasets based on {len(original_df)} original samples...")
    
    datasets_created = []
    
    # 1. General Population Screening (0.5% prevalence)
    df, filename = create_balanced_dataset(
        original_df,
        total_size=2000,
        prevalence=0.005,  # 0.5%
        name="General Population",
        description="Realistic general population screening (0.5% prevalence)"
    )
    datasets_created.append(("General Population Screening", filename, "0.5%", "2,000", "Realistic screening scenario"))
    
    # 2. Elderly Screening (2% prevalence)
    df, filename = create_balanced_dataset(
        original_df,
        total_size=1500,
        prevalence=0.02,  # 2%
        name="Elderly Screening", 
        description="Elderly population screening (2% prevalence)"
    )
    datasets_created.append(("Elderly Population Screening", filename, "2%", "1,500", "Age 65+ screening"))
    
    # 3. High-Risk Screening (5% prevalence)
    df, filename = create_balanced_dataset(
        original_df,
        total_size=1000,
        prevalence=0.05,  # 5%
        name="High Risk Screening",
        description="High-risk population with family history (5% prevalence)"
    )
    datasets_created.append(("High-Risk Screening", filename, "5%", "1,000", "Family history, symptoms"))
    
    # 4. Symptom-Based Screening (15% prevalence)
    df, filename = create_balanced_dataset(
        original_df,
        total_size=800,
        prevalence=0.15,  # 15%
        name="Symptom Based Screening",
        description="Patients with motor symptoms referred for evaluation (15% prevalence)"  
    )
    datasets_created.append(("Symptom-Based Screening", filename, "15%", "800", "Patients with motor symptoms"))
    
    # 5. Small Balanced Sample
    df, filename = create_balanced_dataset(
        original_df,
        total_size=100,
        prevalence=0.03,  # 3%
        name="Small Balanced Sample",
        description="Small balanced sample for quick testing (3% prevalence)"
    )
    datasets_created.append(("Small Balanced Sample", filename, "3%", "100", "Quick testing dataset"))
    
    print("\n" + "="*80)
    print("DATASET CREATION COMPLETE")
    print("="*80)
    
    print("\nCreated datasets:")
    for name, filename, prevalence, size, description in datasets_created:
        print(f"- {name}")
        print(f"  File: {filename}")
        print(f"  Prevalence: {prevalence} | Size: {size}")
        print(f"  Use: {description}")
        print()
    
    print("Note: Original biased datasets have been backed up to static/backup_original_demos/")
    print("These new datasets reflect realistic disease prevalence for different screening scenarios.")

if __name__ == "__main__":
    create_all_realistic_datasets()