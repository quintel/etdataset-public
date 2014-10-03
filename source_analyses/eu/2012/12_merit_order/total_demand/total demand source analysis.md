The folder "total_demand" contains everything that is needed to generate a `total_demand.csv` profile for all European countries and the EU27 model. These `total_demand.csv` are used in the Loss of Load calculation and, if available, for the Merit Order. This datain this folder is about **2012**. 

The following describes how the `total_demand.csv` is created from ENTSO-E data: 


#### ENTSO-E data

The "ENTSO-E" folder holds 12 Excel files that have been downloaded directly from https://www.entsoe.eu/db-query/consumption/mhlv-all-countries-for-a-specific-month/
There also is a pdf document, containing some notes by ENTSO-E. 


#### Scripts creating profile

Two scripts are used to convert the raw ENTSO-E data into `total_demand.csv`. profile. 

a. The files downloaded from ENTSO-E are manually converted to CSV files and saved in the `data` folder. No changes are made to the data. 
b. The script "demand_curve_generation.py" prepares the ENTSO-E data. ENTSO-E provides files that consider all countries per month, which is not very useful for our purposes. For each country, the script extracts the relevant data range from all CSV files and generates a continuous profile (8760 hours). 
The script also cleans up messy data points that revolve around daylight-saving times (there is a missing data point in March (labeled as n.a.) and an additional row in October). 
The resulting files are exported in the `demand_curve` folder. 
c. The script `demand_profile_generation.py` loads the demand curves stored in the `demand_curve` folder and scales the result such that all data points add up to 1/3600. The resulting profiles are stored in the `demand_profile` folder. In addition, an EU27 demand profile is generated by filtering all EU27 curves (only Malta is missing). It averages these 26 demand curves and then scales the resulting curve to 1/3600. This profile is written to `demand_profiles/EU27_demand_profile.csv`.
d. The `demand_profiles` can be copied to the corresponding dataset folder on ETSource. Make sure to rename the file to `total_demand.yml` and change the layout (see `etsource/datasets/nl/load_profiles/total_demand.yml` for an example).

