# 11. Area analysis

The dashboard assumptions for the first attempt were obtained from the NL 2011 dataset.

## CO<sub>2</sub> emissions

This [European Environmental Agency download site](http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-10) allows you to download the IPCC Common reporting Format Greenhouse gas emissions for many European countries. 

We have used UNFCCC_v17 here in ASCII format.

The source analysis [201602_EEA_NL GHG emissions IPCC format 1990 & 2013.xlsx](./201602_EEA_NL GHG emissions IPCC format 1990 & 2013.xlsx) provides a good method for calculating energetic CO<sub>2</sub> emissions and does so for NL 2013 and 1990. Be sure to apply some filters to the immense file downloaded from the above link. 
Filter by:

- Country_code: NL
- Pollutant_name: CO2
- Year: 1990

Note that this method also allows you to verify if your dataset produces decent CO<sub>2</sub> emissions for the `present_year` (i.e. 2013 for this dataset).

[Energeia](http://www.energeia.nl/) provides regular updates on CO2 ETS prices (look for news items on STEMMING).

We usually use the Cal 17 forward price.


## Arable land and land available for solar PV

Source file is: [20160210_CBS_Landbouw.xlsx](./20160210_CBS_Landbouw.xlsx).

## Population
Source file is: [20151125_CBS_Bevolking kerncijfers.xlsx](./20151125_CBS_Bevolking kerncijfers.xlsx)