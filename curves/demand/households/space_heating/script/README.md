# Generating heat demand curves for households

### About
The script `generate_all_curves` uses the heat demand tool to generate heating curves
for all housing and insulation types (5*3=15 curves total). The are a few variables
that can be set:
- **Thermostat** You can adjust thermostat settings in the `data/thermostat.csv` file.
- **R values and surface area** You can adjust these values in `heat_demand/config.py`.
- **Extra behaviour parameters** You can adjust the behaviour even more by setting the `BEHAVIOUR_FITTING_RESULTS` constant in `heat_demand/config.py.


The script expects that each country has an `input` folder containing the csv files `air_temperature` and `irradiation`.

### Running the script
You can run the tool for any country with:
```
python3 generate_all_curves.py <YEAR> <COUNTRY_1> <COUNTRY_2> <COUNTRY_3> ...
```

Or you can use the special keyword 'EU_27'. For example
```
python3 generate_all_curves.py 2019 EU_27
```
will generate and write curves for all countries in EU-27 for the year 2019.
