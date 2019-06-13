## Demand - Total demand

The total_demand curve is used as a back-up curve if an electric technology does not have a specific curve assigned (currently not the case). 


### Source
The input data for total demand is provided by ETNSOE ([ENTSO-E, hourly load](https://www.entsoe.eu/data/power-stats/hourly_load/))


For the years **2011 - 2015** the raw data has to be converted from 12 files to one file for each country. For the years 2016 and 2017 The format of the ETNSO-E data can directly be used as input for the last step of the data-analysis.

### Script
The script reads input from the source folder, normalized to 1/3600 and places the output file in the right folder.