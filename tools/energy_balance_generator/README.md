# Energy balance conversion
Converts an energy balance according to some steps and input files.

### Setup
You can easily setup with pipenv.
```
pipenv install
```

### Running the tool

And then you can run the conversions with
```
pipenv run conversions <YEAR> <COUNTRIES>
```

Or you can generate some source analyses with
```
pipenv run source_analyses <YEAR> <COUNTRIES>
```

For COUNTRIES you can use the special keyword `EU28` to run the tool for all European countries at once. Or you can run a single country, or a list of countries (separated by commas, without spaces between them, eg `AT,BE,DE`).

To export the energy balances to ETLocal please use
```
pipenv run export <YEAR> <COUNTRIES>
```

Here the special keyword `ALL` can be used to export all energy balances.

# Conversions

## Inputs and parameters

The tool will automatically download a clean Eurostat balance from the official
Eurostat API to start the conversion with. If you don't want this, you can also supply
your own energy balance (in Eurostat flat format).

The code-keys for the flows and products from the Eurostat EB will be translated and
ordered based on the translations given in the `config/eurostat_translations.yml` file.

**NOTE:** Add some more info about what input files are needed per country
- powerplant files
- demand files
- ???

## Types of conversions

In `energy_balance_operations/converters` you can find all the different converters,
and you may add more converters there. These converters have one main method called
`conversion` that takes arguments that are needed for the type of conversion.

You can call these converters from the main script.

### Industry chemical converter
This converter uses final demands of different carriers in the fertilizer sector to
split the original Eurostat chemical sector up into the ETM sectors _chemical fertilizers_
and _chemical other_.

In psuedocode:
```
fertilizer_demand_of_carrier_group is given by INPUT

for each carrier_group
  chemical_demand_carrier_group = sum(chemical_demand_carrier for carrier in carrier_group)
  share = fertilizer_demand_of_carrier_group / chemical_demand_carrier_group
  set fertilizer sector demand of each carrier to chemical_demand_carrier * share
```

### Industry ICT converter

Story about converter

Pseudocode of converter

### Industry metal converter

Story about converter

Pseudocode of converter

### Powerplants converter

Story about converter

Pseudocode of converter

# Source analyses

## Inputs and parameters

Something about that.

## Types of analyses

### Industry chemical analyses
Generates three files: for gas, oil_products and fuels.

# Developing and using the tool

## Structure of the tool

You can add scripts that use the tools in the scripts folder.

Or you can continue building the tools that are in the etm_tools folder.

__under construction__
