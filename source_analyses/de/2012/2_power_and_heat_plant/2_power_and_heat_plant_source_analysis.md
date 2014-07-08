# 2. Power and heat plant analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.

The Power and heat plant analysis is filled based on the Platts data. See [de_2012_installed_capacities.xlsm](../2_power_and_heat_plant/de_2012_installed_capacities.xlsm).


## Coal and lignite

Platts reports electricity production by coal and lignite plants using combined cycle  (67 MW) and steam turbines (46,767 MW). Is is assumed that the electricity production is proportional to the installed capacity. The share of Combined cycle is 0.15% of both coal and lignite plants. The share of Combined cycle for coal plants is therefore set to 0.3%. The shares of Ultra supercritical and Supercritical are optimized to match the coal use. 

| Technology                    | Share | Comment                 |
| :---------------------------- | ----: | :---------------------- |
| Ultra supercritical co-firing |  9.1% | Based on energy balance |
| Ultra supercritical           | 40.0% | Optimized               |
| Combined cycle                |  0.3% | Based on Platts         |
| Supercritical                 | 50.7% | Optimized               |


## Gas

An initial split of the electricity production is based on the default FLH and the installed capacities reported by Platts for the Turbine, Combined cycle, Engine and Ultra supercritical. With the default FLH and the intial share, the calculated fuel input was too low. The share of the Ulta supercritical (lower efficiency) is therefore increased and the Combined cycle (high efficiency) is decreased. Increase of the production with Ultra supercritical resulted in an increase in installed capacity. The FLH of the Turbine and Ultra supercritical are therefore increased to 2000 h to ensure a installed capacity that matches the Platts data.

| Technology | Capacity | Default FLH | Initial share | Final share | Final FLH |
| :--------- | -------: | ----------: | ------------: | ----------: | --------: |
| Turbine             | 1,411 |  700 |  4.4% |  4.4% | 2000 |
| Combined cycle      | 4,611 | 4200 | 83.0% | 66.9% | 4200 |
| Engine              |    33 |  700 |  0.1% |  0.1% |  700 |
| Ultra supercritical | 2,819 |  700 | 12.5% | 32.5% | 2000 |


## Nuclear

Since there are no 3rd generation nuclear plants yet, the production by 2nd generation nuclear plants is set to 100%. The FLH are set to 7,900 h to reflect the installed capacities according to the Platts data.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | ----: | ------: |
| River      |                   3,947 | 65.3% |   3,509 |
| Mountain   |                   1,308 | 34.7% |   5,614 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Wind

Currently based on DE 2011 data. Requires validation.


## Debts

- (Coal and Lignite) Current FLH are slightly to low to match the installed capacity by Platts (ETM: 50.8 GW, Platts: 46.8 GW)
- (Wind) Shares between inland and coastal wind requires more research.
- (Wind) Methodology for wind should be described in source analysis.