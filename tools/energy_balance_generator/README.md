# Energy Balance Conversion Tool

This tool processes and converts energy balances from Eurostat or CSV files according to specific steps and input files. It also allows exporting the results to `ETLocal` or generating source analyses.

## Setup

To get started, you'll need to install the necessary dependencies using `pipenv`.

### Installation:

1. Clone the repository.
2. Navigate to the project directory.
3. Ensure you have Python 3.x and Pipenv installed. Then, run the following command to install dependencies:

   ```bash
   pipenv install
   ```

## Running the Tool

The tool processes energy balances for a given year and a list of countries. Available operations include conversions, exporting to `ETLocal`, and generating source analyses.

### Conversion of Energy Balances

The tool automatically fetches data from Eurostat via the API or reads pre-existing CSV files. It applies conversions to the energy balance data based on the specified country and year.

#### Usage:

```bash
pipenv run conversions <YEAR> <COUNTRIES> [retrieve-only]
```

- `<YEAR>`: The year of the energy balance you want to process.
- `<COUNTRIES>`: A list of country codes, separated by commas (without spaces). You can also use `EU27_COUNTRIES_AND_TOTAL` to process all EU27 countries at once.
- `[retrieve-only]`: (Optional) If provided, the script retrieves the raw CSV from the API and saves it without further processing.

#### Examples:

To run conversions for France in 2019:
```bash
pipenv run conversions 2019 FR
```
This will check if raw Eurostat data exists, and use it if it does. If the data is not found, it will draw data from Eurostat and process it straight away.

To retrieve and save the raw CSV from Eurostat without processing:
```bash
pipenv run conversions 2019 FR retrieve-only
```

### Importing World Balances

The tool fetches data from a specified input folder, and processes it similar to the Eurostat data,
but for a 'world' balance. The output should be in the same format as the output of the conversions.

#### Usage:

```bash
pipenv run import_world <COUNTRY> <YEAR> [input_folder] [output_folder]
pipenv run import_world --list-countries [input_folder]
```

#### Examples:

To import the world balance for Switzerland in 2019 (note Switzerland is spelt as 'SWITLAND' - many countries have this quirk):
```bash
pipenv run import_world SWITLAND 2019 "/Users/User/Desktop/Secure Location" ../../data/CH_switzerland/2019/energy_balance
```

To retrieve a list of all the country names in the txt files (to account for strange spellings):
```bash
pipenv run import_world --list-countries ./data/input
```

### Exporting Energy Balances to ETLocal

After processing the energy balances, you can export them to `ETLocal` using the following command:

```bash
pipenv run export <YEAR> <COUNTRIES>
```

- `<YEAR>`: The year of the energy balance to export.
- `<COUNTRIES>`: Specify the country code(s), or use `ALL` to export all available energy balances.

#### Example:

To export energy balances for France in 2019:
```bash
pipenv run export 2019 FR
```

To export all energy balances for 2019:
```bash
pipenv run export 2019 ALL
```

### Generating Source Analyses

You can generate source analyses for energy balances using the following command:

```bash
pipenv run source_analyses <YEAR> <COUNTRIES>
```

- `<YEAR>`: The year for which to generate source analyses.
- `<COUNTRIES>`: Specify the country code(s), or use `EU27_COUNTRIES_AND_TOTAL` for all EU27 countries.

#### Example:

To generate source analyses for France in 2019:
```bash
pipenv run source_analyses 2019 FR
```

### Working with Scripts

You can modify or extend the tool's functionality by editing the scripts or adding new converters under the `etm_tools` directory.

- **Converters**: Located under `etm_tools.energy_balance_operations.converters`, these define how energy balances are processed.
- **Source Analyses**: Scripts for generating source analyses are located under `etm_tools.source_analysis`.

### Structure of the Tool

- **Conversions**: The tool processes energy balances from either Eurostat or CSV files and applies a series of transformations (e.g., industry chemical, ICT, metal, power plants).
- **Export**: The export script moves processed energy balances into a dataset folder for `ETLocal`.
- **Source Analyses**: Generates additional files for source analyses using pre-defined methodologies.
- **Import World**: Grabs data from a local .txt file in a secure location and applies a series of transformations
  (e.g., industry chemical, ICT, metal, power plants) to generate enriched energy balances for world format data.
