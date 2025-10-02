import pandas as pd
import numpy as np
import xlwings as xw
from pathlib import Path


def extract_most_recent_km_data(file_path, sheet_name="Data", target_year=2023):
    """
    Extract Klimaatmonitor data and automatically get the most recent year for each municipality and variable
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the Klimaatmonitor Excel file
    sheet_name : str, optional
        Name of the sheet containing the data (default: "Data")
    target_year : int, optional
        The target year for the output columns (default: 2023)
        
    Returns:
    --------
    pandas.DataFrame
        Processed DataFrame with most recent year data for each municipality/variable combination
    """
    
    # 1. Load the Klimaatmonitor data
    wb_km = xw.Book(str(file_path))
    ws_km_data = wb_km.sheets[sheet_name]
    
    df_data = pd.DataFrame(ws_km_data.used_range.value)
    df_data.columns = df_data.iloc[0]
    df_data = df_data[1:]
    df_data = df_data.set_index(df_data.columns[1])  # Set municipality code as index
    
    # Remove the 'Gebieden' column if it exists
    if "Gebieden" in df_data.columns:
        df_data = df_data.drop(columns=["Gebieden"])
    
    wb_km.close()
    
    # 2. Process the data to extract most recent years
    df_result = pd.DataFrame(index=df_data.index)
    
    # Get all columns that have year suffixes
    all_columns = df_data.columns
    
    # Group columns by variable name (remove _YYYY suffix)
    variable_groups = {}
    non_year_columns = []
    
    for col in all_columns:
        # Check if column ends with a year pattern
        if col.endswith(('_2020', '_2021', '_2022', '_2023')):
            base_var = col.rsplit('_', 1)[0]
            year_val = int(col.rsplit('_', 1)[1])
            
            if base_var not in variable_groups:
                variable_groups[base_var] = []
            variable_groups[base_var].append((col, year_val))
        else:
            # Keep non-year columns as-is
            non_year_columns.append(col)
    
    # Copy non-year columns directly
    for col in non_year_columns:
        df_result[col] = df_data[col]
    
    print(f"Processing {len(variable_groups)} variable groups for most recent year extraction...")
    
    # For each variable group, extract the most recent available data
    for base_var, year_columns in variable_groups.items():
        # Sort by year (most recent first)
        year_columns.sort(key=lambda x: x[1], reverse=True)
        
        # Create result column with target year suffix
        result_col = f"{base_var}_{target_year}"
        df_result[result_col] = pd.NA
        
        # Track statistics
        municipalities_filled = 0
        year_usage = {2020: 0, 2021: 0, 2022: 0, 2023: 0}
        
        # For each municipality, find the most recent available data
        for municipality in df_data.index:
            for col, col_year in year_columns:
                value = df_data.loc[municipality, col]
                
                # Check if value is valid (not NaN, not '?', not empty)
                if pd.notna(value) and value != '?' and value != '':
                    df_result.loc[municipality, result_col] = value
                    municipalities_filled += 1
                    year_usage[col_year] += 1
                    break  # Stop at first valid value (most recent)
        
        # Print statistics for this variable
        total_municipalities = len(df_data.index)
        print(f"  {base_var}: {municipalities_filled}/{total_municipalities} municipalities filled")
        if municipalities_filled > 0:
            year_breakdown = ", ".join([f"{year}: {count}" for year, count in year_usage.items() if count > 0])
            print(f"    Year usage: {year_breakdown}")
    
    return df_result


def load_km_metadata(file_path, sheet_name="Onderwerp Informatie"):
    """
    Load Klimaatmonitor metadata from Excel file
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the Klimaatmonitor Excel file
    sheet_name : str, optional
        Name of the metadata sheet (default: "Onderwerp Informatie")
        
    Returns:
    --------
    pandas.DataFrame
        Metadata DataFrame with topic information
    """
    wb_km = xw.Book(str(file_path))
    ws_km_meta = wb_km.sheets[sheet_name]
    
    df_meta = pd.DataFrame(ws_km_meta.used_range.value)
    df_meta.columns = df_meta.iloc[0]
    df_meta = df_meta[1:]
    df_meta = df_meta.set_index(df_meta.columns[0])
    
    wb_km.close()
    
    return df_meta


def load_km_raw_data(file_path, sheet_name="Data"):
    """
    Load raw Klimaatmonitor data from Excel file without processing
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the Klimaatmonitor Excel file
    sheet_name : str, optional
        Name of the data sheet (default: "Data")
        
    Returns:
    --------
    pandas.DataFrame
        Raw data DataFrame
    """
    wb_km = xw.Book(str(file_path))
    ws_km_data = wb_km.sheets[sheet_name]
    
    df_data = pd.DataFrame(ws_km_data.used_range.value)
    df_data.columns = df_data.iloc[0]
    df_data = df_data[1:]
    df_data = df_data.set_index(df_data.columns[1])
    
    # Remove the 'Gebieden' column if it exists
    if "Gebieden" in df_data.columns:
        df_data = df_data.drop(columns=["Gebieden"])
    
    wb_km.close()
    
    return df_data