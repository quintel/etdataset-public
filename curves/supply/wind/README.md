The wind load curves are based on data provided by the [Open Power System Data platform](https://data.open-power-system-data.org). The specific data used in this analysis has been downloaded from [https://data.open-power-system-data.org/time_series/](https://data.open-power-system-data.org/time_series/), choosing the 60 minutes resolution and filtering for only the data specific for:

* the type of profile (preferably `wind_profile`; if not available, `wind_onshore_generation_actual` and `wind_offshore_generation_actual`)
* the relevant country
* the relevant year

According to the website, the underlying data for wind profiles are the measured generation curves. For example for Germany, these are as provided by the four German TSO's. For many other countries, the data is retrieved from the ENTSOE Transparancy platform.

If the Open Power System Data platform has no data available for a country, the "nl" data is used.

Furthermore, if the data quality is not sufficient (i.e., less than 98% available data points for a specific year and country), the data is not used to create a curve. This is the case for the offshore wind curves for Belgium (2017) and the Netherlands (2015). Hence, for the Netherlands (2015) a different source (Ecofys) has been used to generate this curve.

NB: The data source only has data available for Great Britain. Hence, we use this data for the United Kingdom. In order to run the script without problems, the headers in the source csv file should be changed from "GB\_..." to "UK\_...".
