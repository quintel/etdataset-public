### This eu folder contains load profiles for the EU27 model (base year 2011). 

Documentation on how profiles are made in general can be found on [https://github.com/quintel/merit/blob/master/profile_generation_guidelines.md](https://github.com/quintel/merit/blob/master/profile_generation_guidelines.md)
The profiles stored in this folder are exported from the excel file "wind_solar_hydro analysis.xlsx". 

This folder contains 9 profiles: 

##### agriculture_chp.csv
	identical to NL profile - lack of data for EU27

##### buildings_chp.csv
	identical to NL profile - lack of data for EU27

##### industry_chp.csv
	This profile is 'always on', as we assume that industry runs around the clock  - sane assumption as in NL model

##### river.csv
	identical to NL profile - lack of data for EU27

##### solar_pv.csv
	based on 2 German, 1 Spanish and 1 fake Greek (Spanish profile, time-zone shifted)

##### total_demand.csv

	The original curves (per country and per month) have been downloaded from ENTSO-E, see https://www.entsoe.eu/db-query/consumption/mhlv-all-countries-for-a-specific-month 
	We consider 26 out of the 27 EU countries, only Malta is missing. Have a look at the readme.md in .../data/total demand

##### wind_coastal.csv
	identical to NL profile - lack of data for EU27

##### wind_inland.csv
	based on 1 Dutch inland, 2 German and 1 Austrian load curve. 

##### wind_offshore.csv
	identical to NL profile - lack of data for EU27
