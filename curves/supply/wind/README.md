## Wind production curves

We have three methods for generating wind production curves:

* **Open Power System Data platform** - uses measured wind production
* **Renewables.ninja** - modelled production curves based on satellite weather data
* **Quintel analysis** - based on wind measurements which are converted to production

We assess the quality of each of these three methods to select the best curves per region / climate year. The following criteria are important:
* Aggregated curves: The ETM models a whole region and hence the production curves should represent the (aggregated) wind production, not the output of an individual wind turbine. This means that the maximum capacity factor should be lower than 1 (peak production is lower than installed capacity).
* Consistent full load hours: For the present year, the ETM takes its full load hours from statistical agencies. The number of full load hours encoded in a production curve should be consistent with this data, otherwise the capacity factors in the ETM are underestimed or overestimated.

### OPSD
The wind load curves are based on data provided by the [Open Power System Data platform](https://data.open-power-system-data.org). The specific data used in this analysis has been downloaded from [https://data.open-power-system-data.org/time_series/](https://data.open-power-system-data.org/time_series/), choosing the 60 minutes resolution and filtering for only the data specific for:

* the type of profile (preferably `wind_profile`; if not available, `wind_onshore_generation_actual` and `wind_offshore_generation_actual`)
* the relevant country
* the relevant year

According to the website, the underlying data for wind profiles are the measured generation curves. For example for Germany, these are as provided by the four German TSO's. For many other countries, the data is retrieved from the ENTSOE Transparancy platform.

If the data quality is not sufficient (i.e., less than 98% available data points for a specific year and country), the data is not used to create a curve. This is the case for the offshore wind curves for Belgium (2017) and the Netherlands (2015, 2019).

NB1: The data source only has data available for Great Britain. Hence, we use this data for the United Kingdom. In order to run the script without problems, the headers in the source csv file should be changed from "GB\_..." to "UK\_...".

NB2: In 2016 there was a significant increase in installed offshore wind capacity in The Netherlands (factor 3). The measured production data is corrected for this increase. See `wind - data - nl - 2016 - source`.

### Renewables.ninja
[Renewables.ninja](https://www.renewables.ninja/) is a scientific project modelling wind and solar curves for all climate years from 1980 onwards. For (European) countries they offer aggregated production curves, taking into account concurrency of production across a country.

For NL2019 we use the inland wind curves from this source for the climate years 1987, 1997, 2004 and 2019.

We use Renewables.ninja for all European curves
### Quintel method
For some historic years we use measured wind data and convert that to production. General information can be found in the read me in `script` - `weather_years`.
