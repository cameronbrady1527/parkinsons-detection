#!/usr/bin/env python3
"""
Generate a large, realistic Parkinson's detection dataset
Creates 100+ samples with diverse demographics and severity levels
"""

import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_sample(case_type, severity=None, age_group=None, gender=None):
    """Generate a single sample with realistic voice measurements"""
    
    # Base ranges from original dataset analysis
    if case_type == 'healthy':
        base_params = {
            'MDVP:Fo(Hz)': (140, 240),
            'MDVP:Fhi(Hz)': (160, 280), 
            'MDVP:Flo(Hz)': (120, 220),
            'MDVP:Jitter(%)': (0.002, 0.012),
            'MDVP:Jitter(Abs)': (0.00001, 0.00008),
            'MDVP:RAP': (0.001, 0.006),
            'MDVP:PPQ': (0.001, 0.007),
            'Jitter:DDP': (0.003, 0.018),
            'MDVP:Shimmer': (0.010, 0.035),
            'MDVP:Shimmer(dB)': (0.1, 0.35),
            'Shimmer:APQ3': (0.005, 0.018),
            'Shimmer:APQ5': (0.006, 0.022),
            'MDVP:APQ': (0.008, 0.025),
            'Shimmer:DDA': (0.015, 0.054),
            'NHR': (0.001, 0.080),
            'HNR': (20, 32),
            'RPDE': (0.30, 0.55),
            'DFA': (0.65, 0.78),
            'spread1': (-7.5, -5.5),
            'spread2': (0.15, 0.25),
            'D2': (1.7, 2.3),
            'PPE': (0.05, 0.20),
            'status': 0
        }
    else:  # Parkinson's cases
        # Adjust based on severity
        severity_multipliers = {
            'mild': {'jitter': 1.5, 'shimmer': 1.3, 'nhr': 1.5, 'hnr': 0.8, 'ppe': 1.8},
            'moderate': {'jitter': 2.5, 'shimmer': 2.0, 'nhr': 2.5, 'hnr': 0.7, 'ppe': 2.5},
            'severe': {'jitter': 4.0, 'shimmer': 3.5, 'nhr': 4.0, 'hnr': 0.5, 'ppe': 3.5}
        }
        
        mult = severity_multipliers.get(severity, severity_multipliers['moderate'])
        
        base_params = {
            'MDVP:Fo(Hz)': (100, 200),
            'MDVP:Fhi(Hz)': (130, 240),
            'MDVP:Flo(Hz)': (80, 180),
            'MDVP:Jitter(%)': (0.008 * mult['jitter'], 0.030 * mult['jitter']),
            'MDVP:Jitter(Abs)': (0.00005 * mult['jitter'], 0.00020 * mult['jitter']),
            'MDVP:RAP': (0.004 * mult['jitter'], 0.015 * mult['jitter']),
            'MDVP:PPQ': (0.005 * mult['jitter'], 0.018 * mult['jitter']),
            'Jitter:DDP': (0.012 * mult['jitter'], 0.045 * mult['jitter']),
            'MDVP:Shimmer': (0.030 * mult['shimmer'], 0.100 * mult['shimmer']),
            'MDVP:Shimmer(dB)': (0.3 * mult['shimmer'], 1.0 * mult['shimmer']),
            'Shimmer:APQ3': (0.015 * mult['shimmer'], 0.050 * mult['shimmer']),
            'Shimmer:APQ5': (0.020 * mult['shimmer'], 0.065 * mult['shimmer']),
            'MDVP:APQ': (0.025 * mult['shimmer'], 0.080 * mult['shimmer']),
            'Shimmer:DDA': (0.045 * mult['shimmer'], 0.150 * mult['shimmer']),
            'NHR': (0.015 * mult['nhr'], 0.250 * mult['nhr']),
            'HNR': (12 * mult['hnr'], 25 * mult['hnr']),
            'RPDE': (0.40, 0.65),
            'DFA': (0.58, 0.82),
            'spread1': (-5.0, -3.0),
            'spread2': (0.25, 0.45),
            'D2': (2.2, 3.2),
            'PPE': (0.15 * mult['ppe'], 0.50 * mult['ppe']),
            'status': 1
        }
    
    # Gender adjustments (females typically have higher fundamental frequency)
    if gender == 'female':
        base_params['MDVP:Fo(Hz)'] = (base_params['MDVP:Fo(Hz)'][0] * 1.3, 
                                      base_params['MDVP:Fo(Hz)'][1] * 1.3)
        base_params['MDVP:Fhi(Hz)'] = (base_params['MDVP:Fhi(Hz)'][0] * 1.3,
                                       base_params['MDVP:Fhi(Hz)'][1] * 1.3)
        base_params['MDVP:Flo(Hz)'] = (base_params['MDVP:Flo(Hz)'][0] * 1.3,
                                       base_params['MDVP:Flo(Hz)'][1] * 1.3)
    
    # Age adjustments (older voices tend to be more variable)
    if age_group == 'elderly':
        for param in ['MDVP:Jitter(%)', 'MDVP:Shimmer', 'NHR']:
            if param in base_params:
                min_val, max_val = base_params[param]
                base_params[param] = (min_val * 1.2, max_val * 1.4)
    
    # Generate sample
    sample = {}
    for param, value in base_params.items():
        if param == 'status':
            sample[param] = value
        else:
            min_val, max_val = value
            sample[param] = np.random.uniform(min_val, max_val)
    
    return sample

def generate_large_dataset():
    """Generate comprehensive dataset with 120 samples"""
    
    samples = []
    sample_id = 1
    
    # Demographics distribution
    case_types = [
        ('healthy', None, 'young', 'male', 8),
        ('healthy', None, 'young', 'female', 8), 
        ('healthy', None, 'middle', 'male', 6),
        ('healthy', None, 'middle', 'female', 6),
        ('healthy', None, 'elderly', 'male', 6),
        ('healthy', None, 'elderly', 'female', 6),
        
        ('parkinsons', 'mild', 'young', 'male', 4),
        ('parkinsons', 'mild', 'young', 'female', 4),
        ('parkinsons', 'mild', 'middle', 'male', 8),
        ('parkinsons', 'mild', 'middle', 'female', 8),
        ('parkinsons', 'mild', 'elderly', 'male', 8),
        ('parkinsons', 'mild', 'elderly', 'female', 8),
        
        ('parkinsons', 'moderate', 'middle', 'male', 8),
        ('parkinsons', 'moderate', 'middle', 'female', 8),
        ('parkinsons', 'moderate', 'elderly', 'male', 10),
        ('parkinsons', 'moderate', 'elderly', 'female', 10),
        
        ('parkinsons', 'severe', 'elderly', 'male', 6),
        ('parkinsons', 'severe', 'elderly', 'female', 6),
    ]
    
    for case_type, severity, age_group, gender, count in case_types:
        for i in range(count):
            sample = generate_sample(case_type, severity, age_group, gender)
            
            # Generate realistic name
            if case_type == 'healthy':
                prefix = f"healthy_{age_group}_{gender}_{i+1}"
            else:
                prefix = f"pd_{severity}_{age_group}_{gender}_{i+1}"
            
            sample['name'] = prefix
            samples.append(sample)
            sample_id += 1
    
    # Create DataFrame
    df = pd.DataFrame(samples)
    
    # Reorder columns to match original dataset
    column_order = [
        'name', 'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 
        'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 
        'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 
        'NHR', 'HNR', 'status', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE'
    ]
    
    df = df[column_order]
    
    print(f"Generated {len(df)} samples:")
    print(f"Healthy cases: {sum(df['status'] == 0)}")
    print(f"Parkinson's cases: {sum(df['status'] == 1)}")
    
    # Save to CSV
    df.to_csv('static/demo_large_dataset.csv', index=False)
    print("\nLarge dataset saved to: static/demo_large_dataset.csv")
    
    return df

if __name__ == "__main__":
    generate_large_dataset()