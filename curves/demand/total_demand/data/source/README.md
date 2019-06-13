## Demand - Total demand - source


The raw data for total demand is provided by ETNSOE ([ENTSO-E, hourly load](https://www.entsoe.eu/data/power-stats/hourly_load/))

For the years **2011 - 2015** 

* the total demand is presented in 12 files, one for each month
* The files downloaded from ENTSO-E are manually converted to CSV files and saved in the `data` folder. No changes are made to the data. 
* The script `demand_curve_generation.py` prepares the ENTSO-E data. ENTSO-E provides files that consider all countries per month, which is not very useful for our purposes. For each country, the script extracts the relevant data range from all CSV files and generates a continuous profile (8760 hours). 
The script also cleans up messy data points that revolve around daylight-saving times (there is a missing data point in March (labeled as n.a.) and an additional row in October). The resulting files are exported in the `demand_curve` folder. 


For the years **2016 and 2017**:

* The format of the ETNSO-E data can directly be used as input for the last step of the data-analysis.
