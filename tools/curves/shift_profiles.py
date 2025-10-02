#!/usr/bin/env python3
"""
Flexible Profile Day Shifter
Converts yearly hourly profiles from any starting day to any target day.

Usage:
    python shift_profiles.py --from tuesday --to sunday --input input/ --output output/
"""

import argparse
import os
import sys
from pathlib import Path
import pandas as pd


def calculate_day_offset(from_day, to_day):
    """
    Calculate hour offset needed to shift from source day to target day.
    
    Args:
        from_day (str): Source day name (case-insensitive)
        to_day (str): Target day name (case-insensitive)
    
    Returns:
        int: Hour offset to reach first occurrence of target day from source day start
    
    Raises:
        ValueError: If day names are invalid
    """
    # Define valid days and their positions (0 = Sunday, 1 = Monday, etc.)
    days_map = {
        'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3,
        'thursday': 4, 'friday': 5, 'saturday': 6
    }
    
    # Normalize input
    from_day = from_day.lower().strip()
    to_day = to_day.lower().strip()
    
    # Validate day names
    if from_day not in days_map:
        raise ValueError(f"Invalid source day: '{from_day}'. Must be one of: {list(days_map.keys())}")
    if to_day not in days_map:
        raise ValueError(f"Invalid target day: '{to_day}'. Must be one of: {list(days_map.keys())}")
    
    # Get day positions
    from_pos = days_map[from_day]
    to_pos = days_map[to_day]
    
    # Calculate days difference (positive = forward, negative = backward)
    day_diff = (to_pos - from_pos) % 7
    
    # Convert to hours (24 hours per day)
    hour_offset = day_diff * 24
    
    return hour_offset


def shift_profile_flexible(df, hour_offset):
    """
    Shift profile by specified hour offset using 48-hour block logic.
    
    Args:
        df (pd.Series or pd.DataFrame): Input profile data
        hour_offset (int): Hours to shift forward to reach target day
    
    Returns:
        pd.Series or pd.DataFrame: Shifted profile maintaining original structure
    """
    # Create a copy to avoid modifying the original
    shifted_df = df.copy()
    
    # Handle Series case
    if isinstance(shifted_df, pd.Series):
        # If index is datetime, shift by calculated offset
        if pd.api.types.is_datetime64_any_dtype(shifted_df.index):
            shifted_df.index = shifted_df.index - pd.Timedelta(hours=hour_offset)
        else:
            # For Series without datetime: apply shifting logic
            if hour_offset == 0:
                return shifted_df  # No shift needed
            
            # Find the target day-pair start position
            target_start = hour_offset
            
            # Copy target day + next day (48 hours) from the calculated position
            target_block = shifted_df.iloc[target_start:target_start + 48].copy()
            
            # Keep all original data but remove last 48 hours to maintain year length
            remaining_data = shifted_df.iloc[:-48]
            
            # Final combination: target block first, then remaining data
            shifted_values = pd.concat([target_block, remaining_data])
            
            # Create new series with proper index
            shifted_df = pd.Series(shifted_values.values, index=range(len(shifted_values)))
    
    # Handle DataFrame case
    else:
        # If index is datetime, shift by calculated offset
        if pd.api.types.is_datetime64_any_dtype(shifted_df.index):
            shifted_df.index = shifted_df.index - pd.Timedelta(hours=hour_offset)
        
        # If there's a datetime column, shift it
        elif any(pd.api.types.is_datetime64_any_dtype(shifted_df[col]) for col in shifted_df.columns):
            for col in shifted_df.columns:
                if pd.api.types.is_datetime64_any_dtype(shifted_df[col]):
                    shifted_df[col] = shifted_df[col] - pd.Timedelta(hours=hour_offset)
        
        # Handle DataFrame without datetime index
        else:
            if hour_offset == 0:
                return shifted_df  # No shift needed
            
            # Apply same logic to each column
            for col in shifted_df.columns:
                col_data = shifted_df[col]
                
                # Find target day start position
                target_start = hour_offset
                
                # Copy target day + next day (48 hours)
                target_block = col_data.iloc[target_start:target_start + 48].copy()
                
                # Keep all original data but remove last 48 hours
                remaining_data = col_data.iloc[:-48]
                
                # Final combination: target block first, then remaining data
                shifted_values = pd.concat([target_block, remaining_data])
                shifted_df[col] = shifted_values.values
    
    return shifted_df


def normalize_profile(profile, target_sum=1/3600):
    """
    Normalize profile to sum to target_sum.
    
    Args:
        profile (pd.Series or pd.DataFrame): Profile data to normalize
        target_sum (float): Target sum for normalization (default: 1/3600)
    
    Returns:
        pd.Series or pd.DataFrame: Normalized profile
    """
    normalized = profile.copy()
    
    if isinstance(profile, pd.Series):
        current_sum = profile.sum()
        if current_sum > 0:
            normalized = profile * (target_sum / current_sum)
    else:
        # For DataFrame, normalize each column
        for col in profile.columns:
            current_sum = profile[col].sum()
            if current_sum > 0:
                normalized[col] = profile[col] * (target_sum / current_sum)
    
    return normalized


def validate_profile_length(profile, expected_length=8760):
    """
    Validate that profile has expected number of hours.
    
    Args:
        profile (pd.Series or pd.DataFrame): Profile to validate
        expected_length (int): Expected number of hours (default: 8760 for yearly)
    
    Raises:
        ValueError: If profile length doesn't match expected length
    """
    actual_length = len(profile)
    if actual_length != expected_length:
        raise ValueError(
            f"Profile length mismatch: expected {expected_length} hours, "
            f"got {actual_length} hours"
        )


def process_csv_file(file_path, hour_offset, normalize=True):
    """
    Process a single CSV file with shifting and optional normalization.
    
    Args:
        file_path (Path): Path to CSV file
        hour_offset (int): Hour offset for shifting
        normalize (bool): Whether to normalize the profile
    
    Returns:
        pd.Series: Processed profile
    
    Raises:
        ValueError: If file processing fails
    """
    try:
        # Read the profile as a DataFrame first, then convert to Series
        df_temp = pd.read_csv(file_path, header=None)
        
        # Handle both single and multi-column CSVs
        if df_temp.shape[1] == 1:
            profile = df_temp.iloc[:, 0]  # Convert single column DataFrame to Series
        else:
            profile = df_temp  # Keep as DataFrame for multi-column
        
        # Validate profile length
        validate_profile_length(profile)
        
        # Shift the profile
        shifted_profile = shift_profile_flexible(profile, hour_offset)
        
        # Normalize if requested
        if normalize:
            shifted_profile = normalize_profile(shifted_profile)
        
        return shifted_profile
        
    except Exception as e:
        raise ValueError(f"Failed to process {file_path.name}: {str(e)}")


def main():
    """CLI interface and file processing."""
    parser = argparse.ArgumentParser(
        description="Shift yearly transport profiles from any day to any other day",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python shift_profiles.py --from tuesday --to sunday
  python shift_profiles.py --from monday --to friday --input transport_data/ --output results/
  python shift_profiles.py --from saturday --to wednesday --normalize
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--from', dest='from_day', required=True,
        help='Source day name (monday, tuesday, wednesday, thursday, friday, saturday, sunday)'
    )
    parser.add_argument(
        '--to', dest='to_day', required=True,
        help='Target day name (monday, tuesday, wednesday, thursday, friday, saturday, sunday)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--input', dest='input_dir', default='input',
        help='Input directory containing CSV files (default: input)'
    )
    parser.add_argument(
        '--output', dest='output_dir', default='output',
        help='Output directory for shifted CSV files (default: output)'
    )
    parser.add_argument(
        '--normalize', action='store_true', default=True,
        help='Normalize profiles to sum to 1/3600 (default: True)'
    )
    parser.add_argument(
        '--prefix', default='',
        help='Prefix for output filenames (default: no prefix)'
    )
    
    args = parser.parse_args()
    
    try:
        # Calculate hour offset
        hour_offset = calculate_day_offset(args.from_day, args.to_day)
        print(f"Shifting profiles from {args.from_day.title()} to {args.to_day.title()}")
        print(f"Hour offset: {hour_offset} hours")
        
        # Validate input directory
        input_path = Path(args.input_dir)
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory does not exist: {input_path}")
        if not input_path.is_dir():
            raise NotADirectoryError(f"Input path is not a directory: {input_path}")
        
        # Create output directory
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get all CSV files from the input directory
        csv_files = list(input_path.glob('*.csv'))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in directory: {input_path}")
        
        print(f"Found {len(csv_files)} CSV files to process")
        
        # Process each profile file
        processed_count = 0
        for csv_file in csv_files:
            try:
                # Process the file
                shifted_profile = process_csv_file(csv_file, hour_offset, args.normalize)
                
                # Save the shifted profile with original filename
                output_filename = csv_file.name if not args.prefix else f"{args.prefix}{csv_file.name}"
                output_file_path = output_path / output_filename
                
                # Save based on data type
                if isinstance(shifted_profile, pd.Series):
                    shifted_profile.to_csv(output_file_path, header=False, index=False)
                else:
                    shifted_profile.to_csv(output_file_path, header=False, index=False)
                
                print(f"✓ Processed and saved: {csv_file.name} -> {output_filename}")
                processed_count += 1
                
            except Exception as e:
                print(f"✗ Error processing {csv_file.name}: {str(e)}", file=sys.stderr)
                continue
        
        # Summary
        print(f"\nCompleted: {processed_count}/{len(csv_files)} files processed successfully")
        if args.normalize:
            print("Profiles were normalized to sum to 1/3600")
        
        if processed_count == 0:
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()