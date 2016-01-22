# 2. Power and heat plant analysis

The [2_chp_pp_source_analysis.xlsx](../2_power_and_heat_plant/2_chp_pp_source_analysis.xlsx) source analysis is the basis for all but some dashboard values used in the `power_and_heat_plant_analysis`. The sheets `PP - CBS Results by machine` and `Power Plants and CHPs compare` in the source analysis are the most important. This source analysis relies heavily on data on heat and electricity generation and production capacity from the Dutch Centraal Bureau voor Statistiek (CBS). 

The aim of the `2_power_and_heat_plant_analysis` is to makes sure the right technologies per fuel type are used by the ETM to produce electricity. The file `2_chp_pp_source_analysis.xlsx` summarizes CBS data in the output formats found on the `chp_analysis` and ` pp_hp_analysis` 'Results by machine' sheets. This makes comparison easiers. 

The `Power Plants and CHPs compare` sheet in the `2_chp_pp_source_analysis.xlsx` file provides an overview of results from the 2011 and 2012 chp_analysis and pp_hp_analysis and the CBS 2013 data. This makes it easier to compare changes between the 2011 and 2012 ETM datasets for NL as well as comparing the 2013 ETM dataset to the numbers reported by CBS.

The 2011 ETM dataset and the 2012 ETM dataset are a bit different, due to better sources being available this year. This is an improvement therefore. 

## Coal and Lignite

CBS does not provide enough information to determine the installed coal-fired power plant capacity. For that number we referred to PLATTS data. See [nl_2012_installed_capacities_PLATTS.xlsm](../2_power_and_heat_plant/nl_2012_installed_capacities_PLATTS.xlsm) for more information on where this data came from. This number is also used to determine the installed capacity of Gas-fired steam turbines.
The installed capacity for coal-fired IGCC is known as there is only one plant. Its production share (4.8%) for coal-fired electricity is calculated based on CBS numbers.

## Gas

The technology shares for electricity production by gas plants are optimized to match fuel use. The full load hours are optimized to obtain installed capacities as listed in 2_chp_pp_source_analysis.xlsx.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | -----:| ------: |
| River      |                      37 |  100% |   3,050 |
| Mountain   |                       0 |    0% |   4,492 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers  several EU countries.


## Solar

See [solar_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/solar_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers  several EU countries. This mostly provides an estimate of full load hours. The pp_hp_analysis calculated the effective installed capacity based on these and the IEA autoproducer table includes information on the sectors solar PV is installed in.  

## Wind

The 2_chp_pp_source_analysis.xlsx file provides a detailed overview of all windparks in the Netherlands. This is used to estimate the split between coastal and inland onshore wind turbines. CBS provides the total production and installed capacity split between onshore and offshore wind turbines. CBS also provides the installed onshore wind capacities and elecricity production per province. This latter information is used to estimate FLH for inland wind turbines. These were adjusted upward w.r.t. the 2012 dataset from 1,700 to 1,800 FLH. Coastal wind turbine FLH were readjusted to 2,300 FLH from 2,250 FLH in 2012 to reproduce installed capacities. 

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | -----:| ------: |
| Coastal    |              755        | 30.8% |   2,300 |
| Offshore   |              220        | 13.7% |   3,500 |
| Inland     |            1,733        | 55.5% |   1,800 |
   
 
## Full load hours

The FLH are mostly tweaked to optimize installed capacities according to 2_chp_pp_source_analysis.xlsx. 


## Debts

## Most important sources

- [CBS statline electricity and heat numbers](http://statline.cbs.nl/StatWeb/publication/?VW=T&DM=SLNL&PA=37823WKK&D1=59,1318&D2=a&D3=a&D4=a&D5=l&HD=1309181425&HDR=G4,T&STB=G1,G2,G3)
- [CBS statline wind production numbers](http://statline.cbs.nl/StatWeb/publication/?DM=SLNL&PA=70802NED&D1=0,3,6&D2=a&D3=152,169,186,203&HDR=T,G1&STB=G2&VW=T)
- [Overview of all Dutch wind parks](http://www.thewindpower.net/country_zones_en_10_netherlands.php)
- [Installed onshore wind capacities and electricity production per province](http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=70960NED&D1=0,3,6,9&D2=a&D3=20-24&HDR=T&STB=G1,G2&VW=T)
- [Platts data](../2_power_and_heat_plant/nl_2012_installed_capacities_PLATTS.xlsm)