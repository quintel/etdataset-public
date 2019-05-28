The Open Power System source data provides (filtered) data for a specific profile, country and year, which should be stored in the country specific source folder under the following name: `time_series_60min_singleindex_filtered.csv`. Then, run the script `process_data.py [country] [year]`. Depending on which data is available, one of the other data processing scripts (either `process_wind_profile_data.py`, `process_wind_onshore_offshore_generation_actual_data.py`, or `process_wind_onshore_generation_actual_data.py`) is run. This results in the following input csv files:

* `wind_coastal.csv`
* `wind_inland.csv`
* `wind_offshore.csv`

If onshore and offshore production are both available, we use the onshore production data to generate a wind inland profile. The offshore production data is used to generate both coastal and offshore wind profiles. These profiles are corrected by running `generate_wind_profiles.py [country] [year]` to make sure that they match the full load hours as determined in the Power and heat plant analysis. As with all load profiles, we normalize the load profiles to 1/3600. This results in the following output csv files:

* `wind_coastal_baseline.csv`
* `wind_inland_baseline.csv`
* `wind_offshore_baseline.csv`
