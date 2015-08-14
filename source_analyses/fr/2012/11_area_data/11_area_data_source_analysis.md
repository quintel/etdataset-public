# 11. Area analysis

The dashboard assumptions for the first attempt were obtained from the NL 2011 dataset.


The following changes were made:

- Areable land, coast line, land available for solar, number of inhabitants, offshore suitable for wind, onshore suitable for wind, number of buildings, number of residences, residences roof surface available for pv, buildings roof surface available for pv, co2 emissions 1990 were obtained from various sources.


## Roof surface available for PV

The total roof surface available for PV is 854 km2 according to Ecofys analysis. It is assumed that 2/3 is on residences and 1/3 on buildings.

| Location                                 | Area (km2) |
| :--------------------------------------- | ---------: |
| residences_roof_surface_available_for_PV |       569  |
| buildings_roof_surface_available_for_PV  |       285  |

## CO<sub>2</sub> emissions

This [European Environmental Agency download site](http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-7/national-greenhouse-gas-inventories-ipcc-common-reporting-format-sector-classification/ascii-delimited-zip/at_download) allows you to download the IPCC Common reporting Format Greenhouse gas emissions for many European countries. 

The source analysis [201409_EEA_NL GHG emissions IPCC format 1990 & 2012.xlsx](../../../nl/2012/11_area/201409_EEA_NL GHG emissions IPCC format 1990 & 2012.xlsx) provides a good method for calculating energetic CO<sub>2</sub> emissions and does so for NL 2012 and 1990. Be sure to apply some filters to the immense file downloaded from the above link. 
Filter by:

- Country_code: FR
- Pollutant_name: CO2
- Year: 1990

Note that this method also allows you to verify if your dataset produces decent CO<sub>2</sub> emissions for the `present_year` (i.e. 2012 for this dataset).

[Energeia](http://www.energeia.nl/) provides regular updates on CO2 ETS prices (look for news items on STEMMING).

We usually use the Cal 16 forward price.


## Debts

- More research and validation is required.
- Offshore wind potential requires more research.
- Capacity credit parameters need to be updated.
