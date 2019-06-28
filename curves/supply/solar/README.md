## Processing solar profiles

The solar profiles from the OPSD platform should only be normalized before being used in the ETM. Two scripts are available:

- process\_solar\_generation\_actual\_data.py
- process\_solar\_profile\_data.py

For most countries the process\_solar\_generation\_actual\_data.py should be used.
Only for Germany and the United Kingdom process\_solar\_profile\_data.py should be used, since these countries use a OPSD 'solar\_profile' (= a solar profile based on the installed capacity) instead of a 'solar\_generation\_actual'. For Germany, the underlying data for solar pv and wind profiles are the measured generation curves as provided by the four German TSO's.

Furthermore, if the data quality is not sufficient (i.e., less than 98% available data points for a specific year and country), the data is not used to create a curve. This is the case for the solar curve for the Netherlands (2015). Hence, a different source (SoDa: Solar Radiation Data) has been used to generate this curve.

## Other scripts

In this folder other scripts are available and this is what they do:

- generate\_solar\_slider\_caps.py ->
  This script gives the performance ratio and full load hours of the solar solar profile. The performance ratio is the ratio between the maximum produced capacity and the maximum installed capacity.

- interpolate\_solar\_profiles.py ->
  This script interpolates between the Spain solar profile and the country-specific solar profile based on full load hours.

- plot\_solar\_profiles.py ->
  This script plots the solar profiles.
