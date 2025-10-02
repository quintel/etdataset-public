#!/usr/bin/env python3
"""
Energy Profile Data Processor

This script processes energy profile data (electricity and gas curves) from CSV files,
normalizes the data, and creates final demand curves for various energy usage categories.

Usage:
    python energy_processor.py

Script location: etdataset/tools/curves/
Input files expected: etdataset/data/nl/2023/13_curves/heat and electricity/input/
    - Energiedatawijzer_profielen_elektriciteit.csv
    - Energiedatawijzer_profielen_aardgas.csv

Output directory: etdataset/data/nl/2023/13_curves/output/
    - Final demand curve CSV files (headerless)
"""

import pandas as pd
import os
import sys
from pathlib import Path


def get_project_paths():
    """
    Get the correct input and output paths relative to the script location.
    Script is in: etdataset/tools/curves/
    Input is in: etdataset/data/nl/2023/13_curves/input/
    Output is in: etdataset/data/nl/2023/13_curves/output/
    """
    # Get the script directory (etdataset/tools/curves/)
    script_dir = Path(__file__).parent
    
    # Navigate to etdataset root (go up 2 levels: curves -> tools -> etdataset)
    etdataset_root = script_dir.parent.parent
    
    # Define input and output paths
    input_dir = etdataset_root / "data" / "nl" / "2023" / "13_curves" / "input" / "heat and electricity" 
    output_dir = etdataset_root / "data" / "nl" / "2023" / "13_curves" / "output"
    
    return input_dir, output_dir


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist."""
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory ready: {output_dir}")


def normalize_energy_columns(df, exclude_col='Time'):
    """
    Normalize all columns except the specified exclude column so that their sum equals 1/3600.
    
    Parameters:
    df: pandas DataFrame with energy data
    exclude_col: column name to exclude from normalization (default: 'Time')
    
    Returns:
    pandas DataFrame with normalized columns
    """
    # Create a copy to avoid modifying the original dataframe
    normalized_df = df.copy()
    
    # Get all columns except the exclude column
    energy_cols = [col for col in df.columns if col != exclude_col]
    
    # Normalize each energy column so its sum equals 1/3600
    target_sum = 1/3600
    for col in energy_cols:
        column_sum = df[col].sum()
        if column_sum > 0:  # Avoid division by zero
            normalized_df[col] = df[col] * target_sum / column_sum
            print(f"Normalizing {col}: {column_sum} -> {normalized_df[col].sum()}")
        else:
            print(f"Warning: Column {col} has zero sum, skipping normalization")
    
    return normalized_df

def process_electricity_data(input_path):
    """
    Process electricity profile data and return normalized curves.
    
    Parameters:
    input_path: Path to the electricity CSV file
    
    Returns:
    pandas DataFrame with processed and normalized electricity data
    """
    print("Processing electricity data...")
    
    try:
        # Read the raw electricity curves
        raw_electricity_curves = pd.read_csv(input_path, sep=",")
        print(f"Loaded electricity data with shape: {raw_electricity_curves.shape}")
        
        # Convert numeric columns to float first (excluding Time column)
        numeric_cols = raw_electricity_curves.columns[1:]
        raw_electricity_curves[numeric_cols] = raw_electricity_curves[numeric_cols].astype(float)
        
        # Group every 4 rows and sum them, keeping every 4th Time value
        hourly_elektriciteit = raw_electricity_curves.groupby(raw_electricity_curves.index // 4).agg({
            'Time': 'first',  # Keep the first time value of each group
            **{col: 'sum' for col in numeric_cols}  # Sum all numeric columns
        }).reset_index(drop=True)
        
        print(f"Grouped to hourly data with shape: {hourly_elektriciteit.shape}")
        
        # Set Time as index temporarily for processing
        hourly_elektriciteit.set_index('Time', inplace=True)
        
        # Normalize the energy columns
        elektriciteit_normalized = normalize_energy_columns(hourly_elektriciteit)
        
        # Reset index
        elektriciteit_normalized.reset_index(inplace=True, drop=True)
        
        print("Electricity data processed and normalized successfully.")
        return elektriciteit_normalized
        
    except FileNotFoundError:
        print(f"Error: Could not find electricity input file at {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing electricity data: {str(e)}")
        sys.exit(1)


def process_gas_data(input_path):
    """
    Process gas profile data and return normalized curves.
    
    Parameters:
    input_path: Path to the gas CSV file
    
    Returns:
    pandas DataFrame with processed gas data
    """
    print("Processing gas data...")
    
    try:
        # Read the raw gas curves
        raw_gas_curves = pd.read_csv(input_path, sep=",")
        print(f"Loaded gas data with shape: {raw_gas_curves.shape}")
        
        # Get columns that contain 'TOP' in their name
        top_columns = [col for col in raw_gas_curves.columns if 'TOP' in col]
        print(f"Found TOP columns: {top_columns}")
        
        # Convert TOP columns to numeric (they're currently object type)
        for col in top_columns:
            raw_gas_curves[col] = pd.to_numeric(raw_gas_curves[col], errors='coerce')
        
        # Normalize each TOP column so its sum equals 1/3600
        target_sum = 1/3600
        for col in top_columns:
            column_sum = raw_gas_curves[col].sum()
            if column_sum > 0:  # Avoid division by zero
                raw_gas_curves[col] = raw_gas_curves[col] * target_sum / column_sum
            print(column_sum, target_sum)

        print("Gas data processed and normalized successfully.")
        return raw_gas_curves
        
    except FileNotFoundError:
        print(f"Error: Could not find gas input file at {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing gas data: {str(e)}")
        sys.exit(1)


def create_final_demand_curves(elektriciteit_normalized, raw_gas_curves, output_dir):
    """
    Create final demand curves and save them to the output directory.
    
    Parameters:
    elektriciteit_normalized: DataFrame with normalized electricity data
    raw_gas_curves: DataFrame with processed gas data
    output_dir: Path to output directory
    """
    print("Creating final demand curves...")
    
    # Define the curve mapping dictionary
    curve_dictionary = {
        'E3A': ('agriculture_electricity', 'buildings_appliances'),
        'E1A': ('households_appliances'),
        'G2C': ('industry_other_heat',),
        'E3D': ('industry_ict', 'industry_other_electricity')
    }
    
    try:
        total_curves_created = 0
        
        for curve_code, curve_names in curve_dictionary.items():
            if curve_code.startswith('E'):  # Electricity curves
                for curve_name in curve_names:
                    output_path = output_dir / f'{curve_name}.csv'
                    elektriciteit_normalized[[curve_code]].to_csv(
                        output_path, index=False, header=False
                    )
                    total_curves_created += 1
                    print(f"  Created: {curve_name}.csv (from {curve_code})")
                    
            else:  # Gas curves
                for curve_name in curve_names:
                    output_path = output_dir / f'{curve_name}.csv'
                    raw_gas_curves[[f'{curve_code}_TOP']].to_csv(
                        output_path, index=False, header=False
                    )
                    total_curves_created += 1
                    print(f"  Created: {curve_name}.csv (from {curve_code}_TOP)")
        
        print(f"\nSuccessfully created {total_curves_created} demand curve files.")
        
        # Print summary of created files by category
        print("\nFinal demand curves by category:")
        electricity_curves = []
        gas_curves = []
        
        for curve_code, curve_names in curve_dictionary.items():
            if curve_code.startswith('E'):
                electricity_curves.extend(curve_names)
            else:
                gas_curves.extend(curve_names)
        
        print(f"  Electricity-based curves ({len(electricity_curves)}): {', '.join(electricity_curves)}")
        print(f"  Gas-based curves ({len(gas_curves)}): {', '.join(gas_curves)}")
            
    except Exception as e:
        print(f"Error creating demand curves: {str(e)}")
        sys.exit(1)


def main():
    """Main execution function."""
    print("=== Energy Profile Data Processor ===")
    print("Generating final demand curves only...\n")
    
    # Get input and output paths
    input_dir, output_dir = get_project_paths()
    
    # Define input file paths
    electricity_path = input_dir / "Energiedatawijzer_profielen_elektriciteit.csv"
    gas_path = input_dir / "Energiedatawijzer_profielen_aardgas.csv"
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Check if input files exist
    if not electricity_path.exists():
        print(f"Error: Electricity input file not found at {electricity_path}")
        print("Please ensure the input directory contains the required CSV file.")
        sys.exit(1)
        
    if not gas_path.exists():
        print(f"Error: Gas input file not found at {gas_path}")
        print("Please ensure the input directory contains the required CSV file.")
        sys.exit(1)
    
    # Create output directory
    create_output_directory(output_dir)
    
    # Process electricity data
    elektriciteit_normalized = process_electricity_data(electricity_path)
    
    # Process gas data
    raw_gas_curves = process_gas_data(gas_path)
    
    # Create final demand curves
    create_final_demand_curves(elektriciteit_normalized, raw_gas_curves, output_dir)
    
    print(f"\n=== Processing Complete ===")
    print(f"All final demand curves have been successfully created in:")
    print(f"{output_dir}")
    print("\nThese curves are ready for use in the energy transition dataset.")


if __name__ == "__main__":
    main()