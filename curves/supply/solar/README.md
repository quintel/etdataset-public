## Solar production curves

There are two methods for generating solar production curves:

* **Default years** - uses measured solar production
* **Weather years** - based on irradiation measurements which are converted to production

### Default curves

The solar load curves are based on data provided by the [Open Power System Data platform](https://data.open-power-system-data.org). The specific data used in this analysis has been downloaded from [https://data.open-power-system-data.org/time_series/](https://data.open-power-system-data.org/time_series/), choosing the 60 minutes resolution and filtering for only the data specific for:

* the type of profile (either 'solar\_generation\_actual' or 'solar\_profile') 
* the relevant country
* the relevant year

The solar profiles from the OPSD platform should only be normalized before being used in the ETM. Two scripts are available:

* `process_solar_generation_actual_data.py`
* `process_solar_profile_data.py`

For most countries the `process_solar_generation_actual_data.py` script should be used.
Only for Germany and the United Kingdom `process_solar_profile_data.py` should be used, since these countries use a OPSD 'solar\_profile' (= a solar profile based on the installed capacity) instead of a 'solar\_generation\_actual'. For Germany, the underlying data for solar pv and wind profiles are the measured generation curves as provided by the four German TSO's.

Furthermore, if the data quality is not sufficient (i.e., less than 98% available data points for a specific year and country), the data is not used to create a curve. This is the case for the solar curve for the Netherlands (2015). Hence, a different source (SoDa: Solar Radiation Data) has been used to generate this curve.


### Weather years
The solar load curves which are based on data provided by the [Open Power System Data platform](https://data.open-power-system-data.org) are not available for the weather years (1987, 1997, 2004). That is why we use measured irradiation data and convert that to production.

General information can be found in the read me in `script` - `weather_years`.