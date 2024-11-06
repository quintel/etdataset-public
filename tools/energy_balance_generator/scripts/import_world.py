"""
This script reads world energy balance data from text files, filters the data based on
specified country and year, processes it into a structured CSV format, and saves
the result to an output folder.
The input folder should be an absolute path (e.g.): "/Users/User/Desktop/Secure Location".
The output folder should follow the structure: data/CO_Country/Year/energy_balance.

Usage:
    pipenv run import_world <COUNTRY> <YEAR> [input_folder] [output_folder]
    pipenv run import_world --list-countries [input_folder]

Example:
    pipenv run import_world SWITLAND 2019 "/Users/User/Desktop/Secure Location" ../../data/CH_switzerland/2019/energy_balance
    pipenv run import_world --list-countries ./data/input
"""

import argparse
import pandas as pd
import re
from pathlib import Path
import sys
import logging
import os
import yaml

from etm_tools.energy_balance_operations import Runner

CONVERSIONS = [
    'industry_ict',
    'industry_metal',
    'industry_chemical'
]

def process_wb(file, filtered_data, country, year):
    """
    Processes the energy balance data from a file, filtering by country, year, and unit.

    Args:
        file (file object): Open file object to read lines from.
        filtered_data (list): List to append filtered data to.
        country (str): Country code to filter by.
        year (int): Year to filter by.

    Returns:
        list: Updated list with filtered data.
    """
    pattern = r'\s+'
    for line in file:
        split_line = re.split(pattern, line.strip())
        split_line = ["" if val.lower() in ["x", ".."] else val for val in split_line]

        if (split_line[0] == country and
            split_line[2] == str(year) and
            split_line[4].upper() == "TJ"):
            filtered_data.append(split_line)
    return filtered_data


def load_raw_wb_from_txt(country, year, input_folder, output_folder):
    """
    Loads and processes raw energy balance data from text files, applies mappings,
    adds a total column, reorders columns and rows according to the YAML configuration,
    and saves the final DataFrame to a CSV file.

    Args:
        country (str): Country code to filter data by.
        year (int): Year to filter data by.
        input_folder (Path): Path to the input folder containing WORLDBIG2.txt.
        output_folder (Path): Path to the folder where the output CSV will be saved.

    Returns:
        None
    """
    filtered_data = []

    raw_files = [input_folder / "WORLDBIG1.txt", input_folder / "WORLDBIG2.txt"]

    # Check if at least one of the files exists
    if not any(raw_file.is_file() for raw_file in raw_files):
        logging.error(f"Neither WORLDBIG1.txt nor WORLDBIG2.txt exist in '{input_folder}'.")
        sys.exit(1)

    for raw_file in raw_files:
        if not raw_file.is_file():
            logging.warning(f"File '{raw_file}' does not exist. Skipping.")
            continue

        logging.info(f"Processing file: {raw_file}")
        with open(raw_file, 'r') as file:
            process_wb(file, filtered_data, country, year)

        if filtered_data:
            break # Data found, stop processing further files

    if not filtered_data:
        logging.error(f"No matching data found for country '{country}' and year '{year}' in available files.")
        sys.exit(1)

    columns = ['Country', 'world_code', 'Year', 'nrg_bal', 'Unit', 'Value']

    try:
        df = pd.DataFrame(filtered_data, columns=columns)
    except ValueError as e:
        logging.error(f"Error creating DataFrame: {e}")
        sys.exit(1)

    df.drop(['Country', 'Year', 'Unit'], axis=1, inplace=True)

    output_folder.mkdir(parents=True, exist_ok=True)

    filtered_long_csv = output_folder / 'intermediate_energy_balance_world_raw.encrypted.csv'
    df.to_csv(filtered_long_csv, index=False)

    df_pivot = df.pivot_table(
        index='nrg_bal',
        columns='world_code',
        values='Value',
        aggfunc='first'
    ).fillna(0.0)

    logging.info("Pivoted DataFrame saved.")

    filtered_wide_csv = output_folder / 'intermediate_energy_balance_world_wide.encrypted.csv'
    df_pivot.to_csv(filtered_wide_csv, index=True)
    logging.info(f"Filtered data saved to '{filtered_wide_csv}'.")

    flow_path = Path("config/flows_world_to_europe.csv").resolve()
    prod_path = Path("config/products_world_to_europe.csv").resolve()

    if not flow_path.is_file():
        logging.error(f"Flow mapping file '{flow_path}' does not exist.")
        sys.exit(1)
    if not prod_path.is_file():
        logging.error(f"Product mapping file '{prod_path}' does not exist.")
        sys.exit(1)

    flow_mapping = pd.read_csv(flow_path)
    df_flowed = apply_mappings(df_pivot, flow_mapping, 'flows')

    prod_mapping = pd.read_csv(prod_path)
    df_final = apply_mappings(df_flowed, prod_mapping, 'products')

    products, flows = load_yaml_config()

    columns_order = [product for product in products if product in df_final.columns]
    remaining_columns = [col for col in df_final.columns if col not in columns_order]
    df_final = df_final[columns_order + remaining_columns]

    flows_order = [flow for flow in flows if flow in df_final.index]
    remaining_flows = [idx for idx in df_final.index if idx not in flows_order]
    df_final = df_final.loc[flows_order + remaining_flows].abs()

    # Save the Europe format version of the EB pre-enrichment.
    pre_enriched_csv = output_folder / 'intermediate_energy_balance_europe.encrypted.csv'
    df_final.to_csv(pre_enriched_csv, index=True)

    # Enrich using the EUROSTAT_CONVERSIONS
    country_code = extract_country_code(output_folder)
    runner = Runner.load_from_df(df_final, country_code, year)
    runner.process(*CONVERSIONS)

def load_yaml_config():
    """
    Loads the YAML configuration file and extracts the products and flows
    under the 'energy_balance' section.

    Returns:
        tuple: Two lists containing the products and flows.
    """
    yaml_path = Path("config/eurostat.yml").resolve()
    if not yaml_path.is_file():
        logging.error(f"YAML configuration file '{yaml_path}' does not exist.")
        sys.exit(1)

    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    energy_balance = config.get('energy_balance', {})
    products = energy_balance.get('products', [])
    flows = energy_balance.get('flows', [])

    if not products or not flows:
        logging.error("No products or flows found in the 'energy_balance' section of the YAML file.")
        sys.exit(1)

    return products, flows

def list_countries(input_folder):
    """
    Lists all unique countries available in the text files.

    Args:
        input_folder (Path): Path to the input folder containing WORLDBIG1.txt and WORLDBIG2.txt.

    Returns:
        None
    """
    unique_countries = set()

    raw_files = [input_folder / 'WORLDBIG1.txt', input_folder / 'WORLDBIG2.txt']

    for raw_file in raw_files:
        if not raw_file.is_file():
            logging.warning(f"File '{raw_file}' does not exist. Skipping.")
            continue
        with open(raw_file, 'r') as file:
            for line in file:
                split_line = re.split(r'\s+', line.strip())
                unique_countries.add(split_line[0])

    logging.info("Available countries:")
    for country in sorted(unique_countries):
        print(country)

def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process energy balance data from text files."
    )
    parser.add_argument(
        'country',
        type=str,
        nargs='?',
        help="Country code to filter data by (e.g., SWITLAND)."
    )
    parser.add_argument(
        'year',
        type=int,
        nargs='?',
        help="Year to filter data by (e.g., 2023)."
    )
    parser.add_argument(
        'input_folder',
        type=str,
        help="Path to the input folder containing WORLDBIG1.txt and WORLDBIG2.txt."
    )
    parser.add_argument(
        'output_folder',
        type=str,
        nargs='?',
        default="output",
        help="Path to the folder where the output CSV will be saved."
    )
    parser.add_argument(
        '--list-countries',
        action='store_true',
        help="List all available countries in the input files."
    )
    return parser.parse_args()

def extract_country_code(output_folder):
    """
    Extracts the country code from the output_folder path.
    Assumes the path contains a segment like 'CH_switzerland' and extracts 'CH'.
    """
    # Iterate through the path parts to find the country code
    for part in output_folder.parts:
        # Look for a part that matches the pattern 'XX_something', where XX is the country code
        if '_' in part:
            country_code = part.split('_')[0].upper()
            if len(country_code) == 2:
                return country_code
    logging.error("Could not extract country code from output folder path.")
    sys.exit(1)

def apply_mappings(frame, mappings, axis):
    """
    Applies mappings to the DataFrame using the specified axis.

    Args:
        frame (pd.DataFrame): The DataFrame to apply mappings to.
        mappings (pd.DataFrame): The mappings DataFrame.
        axis (str): The axis to apply mappings on ('flows' or 'products').

    Returns:
        pd.DataFrame: The DataFrame after applying mappings.
    """
    result = frame.apply(pd.to_numeric, errors='coerce').fillna(0.0)
    applier = MappingApplier(result, mappings, axis)
    return applier.apply()


class MappingApplier:
    def __init__(self, result, mappings, axis):
        """
        Initializes the MappingApplier.

        Args:
            result (pd.DataFrame): The DataFrame to apply mappings to.
            mappings (pd.DataFrame): The mappings DataFrame.
            axis (str): The axis to apply mappings on ('flows' or 'products').
        """
        self.result = result
        self.mappings = mappings
        self.axis = axis

        if self.axis == "flows":
            self.target = self.result.index
            self.re_axis = "index"
        elif self.axis == "products":
            self.target = self.result.columns
            self.re_axis = "columns"
        else:
            raise ValueError("Axis must be 'flows' or 'products'")

        self.mapping_funcs = {
            'direct': self.apply_direct,
            'nettify': self.apply_nettify,
            'ignore': self.apply_ignore,
            'convert': self.apply_convert,
            'add': self.apply_add,
            'empty': self.apply_empty
        }

    def apply(self):
        """
        Applies the mappings to the DataFrame.

        Returns:
            pd.DataFrame: The DataFrame after applying mappings.
        """
        aggregate_mappings = self.mappings[self.mappings['mapping'] == 'aggregate']
        if not aggregate_mappings.empty:
            self.apply_aggregate(aggregate_mappings)

        remaining_mappings = self.mappings[self.mappings['mapping'] != 'aggregate']
        empty_mappings = remaining_mappings[remaining_mappings['mapping'] == 'empty']
        if not empty_mappings.empty:
            self.apply_empty(empty_mappings)

        other_mappings = remaining_mappings[remaining_mappings['mapping'] != 'empty']
        grouped_mappings = other_mappings.groupby('world_code')

        for world_code, group in grouped_mappings:
            mapping_type = group['mapping'].iloc[0]
            europe_labels = group['europe_label'].tolist()
            mapping_func = self.mapping_funcs.get(mapping_type)
            if mapping_func:
                mapping_func(world_code, europe_labels, group)
            else:
                logging.warning(f"Unknown mapping type '{mapping_type}' for world code '{world_code}'")
        return self.result

    def rename_label(self, world_code, europe_label):
        """
        Renames a label from world_code to europe_label in the DataFrame.

        Args:
            world_code (str): The original label.
            europe_label (str): The new label.
        """
        if world_code in self.target:
            self.result.rename({world_code: europe_label}, axis=self.re_axis, inplace=True)
            if self.axis == "flows":
                self.target = self.result.index
            else:
                self.target = self.result.columns

    def apply_direct(self, world_code, europe_labels, group):
        """
        Applies a 'direct' mapping by renaming the world_code to europe_label.

        Args:
            world_code (str): The original code.
            europe_labels (list): List containing the new label.
            group (pd.DataFrame): The group of mappings for this world_code.
        """
        if world_code in self.target:
            self.rename_label(world_code, europe_labels[0])

    def apply_nettify(self, world_code, europe_labels, group):
        """
        Applies a 'nettify' mapping, splitting values into positive (imports) and negative (exports),
        while accounting for special cases from the SplitNegativeConverter's SPECIAL_CASES.

        Args:
            world_code (str): The original code.
            europe_labels (list): List containing the new labels for import and export.
            group (pd.DataFrame): The group of mappings for this world_code.
        """
        nettify_rows = group[group['mapping'] == 'nettify']

        if len(nettify_rows) != 2:
            logging.warning(f"Nettify mapping for '{world_code}' must have exactly two rows - ignoring")
            self.apply_ignore(world_code, europe_labels, group)
            return

        export_row = nettify_rows.iloc[0]
        import_row = nettify_rows.iloc[1]  # import row is negative values

        import_label = import_row['europe_label']
        export_label = export_row['europe_label']

        # Nettify process: Split values into positive (export) and negative (import)
        if world_code in self.target:
            if self.axis == "flows":
                values = self.result.loc[world_code]
                self.result.loc[import_label] = self.result.get(import_label, 0) + values.clip(lower=0)
                self.result.loc[export_label] = self.result.get(export_label, 0) + (-values).clip(lower=0)
            else:
                values = self.result[world_code]
                self.result[import_label] = self.result.get(import_label, 0) + values.clip(lower=0)
                self.result[export_label] = self.result.get(export_label, 0) + (-values).clip(lower=0)

            # Drop the original world_code since it has been split
            self.result.drop(labels=world_code, axis=self.re_axis, inplace=True)

            # Update target index or columns accordingly
            if self.axis == "flows":
                self.target = self.result.index
            else:
                self.target = self.result.columns

    def apply_ignore(self, world_code, europe_labels, group):
        """
        Applies an 'ignore' mapping by dropping the world_code.

        Args:
            world_code (str): The code to drop.
            europe_labels (list): List containing the new label (not used here).
            group (pd.DataFrame): The group of mappings for this world_code.
        """
        if world_code in self.target:
            self.result.drop(labels=world_code, axis=self.re_axis, inplace=True)
            if self.axis == "flows":
                self.target = self.result.index
            else:
                self.target = self.result.columns

    def apply_convert(self, world_code, europe_labels, group):
        """
        Applies a 'convert' mapping by converting units and renaming the label.

        Args:
            world_code (str): The original code.
            europe_labels (list): List containing the new label.
            group (pd.DataFrame): The group of mappings for this world_code.
        """
        conversion_factor = 3.6  # GWh --> TJ
        if world_code in self.target:
            if self.axis == 'flows':
                self.result.loc[world_code] *= conversion_factor
            else:
                self.result[world_code] *= conversion_factor
            self.rename_label(world_code, europe_labels[0])

    def apply_add(self, world_code, europe_labels, group):
        """
        Applies an 'add' mapping by renaming the existing world_code to europe_label.
        This method treats 'add' mappings similarly to 'direct' mappings when the world_code exists.

        Args:
            world_code (str): The original code.
            europe_labels (list): List containing the new label.
            group (pd.DataFrame): The group of mappings for this world_code.
        """
        if world_code in self.target:
            # Rename the existing world_code to europe_label
            self.rename_label(world_code, europe_labels[0])
        else:
            logging.warning(f"World code '{world_code}' not found for 'add' mapping. No action taken.")
        # Update the target to include the new label
        if self.axis == "flows":
            self.target = self.result.index
        else:
            self.target = self.result.columns

    def apply_aggregate(self, aggregate_mappings):
        """
        Applies an 'aggregate' mapping by summing multiple world_codes into one europe_label.

        Args:
            aggregate_mappings (pd.DataFrame): DataFrame containing aggregate mappings.
        """
        grouped = aggregate_mappings.groupby('europe_label')
        for europe_label, group in grouped:
            world_codes = group['world_code'].tolist()
            existing_world_codes = [wc for wc in world_codes if wc in self.target]
            if not existing_world_codes:
                continue

            if self.axis == 'flows':
                summed_values = self.result.loc[existing_world_codes].sum()
                self.result.loc[europe_label] = summed_values
                self.result.drop(labels=existing_world_codes, axis='index', inplace=True)
                self.target = self.result.index
            else:
                summed_values = self.result[existing_world_codes].sum(axis=1)
                self.result[europe_label] = summed_values
                self.result.drop(labels=existing_world_codes, axis='columns', inplace=True)
                self.target = self.result.columns

    def apply_empty(self, group):
        """
        Applies an 'empty' mapping by adding a row or column of zeros with the given europe_label.

        Args:
            group (pd.DataFrame): The group of mappings with 'empty' mapping type.
        """
        for _, row in group.iterrows():
            europe_label = row['europe_label']
            if self.axis == 'flows':
                self.result.loc[europe_label] = 0
            else:
                self.result[europe_label] = 0

        # Update target index or columns accordingly
        if self.axis == "flows":
            self.target = self.result.index
        else:
            self.target = self.result.columns

def main():
    """
    Main function to execute the script.
    """
    args = parse_arguments()
    input_folder = Path(args.input_folder).resolve()
    output_folder = Path(args.output_folder).resolve()

    if not input_folder.exists():
        logging.error(f"Input folder '{input_folder}' does not exist.")
        sys.exit(1)

    if args.list_countries:
        print(f"Input folder: {input_folder}")
        list_countries(input_folder)
    elif args.country and args.year:
        country = args.country.upper()
        year = args.year
        logging.info(f"Starting processing for Country: {country}, Year: {year}")
        load_raw_wb_from_txt(country, year, input_folder, output_folder)
        logging.info("Processing completed successfully.")
    else:
        logging.error("Please provide both country and year as positional arguments, or use --list-countries to list available countries.")
        sys.exit(1)

if __name__ == "__main__":
    main()
