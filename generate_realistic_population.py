#!/usr/bin/env python3
"""
Generate realistic population datasets for Parkinson's disease detection.

This script creates datasets that reflect real-world disease prevalence rather than
clinical study populations. Parkinson's disease affects approximately 0.1-0.5% of the
general population, rising to 1-3% in people over 60. For screening scenarios, we'll
use a 5% prevalence to simulate a higher-risk population (e.g., elderly screening).
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_original_data():
    """Load the original Parkinson's dataset."""
    data_path = Path(__file__).parent / 'data' / 'parkinsons.data'
    if not data_path.exists():
        print(f"Original dataset not found at {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Original dataset: {len(df)} samples")
    print(f"Positive cases: {df['status'].sum()} ({df['status'].mean()*100:.1f}%)")
    print(f"Negative cases: {len(df) - df['status'].sum()} ({(1-df['status'].mean())*100:.1f}%)")
    return df

def generate_realistic_sample(original_df, is_positive, sample_id):
    """
    Generate a realistic sample based on the original dataset.
    
    Args:
        original_df: Original Parkinson's dataset
        is_positive: Whether this should be a positive (1) or negative (0) sample
        sample_id: Unique identifier for the sample
    
    Returns:
        Dictionary representing a single sample
    """
    # Get samples of the same class from original data
    class_samples = original_df[original_df['status'] == is_positive]
    
    if len(class_samples) == 0:
        print(f"Warning: No samples found for class {is_positive}")
        return None
    
    # Randomly select a base sample
    base_sample = class_samples.sample(n=1).iloc[0]
    
    # Add realistic variation to the features
    sample = base_sample.copy()
    sample['name'] = f"population_sample_{sample_id:06d}"
    
    # Add realistic noise to voice measurements (5-15% variation)
    feature_cols = [col for col in sample.index if col not in ['name', 'status']]
    
    for col in feature_cols:
        if pd.notna(sample[col]) and sample[col] != 0:
            # Add Gaussian noise (5-15% of the original value)
            noise_factor = np.random.uniform(0.05, 0.15)
            noise = np.random.normal(0, abs(sample[col]) * noise_factor)
            sample[col] = sample[col] + noise
            
            # Ensure values stay positive for measurements that should be positive
            if sample[col] < 0 and base_sample[col] > 0:
                sample[col] = abs(sample[col])
    
    return sample

def create_population_dataset(original_df, total_size=10000, prevalence=0.05, output_name="realistic_population"):
    """
    Create a realistic population dataset with specified prevalence.
    
    Args:
        original_df: Original Parkinson's dataset
        total_size: Total number of samples to generate
        prevalence: Proportion of positive cases (0.05 = 5%)
        output_name: Name for the output file
    """
    print(f"\nGenerating {output_name} dataset:")
    print(f"Total size: {total_size:,} samples")
    print(f"Prevalence: {prevalence*100:.1f}%")
    
    # Calculate number of positive and negative samples
    n_positive = int(total_size * prevalence)
    n_negative = total_size - n_positive
    
    print(f"Positive samples: {n_positive:,}")
    print(f"Negative samples: {n_negative:,}")
    
    # Generate samples
    samples = []
    sample_id = 1
    
    # Generate positive samples
    print("Generating positive samples...")
    for i in range(n_positive):
        if i % 100 == 0:
            print(f"  Progress: {i}/{n_positive}")
        
        sample = generate_realistic_sample(original_df, 1, sample_id)
        if sample is not None:
            samples.append(sample)
        sample_id += 1
    
    # Generate negative samples
    print("Generating negative samples...")
    for i in range(n_negative):
        if i % 1000 == 0:
            print(f"  Progress: {i}/{n_negative}")
        
        sample = generate_realistic_sample(original_df, 0, sample_id)
        if sample is not None:
            samples.append(sample)
        sample_id += 1
    
    # Create DataFrame
    population_df = pd.DataFrame(samples)
    
    # Shuffle the dataset
    population_df = population_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save to CSV
    output_path = Path(__file__).parent / 'static' / f'demo_{output_name}.csv'
    population_df.to_csv(output_path, index=False)
    
    print(f"\nDataset saved to: {output_path}")
    print(f"Final dataset: {len(population_df)} samples")
    print(f"Actual positive rate: {population_df['status'].mean()*100:.2f}%")
    
    return population_df

def create_screening_datasets():
    """Create multiple realistic screening datasets."""
    
    # Load original data
    original_df = load_original_data()
    if original_df is None:
        return
    
    print("="*60)
    print("REALISTIC POPULATION DATASET GENERATOR")
    print("="*60)
    
    # Dataset 1: General population screening (0.5% prevalence)
    create_population_dataset(
        original_df, 
        total_size=5000, 
        prevalence=0.005,  # 0.5%
        output_name="general_population"
    )
    
    # Dataset 2: High-risk population screening (5% prevalence) 
    create_population_dataset(
        original_df,
        total_size=2000,
        prevalence=0.05,   # 5%
        output_name="high_risk_population"
    )
    
    # Dataset 3: Elderly screening (2% prevalence)
    create_population_dataset(
        original_df,
        total_size=3000,
        prevalence=0.02,   # 2%
        output_name="elderly_screening"
    )
    
    # Dataset 4: Clinic screening (15% prevalence - symptomatic patients)
    create_population_dataset(
        original_df,
        total_size=1000,
        prevalence=0.15,   # 15%
        output_name="clinic_screening"
    )

if __name__ == "__main__":
    create_screening_datasets()
    print("\n" + "="*60)
    print("DATASET GENERATION COMPLETE")
    print("="*60)
    print("\nGenerated datasets:")
    print("1. General Population (0.5% prevalence) - 5,000 samples")
    print("2. High-Risk Population (5% prevalence) - 2,000 samples") 
    print("3. Elderly Screening (2% prevalence) - 3,000 samples")
    print("4. Clinic Screening (15% prevalence) - 1,000 samples")
    print("\nThese datasets reflect realistic disease prevalence rates")
    print("suitable for different screening scenarios.")