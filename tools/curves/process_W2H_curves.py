#!/usr/bin/env python3
"""
CSV Curve Normalizer

This script processes a CSV file containing a time series curve and outputs 
a normalized version with exactly 8760 values that sum to 1/3600.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path


def process_curve(input_csv_path, output_file_path, target_column='NL_heat_profile_water_SFH'):
    """
    Process the CSV curve file and create a normalized output.
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_file_path (str): Full path to the output file (including filename)
        target_column (str): Name of the column to process
    
    Returns:
        str: Path to the created output file
    """
    
    # Validate input file exists
    if not os.path.isfile(input_csv_path):
        raise FileNotFoundError(f"Input file not found: {input_csv_path}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file_path)
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read the CSV file
    print(f"Reading CSV file: {input_csv_path}")
    df = pd.read_csv(input_csv_path)
    
    # Validate the target column exists
    if target_column not in df.columns:
        raise ValueError(f"Column '{target_column}' not found in the CSV file. Available columns: {list(df.columns)}")
    
    # Extract the target column values
    values = df[target_column].values
    print(f"Original data length: {len(values)}")
    
    # Handle the case where we have 8759 values and need 8760
    if len(values) == 8759:
        # Add the missing value using smart indexing
        # Since this is a yearly cycle, the next value should be the first value
        missing_value = values[0]  # Smart indexing: next value in cycle
        values = np.append(values, missing_value)
        print(f"Added missing value: {missing_value} (following the yearly cycle pattern)")
    elif len(values) != 8760:
        # Handle other cases where we don't have exactly 8760 values
        if len(values) < 8760:
            # Extend by repeating the pattern
            needed = 8760 - len(values)
            extension = []
            for i in range(needed):
                extension.append(values[i % len(values)])
            values = np.append(values, extension)
            print(f"Extended data from {len(values) - needed} to {len(values)} values using pattern repetition")
        else:
            # Truncate to 8760 values
            values = values[:8760]
            print(f"Truncated data to 8760 values")
    
    print(f"Final data length: {len(values)}")
    
    # Calculate the sum of the original values
    original_sum = np.sum(values)
    print(f"Original sum: {original_sum}")
    
    # Normalize to sum to 1/3600
    target_sum = 1.0 / 3600.0
    normalized_values = values * (target_sum / original_sum)
    
    # Verify the normalization
    final_sum = np.sum(normalized_values)
    print(f"Normalized sum: {final_sum}")
    print(f"Target sum: {target_sum}")
    print(f"Difference: {abs(final_sum - target_sum)}")
    
    # Save the normalized values (no headers, no timestamps, just the values)
    np.savetxt(output_file_path, normalized_values, delimiter=',', fmt='%.10f')
    
    print(f"Normalized curve saved to: {output_file_path}")
    return output_file_path


def main(input_csv_path=None, output_file_path=None):
    """
    Main function to handle command line arguments, parameters, or interactive input.
    """
    
    # If parameters are provided, use them
    if input_csv_path and output_file_path:
        pass  # Use the provided parameters
    # Check if command line arguments are provided
    elif len(sys.argv) == 3:
        input_csv_path = sys.argv[1]
        output_file_path = sys.argv[2]
    else:
        # Interactive input
        print("CSV Curve Normalizer")
        print("=" * 50)
        
        # Get input file path
        input_csv_path = input("Enter the path to the input CSV file: ").strip()
        if input_csv_path.startswith('"') and input_csv_path.endswith('"'):
            input_csv_path = input_csv_path[1:-1]  # Remove quotes if present
        
        # Get output file path
        output_file_path = input("Enter the full path to the output file (including filename): ").strip()
        if output_file_path.startswith('"') and output_file_path.endswith('"'):
            output_file_path = output_file_path[1:-1]  # Remove quotes if present
    
    try:
        # Process the curve
        output_file = process_curve(input_csv_path, output_file_path)
        print(f"\nSuccess! Processed file saved as: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main(
        input_csv_path="data/nl/2023/13_curves/input/households hot water/2022_W2H_Single_familiy_households_hot_water_demand.csv", 
        output_file_path="data/nl/2023/13_curves/output/households_hot_water.csv"
    )