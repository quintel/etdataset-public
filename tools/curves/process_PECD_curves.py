import pandas as pd
import os
import shutil
from pathlib import Path

# Country code mapping: Excel column name -> folder name(s)
# Most entries map to a single folder, but UK maps to multiple folders
COUNTRY_MAPPING = {
    'NL': ['nl'],  # Special case: lowercase
    'nl': ['nl'],  # In case it's already lowercase in Excel
    'AT': ['AT_austria'],
    'BE': ['BE_belgium'],
    'BG': ['BG_bulgaria'],
    'CH': ['CH_switzerland'],
    'CY': ['CY_cyprus'],
    'CZ': ['CZ_czechia'],
    'DE': ['DE_germany','EU27_european_union'],
    'DK': ['DK_denmark'],
    'EE': ['EE_estonia'],
    'EL': ['EL_greece'],
    'ES': ['ES_spain'],
    'FI': ['FI_finland'],
    'FR': ['FR_france'],
    'GB': ['GB_great_britain'],
    'HR': ['HR_croatia'],
    'HU': ['HU_hungary'],
    'IE': ['IE_ireland'],
    'IT': ['IT_italy'],
    'LT': ['LT_lithuania'],
    'LU': ['LU_luxembourg'],
    'LV': ['LV_latvia'],
    'MT': ['MT_malta'],
    'NO': ['NO_norway'],
    'PL': ['PL_poland'],
    'PT': ['PT_portugal'],
    'RO': ['RO_romania'],
    'RS': ['RS_serbia'],
    'SE': ['SE_sweden'],
    'SI': ['SI_slovenia'],
    'SK': ['SK_slovakia'],
    'UK': ['UK_united_kingdom', 'GB_great_britain', 'UKNI01_northern_ireland'],  # Special: UK maps to 3 outputs
}

def process_solar_profiles(excel_files, input_folder='../../input', output_base_dir='../../data'):
    """
    Process Solar PV profile Excel files and split them into normalized curves.

    Parameters:
    -----------
    excel_files : dict
        Dictionary mapping technology names to Excel file names
        Example: {'technology1': 'file1.xlsx', 'technology2': 'file2.xlsx'}
    input_folder : str
        Directory containing the input Excel files (default: 'input')
    output_base_dir : str
        Base directory for output files (default: 'data')
    """

    for technology, file_name in excel_files.items():
        # Construct full file path
        file_path = os.path.join(input_folder, file_name)
        print(f"\nProcessing technology: {technology}")
        print(f"Reading file: {file_path}")

        try:
            # Read all sheets from the Excel file
            excel_file = pd.ExcelFile(file_path)

            # Process each sheet (year)
            for sheet_name in excel_file.sheet_names:
                year = sheet_name.strip()
                print(f"  Processing year: {year}")

                # Read the sheet
                df = pd.read_excel(file_path, sheet_name=sheet_name)

                # Get country codes (all columns except the first one which is timestamp)
                excel_countries = df.columns[1:].tolist()

                # Store AL curve for solar_csp to use for Greece if needed
                al_curve_normalized = None
                if technology == 'solar_csp' and 'AL' in excel_countries:
                    al_curve = df['AL'].values
                    al_curve_sum = al_curve.sum()
                    if al_curve_sum > 0:
                        al_curve_normalized = al_curve / (al_curve_sum * 3600)
                        print(f"    Stored AL curve for potential use with Greece")

                # Process each country
                for country_column in excel_countries:
                    country_code = str(country_column).strip()

                    # Check if this country is in our mapping (filter out unwanted countries)
                    if country_code not in COUNTRY_MAPPING:
                        print(f"    Skipping country: {country_code} (not in required list)")
                        continue

                    # Only process 2019 for all countries except NL
                    if country_code not in ['NL', 'nl'] and year != '2019':
                        print(f"    Skipping {country_code} for year {year} (only processing 2019 for non-NL countries)")
                        continue

                    # Get the folder name(s) for this country (can be multiple for UK)
                    folder_names = COUNTRY_MAPPING[country_code]
                    print(f"    Processing country: {country_code} -> {', '.join(folder_names)}")

                    # Extract the curve for this country
                    curve = df[country_column].values

                    # Normalize the curve so that it sums to 1/3600
                    # Formula: normalized = original / (sum * 3600)
                    # This ensures: sum(normalized) = 1/3600
                    curve_sum = curve.sum()
                    if curve_sum == 0:
                        print(f"      WARNING: Curve sum is zero for {country_code}, skipping...")
                        continue
                    normalized_curve = curve / (curve_sum * 3600)

                    # Save to each mapped folder (usually just one, but UK maps to three)
                    for folder_name in folder_names:
                        # Create output directory structure using the mapped folder name
                        output_dir = Path(output_base_dir) / folder_name / year / 'curves'
                        output_dir.mkdir(parents=True, exist_ok=True)

                        # Create output file path
                        output_file = output_dir / f"{technology}.csv"

                        # Save as CSV with single column, no header
                        pd.DataFrame(normalized_curve).to_csv(
                            output_file,
                            index=False,
                            header=False
                        )

                        print(f"      Saved to: {output_file}")

                # Special case: For solar_csp, if Greece (EL) doesn't have data, use AL curve
                # Only process for 2019 (following the same rule as other non-NL countries)
                if technology == 'solar_csp' and al_curve_normalized is not None and 'EL' not in excel_countries and year == '2019':
                    print(f"    Special case: Using AL curve for Greece (EL) for solar_csp")
                    for folder_name in COUNTRY_MAPPING['EL']:
                        output_dir = Path(output_base_dir) / folder_name / year / 'curves'
                        output_dir.mkdir(parents=True, exist_ok=True)
                        output_file = output_dir / f"{technology}.csv"

                        pd.DataFrame(al_curve_normalized).to_csv(
                            output_file,
                            index=False,
                            header=False
                        )
                        print(f"      Saved AL curve to Greece: {output_file}")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue

    print("\n✓ Processing complete!")


def cleanup_non_2019_folders(output_base_dir='../../data'):
    """
    Remove year folders that are not 2019 for all countries except NL.

    Parameters:
    -----------
    output_base_dir : str
        Base directory for output files (default: 'data')
    """
    print("\n🧹 Cleaning up non-2019 year folders for EU countries...")

    # Get all unique folder names except NL
    all_folders = set()
    for country_code, folder_names in COUNTRY_MAPPING.items():
        if country_code not in ['NL', 'nl']:
            all_folders.update(folder_names)

    base_path = Path(output_base_dir)

    for folder_name in all_folders:
        folder_path = base_path / folder_name

        if not folder_path.exists():
            continue

        # Get all year folders in this country folder
        for year_folder in folder_path.iterdir():
            if year_folder.is_dir() and year_folder.name != '2019':
                try:
                    shutil.rmtree(year_folder)
                    print(f"  Removed: {year_folder}")
                except Exception as e:
                    print(f"  Error removing {year_folder}: {str(e)}")

    print("✓ Cleanup complete!")


def main():
    """
    Main function to run the script.
    Modify the excel_files dictionary to match your file names and technology names.
    """

    # Define your input and output folders (relative to tools/subfolder/ directory)
# Define your input and output folders (running from project root)
    input_folder = 'source_analyses/EU27_european_union/2019/curves'
    output_folder = 'data'

    # Define your Excel files here
    # Replace with your actual file names and technology names
    excel_files = {
        'solar_pv_on_roof_households': 'Solar generation capacity factor - Residential rooftop.xlsx',
        'solar_pv_on_roof_buildings': 'Solar generation capacity factor - Industrial rooftop.xlsx',
        'solar_pv_on_land': 'Solar generation capacity factor - Utility-scale fixed.xlsx',
        'solar_pv_offshore': 'Solar generation capacity factor - Utility-scale fixed.xlsx',
        'solar_csp': 'Concentrated Solar Power - storage_0_hours_preDispatch.xlsx',
    }

    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        print(f"Please create the folder or update the 'input_folder' variable.")
        return

    # Check if files exist
    missing_files = []
    for file_name in excel_files.values():
        file_path = os.path.join(input_folder, file_name)
        if not os.path.exists(file_path):
            missing_files.append(file_name)

    if missing_files:
        print(f"Warning: The following files were not found in '{input_folder}/':")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease add the files to the input folder or update the 'excel_files' dictionary.")
        return

    # Process the files
    process_solar_profiles(excel_files, input_folder=input_folder, output_base_dir=output_folder)

    # Clean up non-2019 folders for EU countries
    cleanup_non_2019_folders(output_base_dir=output_folder)


if __name__ == "__main__":
    main()
