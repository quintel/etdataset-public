# 2. Power and heat plant analysis

The dashboard assumption for the first attempt were obtained from the NL 2011 dataset. 

The Power and heat plant analysis is filled based on the Platts data. See [fr_2012_installed_capacities.xlsm](../2_power_and_heat_plant/fr_2012_installed_capacities.xlsm).


## Coal and lignite

Platts reports electricity production by coal plants using combined cycle  (600 MW) and steam turbines (6241 MW). Is is assumed that the electricity production is proportional to the installed capacity. The share of Combined cycle is therefore set to 12.3%. The shares of Ultra supercritical and Supercritical are optimized to match the coal use. 

| Technology                    | Share | Comment                 |
| :---------------------------- | ----: | :---------------------- |
| Ultra supercritical co-firing |  0.4% | Based on energy balance |
| Ultra supercritical           |  5.0% | Optimized               |
| Combined cycle                |  6.2% | Based on Platts         |
| Supercritical                 | 88.4% | Optimized               |

The full load hours (FLH) for all coal power plants are set to 3000 h to reflect the installed capacity according to Platts


## Gas

An initial split of the electricity production is based on the default FLH and the installed capacities reported by Platts for the Turbine, Engine and Ultra supercritical. The FLH of the Combined cycle are calculated based on the remaining electricity production and the capacity reported by Platts. The calculated FLH were in line with the average FLH reported by RTE (2013) Bilan electrique 2012, p. 22 (appr. 2300 h).
With the default FLH and the intial share, the calculated fuel input was too low. The shares of the Ultra supercritical and Turbines (lower efficiency) is therefore increased and the Combined cycle (high efficiency) is decreased. 

Increase of the production with Ultra supercritical and Turbines resulted in an increase in installed capacity. The FLH of the Ultra supercritical and Turbines are therefore increased to 1400 h to ensure a installed capacity that matches the Platts data.

| Technology | Capacity | Default FLH | Initial share | Final share | Final FLH |
| :------------------ | ----: | ----: | ----: | ----: | ----: |
| Turbine             |     0 |   700 |  0.0% | 20.0% | 1,200 |
| Combined cycle      | 3,279 | 4,200 | 93.5% | 45.0% | 2,500 |
| Engine              |     3 |   700 |  0.0% |  0.0% |   700 |
| Ultra supercritical | 1,362 |   700 |  6.5% | 35.0% | 2,000 |


## Nuclear

Since there are no 3rd generation nuclear plants yet, the production by 2nd generation nuclear plants is set to 100%. The FLH are set to 6,740 h to reflect the installed capacities according to RTE (2012) Bilan electrique, p. 23 (63,130 MW). The FLH are compareble with those calculated from the Platts data (6,316 h).


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | ----: | ------: |
| River      |                   7,089 | 21.2% |   1,756 |
| Mountain   |                  16,470 | 78.8% |   2,809 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Solar

See [solar_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/solar_source_analysis.xlsx).


## Wind

The share between onshore and offshore wind is calculated in [wind_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/wind_source_analysis.xlsx). It is assumed that all onshore wind is inland. The FLH of coastal and inland wind turbines are set to resp. 2425 h and 1925 h to reflect installed capacity according to RTE (2012) Bilan electrique 2012, p. 14 (load factor 24.0%).


## Oil products

The FLH of oil plants (Oil supercritical and Diesel engine) are set to the average FLH based on total electricity production from the energy balance and the total installed capacity from Platts: 380 h.


## Debts

- (Wind) Shares between inland and coastal wind requires more research.