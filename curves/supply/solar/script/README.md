#### Main scripts

The Open Power System source data provides (filtered) data for a specific profile, country and year, which should be stored in the country specific source folder under the following name: `time_series_60min_singleindex_filtered.csv`. Then, dependent on which type of data (either 'solar\_generation\_actual' or 'solar\_profile') is available, run the script `process_solar_generation_actual_data.py [country] [year]` or `process_solar_profile_data.py [country] [year]`. As with all load curves, we normalize the load curves to 1/3600. This results in the following output csv file:

* `solar_pv.csv`

#### Other scripts

In this folder other scripts are available and this is what they do:

- `generate_solar_slider_caps.py` - This script gives the performance ratio and full load hours of the solar solar profile. The performance ratio is the ratio between the maximum produced capacity and the maximum installed capacity.

- `interpolate_solar_profiles.py` - This script interpolates between the Spain solar profile and the country-specific solar profile based on full load hours.

- `plot_solar_profiles.py` - This script plots the solar profiles.

- `normalise_capacity_profile` - Normalises Capacity profiles to 1/3600, these profiles can be downloaded from https://www.renewables.ninja/, MERRA-2 data (source NASA)
