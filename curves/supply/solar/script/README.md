## Processing solar profiles

The solar profiles from the OPSD platform should only be normalized before being used in the ETM. Two scripts are available:

- process_solar_generation_actual_data.py
- process_solar_profile_data.py

For most countries the process_solar_generation_actual_data.py should be used.
Only for Germany and the United Kingdom process_solar_profile_data.py should be used, since these countries use a OPSD 'solar_profile' (= a solar profile based on the installed capacity) instead of a 'solar_generation_actual'. For Germany, the underlying data for solar pv and wind profiles are the measured generation curves as provided by the four German TSO's.

## Other scripts

In this folder other scripts are available and this is what they do:

- generate_solar_slider_caps.py ->
  This script gives the performance ratio and full load hours of the solar solar profile. The performance ratio is the ratio between the maximum produced capacity and the maximum installed capacity.

- interpolate_solar_profiles.py ->
  This script interpolates between the Spain solar profile and the country-specific solar profile based on full load hours.

- plot_solar_profiles.py ->
  This script plots the solar profiles.
