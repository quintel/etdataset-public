## Sources for irradiation data

Different data sources are used for irradiation data for The Netherlands and all other countries. 

#### The Netherlands

For the Netherlands, irradiation and temperature curves are based on measured data from The Bilt. (Source: [KNMI](https://projects.knmi.nl/klimatologie/uurgegevens/selectie.cgi))

The file "convert KNMI input to irradiation and temperature file.xlsx" converts the txt files to 

* air_temparature.csv
* irradiation.csv

#### Other countries

For other countries than the Netherlands, the irradiation curves are based on weather data from the [Open Power System Data (OPSD) platform](https://data.open-power-system-data.org/weather_data/). This platform offers weather data at hourly resolution, for Europe, aggregated by Renewables.ninja from the NASA MERRA-2 reanalysis. 

The data should be filtered for:

* variable, indicating the type of profile (radiation\_diffuse\_horizontal and radiation\_direct\_horizontal)
* relevant country
* relevant year

The data can be filtered by opening the link to the OPSD data platform. Navigate to the Download section and click on 'Filter' behind 'weather\_data.csv' (under 'Individual data files (csv, xlsx)'.

The csv file with the filtered data (`weather_data_filtered.csv`) should be saved in the source directory for the relevant country and year combination (`etdataset/curves/supply/solar_thermal/data/<country>/<year>/source`).

For non-European countries (Brazil), the Dutch solar thermal curve is adopted.