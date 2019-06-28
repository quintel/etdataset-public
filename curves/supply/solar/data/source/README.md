# Solar profiles

Hourly load profiles are used in the merit order module to determine the availability of volatile electricity sources and the run profiles of must-run technologies. The sources of these load profiles as well as the load profiles themselves are stored in ETDataset.

Both wind and solar pv profiles are based on data provided by the Open Power System Data (OPSD) platform (https://data.open-power-system-data.org/). The specific data used in this analysis has been downloaded from https://data.open-power-system-data.org/time_series/, choosing the 60 minutes resolution and filtering for:

* the type of profile (preferably solar\_profile; if not available, solar\_generation\_actual)
* the relevant country
* the relevant year.

Filtering the data could be done on the website-link above. Go to the Download section, go to 'individual data files' and click on 'Filter' behind the 'time\_series\_60min\_singleindex.csv'.

For each country the following profiles are used:

| Dataset | Source | Profile |
| ------- | ------- |------- |
| BE | OPSD | BE\_solar\_generation\_actual |
| BR | | |
| DE | OPSD | DE\_solar\_profile |
| DK | OPSD | DK\_solar\_generation\_actual |
| ES | OPSD | ES\_solar\_generation\_actual |
| EU | |
| FR | OPSD | FR\_solar\_generation\_actual |
| NL | OPSD | NL\_solar\_generation\_actual |
| PL | | |
| UK | OPSD | GB\_UKM\_solar\_profile |

So only for Germany and the United Kingdom a 'solar\_profile' is available, for almost all other countries the 'solar\_generation\_actual' profile is used.

NB: The data source only has data available for Great Britain. Hence, we use this data for the United Kingdom. In order to run the script without problems, the headers in the source csv file should be changed from "GB\_..." to "UK\_...". And the suffix "UKM" in the GB .csv-file should be removed to run the scripts without problems.
