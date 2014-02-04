The folder "total demand" contains everything that is needed to generate a 'total_demand.csv' profile for Merit Order - EU27 2011 model. 

The following describes how the total_demand.csv is created from ENTSO-E data: 


#### ENTSO-E data

The "ENTSO-E" folder holds 12 Excel files that have been downloaded directly from https://www.entsoe.eu/db-query/consumption/mhlv-all-countries-for-a-specific-month/
There also is a pdf document, containing some notes by ENTSO-E. 

(during the research, individual demand curves were found for individual countries. These might be useful for validation or for future reference, see "not used for EU27" folder)


#### Scripts creating profile

Two scripts are used to convert the raw ENTSO-E data into a EU27 profile. 

a. The files downloaded from ENTSO-E are manually converted to CSV files and saved in the 'input' folder. No changes to the data, only a superfluous line for Spain in October is removed. 
b. The script "EU_demand_curve_preparation.py" prepares the ENTSO-E data. ENTSO-E provides files that consider all countries per month, which is not very useful for our purposes. For each country, the script extracts the relevant data range from all CSV files and generates a continuous profile (8760 hours). 
The script also cleans up messy data points that revolve around daylight-saving times (there is a missing data point in March (labeled as n.a.) and an additional row in October). 
The resulting files are exported in the 'output' folder. 
c. The script "EU_profile_generation.py" loads the demand curves stored in the 'output' folder. It filters all EU27 curves (only Malta is missing). It averages these 26 demand curves and then scales the resulting curve to 1/3600. This profile is written to "EU27_deamnd_profile.csv". This is the final total_demand profile and can be copied to the 'profiles' folder. 


