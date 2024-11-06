import argparse
import pandas as pd
from pathlib import Path
import sys

def safe_sum(df, columns):
    available_columns = [col for col in columns if col in df.columns]
    if available_columns:
        return df[available_columns].sum(axis=1)
    else:
        return pd.Series([0] * len(df))


def process_balance(country, year):

  # Load the input CSV file (replace with actual file path)
  OUTPUT_PATH = Path(__file__).parents[3] / 'data'
  input_file = '{0}/{1}/{2}/energy_balance/output_energy_balance_enriched.csv'.format(OUTPUT_PATH,country,year)
  df = pd.read_csv(input_file)

  # Helper function to sum only available columns

  # --- Step 1: Aggregating Columns ---
  df_aggregated_columns = pd.DataFrame()
  df_aggregated_columns['nrg_bal'] = df['nrg_bal']
  df_aggregated_columns['Total'] = df['Total']

  # Aggregating for 'Coal'
  df_aggregated_columns['Coal'] = safe_sum(df, [
      'Sub-bituminous coal', 'Peat and peat products', 'Oil shale and oil sands',
      'Patent fuel', 'Coke oven coke', 'Gas coke', 'Coal tar',
      'Brown coal briquettes', 'Anthracite', 'Coking coal', 'Other bituminous coal'
  ])

  # Aggregating for 'Coal gas'
  df_aggregated_columns['Coal gas'] = safe_sum(df, [
      'Gas works gas', 'Coke oven gas', 'Blast furnace gas', 'Other recovered gases'
  ])

  # Aggregating for 'Oil'
  df_aggregated_columns['Oil'] = safe_sum(df, [
      'Other oil products', 'Paraffin waxes', 'Fuel oil',
      'White spirit and special boiling point industrial spirits', 'Lubricants', 
      'Bitumen', 'Petroleum coke', 'Naphtha', 'Liquefied petroleum gases', 'Ethane', 
      'Crude oil', 'Natural gas liquids', 'Refinery feedstocks', 
      'Additives and oxygenates (excluding biofuel portion)'
  ])
  df_aggregated_columns['Bio oil'] = safe_sum(df, ['Pure biogasoline', 'Blended biogasoline', 'Pure biodiesels',
                                                  'Pure bio jet kerosene', 'Blended bio jet kerosene', 'Other liquid biofuels'])

  df_aggregated_columns['Lignite'] = safe_sum(df, ['Lignite'])

  # Aggregating for 'Diesel'
  df_aggregated_columns['Diesel'] = df['Gas oil and diesel oil (excluding biofuel portion)'] 

  # Set 'Gas power fuelmix' to 0 
  df_aggregated_columns['Gas power fuelmix'] = 0 

  # Aggregating for 'Network gas'
  df_aggregated_columns['Network gas'] = safe_sum(df, ['Biogases', 'Natural gas'])

  # Aggregating for 'Waste mix'
  df_aggregated_columns['Waste mix'] = safe_sum(df, ['Renewable municipal waste', 'Non-renewable municipal waste', 
                                                    'Industrial waste (non-renewable)'])

  # Aggregating for 'Wood pellets'
  df_aggregated_columns['Wood pellets'] = df['Primary solid biofuels']

  # Aggregating for 'Torrefied Wood pellets'
  df_aggregated_columns['Torrefied Wood pellets'] = df['Charcoal'] 

  # Aggregating for 'Hydro'
  df_aggregated_columns['Hydro'] = df['Hydro']


  # Aggregating for 'Wind'
  df_aggregated_columns['Wind'] = df['Wind']

  # Aggregating for 'Solar thermal'
  df_aggregated_columns['Solar thermal'] = df['Solar thermal']

  # Aggregating for 'Solar photovoltaic'
  df_aggregated_columns['Solar photovoltaic'] = df['Solar photovoltaic']


  # Aggregating for 'Geothermal'
  df_aggregated_columns['Geothermal'] = df['Geothermal'] 

  # Aggregating for 'Nuclear'
  df_aggregated_columns['Nuclear'] = df['Nuclear heat']

  # Aggregating for 'Electricity'
  df_aggregated_columns['Electricity'] = df['Electricity']

  # Aggregating for 'Heat'
  df_aggregated_columns['Heat'] = df['Heat']

  # --- Step 2: Aggregating Rows based on 'nrg_bal' mappings ---
  # Define a mapping dictionary
  mapping_dict = {
      'Transformation input - electricity and heat generation - main activity producer electricity only - energy use':
          'Transformation input - electricity and heat generation - producer electricity only - energy use',
      'Transformation input - electricity and heat generation - main activity producer combined heat and power - energy use':
          'Transformation input - electricity and heat generation - producer combined heat and power - energy use',
      'Transformation input - electricity and heat generation - main activity producer heat only - energy use':
          'Transformation input - electricity and heat generation - producer heat only - energy use',
      'Transformation input - electricity and heat generation - autoproducer electricity only - energy use':
          'Transformation input - electricity and heat generation - producer electricity only - energy use',
      'Transformation input - electricity and heat generation - autoproducer combined heat and power - energy use':
          'Transformation input - electricity and heat generation - producer combined heat and power - energy use',
      'Transformation input - electricity and heat generation - autoproducer heat only - energy use':
          'Transformation input - electricity and heat generation - producer heat only - energy use',
      'Transformation output - electricity and heat generation - main activity producer electricity only':
          'Transformation output - electricity and heat generation - producer electricity only',
      'Transformation output - electricity and heat generation - main activity producer combined heat and power':
          'Transformation output - electricity and heat generation - producer combined heat and power',
      'Transformation output - electricity and heat generation - main activity producer heat only':
          'Transformation output - electricity and heat generation - producer heat only',
      'Transformation output - electricity and heat generation - autoproducer electricity only':
          'Transformation output - electricity and heat generation - producer electricity only',
      'Transformation output - electricity and heat generation - autoproducer combined heat and power':
          'Transformation output - electricity and heat generation - producer combined heat and power',
      'Transformation output - electricity and heat generation - autoproducer heat only':
          'Transformation output - electricity and heat generation - producer heat only',
      'Gross electricity production - autoproducer combined heat and power':
          'Gross electricity production - producer combined heat and power',
      'Gross electricity production - main activity producer combined heat and power':
          'Gross electricity production - producer combined heat and power',
      'Gross electricity production - autoproducer electricity only':
          'Gross electricity production - producer electricity only',
      'Gross electricity production - main activity producer electricity only':
          'Gross electricity production - producer electricity only',
      'Gross heat production - autoproducer combined heat and power':
          'Gross heat production - producer combined heat and power',
      'Gross heat production - main activity producer combined heat and power':
          'Gross heat production - producer combined heat and power',
      'Gross heat production - autoproducer heat only':
          'Gross heat production - producer heat only',
      'Gross heat production - main activity producer heat only':
          'Gross heat production - producer heat only',
      'Gross heat production':
          'Gross heat production',
      'Gross electricity production':
          'Gross electricity production'
      # Add any additional mappings if needed
  }

  # Load the intermediate aggregated file for row aggregation
  df_filtered = df_aggregated_columns[df_aggregated_columns['nrg_bal'].isin(mapping_dict.keys())]

  # Map nrg_bal to the corresponding group
  df_filtered['Group'] = df_filtered['nrg_bal'].map(mapping_dict)

  # Group by 'Group' and sum numeric columns
  numeric_cols = df_filtered.select_dtypes(include='number').columns
  df_aggregated = df_filtered.groupby('Group', as_index=False)[numeric_cols].sum().round(3) # TO-DO round up to a max of 3 

  # Final output CSV
  output_file = '{0}/{1}/{2}/energy_balance/intermediate_producers_raw.csv'.format(OUTPUT_PATH,country,year)
  df_aggregated.to_csv(output_file, index=False)

  print(f"Aggregation completed and saved to '{output_file}'")
  print(df_aggregated)

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
        help="Country code and name to filter data by (e.g., RS_serbia)."
    )
    parser.add_argument(
        'year',
        type=int,
        nargs='?',
        help="Year to filter data by (e.g., 2023)."
    )
    return parser.parse_args()

def main():
    """
    Main function to execute the script.
    """
    args = parse_arguments()
    if args.country and args.year:
      country = args.country.upper()
      year = args.year
      process_balance(country,year)
    else:
      print("Please provide both country and year as positional arguments.")
      sys.exit(1)


if __name__ == "__main__":
    main()


