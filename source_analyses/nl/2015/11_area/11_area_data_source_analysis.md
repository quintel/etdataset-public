# 11. Area analysis

The dashboard assumptions for the first attempt were obtained from the NL 2013 dataset.

## CO<sub>2</sub> emissions

This [European Environmental Agency download site](https://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-13) allows you to download the IPCC Common reporting Format Greenhouse gas emissions for many European countries. 

Be sure to apply some filters to the immense file downloaded from the above link. 
Filter by:

- Country_code: NL
- Pollutant_name: CO2
- Year: 1990

We have used UNFCCC_v21 here. See etdataset/source_analyses/eu/2015/11_area/201807_EEA_all_countries GHG emissions IPCC format 1990 UNFCCC_v21.xlsx for an overview of all countries currently in the ETM.

Note that this method also allows you to verify if your dataset produces decent CO<sub>2</sub> emissions for the `present_year` (i.e. 2015 for this dataset).

EU ETS CO<sub>2</sub> price is based on the average price of 2015, see e.g. [Investing.com](https://www.investing.com/commodities/carbon-emissions-historical-data).


## Arable land and land available for solar PV
Source is: [CBS statline](http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=80780ned&D1=1-11&D2=0&D3=12-13,15&HDR=G1,G2&STB=T&VW=T)

Source file is: [20160210_CBS_Landbouw.xlsx](./20160210_CBS_Landbouw.xlsx).

## Population
Source file is: [20151125_CBS_Bevolking kerncijfers.xlsx](./20151125_CBS_Bevolking kerncijfers.xlsx)