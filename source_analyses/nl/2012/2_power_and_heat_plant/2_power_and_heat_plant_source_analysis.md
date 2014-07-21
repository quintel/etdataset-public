# 2. Power and heat plant analysis

The dashboard assumption for the first attempt were obtained from the NL 2011 dataset. 


## Coal and Lignite

The technology shares for electricity production by coal plants are based on NL 2011 data and optimized to match fuel use.


## Gas

The technology shares for electricity production by gas plants are based on NL 2011 data and optimized to match fuel use.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | -----:| ------: |
| River      |                      37 |  100% |   2,808 |
| Mountain   |                       0 |    0% |   4,492 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers  several EU countries.


## Solar

See [solar_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/solar_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers  several EU countries. 


## Full load hours

The FLH are still on the NL 2011 values. The FLH need to be tweaked using the CBS data (see [1_chp_source_analysis.xlsx](../1_chp/1_chp_source_analysis.xlsx)) and the Platts data (see [nl_2012_installed_capacities_platts.xlsm](nl_2012_installed_capacities_platts.xlsx)).


## Debts

- Technology shares for coal and gas need to be researched.
- FLH need to be researched.