# 2. Power and heat plant analysis

The energy balance and the Platts data for Poland to not match. Were the Platts database reports a substantial amount of main activity power plants (30,308 MW), the IEA energy balance only reports electricity by main activity CHPs. Therefore, only the total installed capacities per commodity are matched for Poland.

See [pl_2012_installed_capacities.xlsm](../2_power_and_heat_plant/pl_2012_installed_capacities.xlsm).

| Commodity | Power plant capacity | CHP capacity | Total capacity |
| :-------- | -------------------: | -----------: | -------------: |
| Coal      |               26,105 |        5,598 |         31,703 |
| Gas       |                   15 |          765 |            780 |
| Oil       |                  400 |         n.a. |            400 |
| Waste     |                 n.a. |            9 |              9 |
| Hydro     |                1,785 |         n.a. |          1,795 |
| Wind      |                1,750 |         n.a. |          1,750 |


## Coal and lignite

The IEA energy balance does not report any electricity from main activity coal power plants.


## Gas

The IEA energy balance does not report any electricity from main activity gas power plants.


## Nuclear

There is no nuclear power.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | ----: | ------: |
| River      |                      67 |  4.6% |   1,384 |
| Mountain   |                     878 | 95.4% |   2,214 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Solar

The IEA energy balance does not report any solar power. The FLH for solar technologies is calculated in the [solar_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/solar_source_analysis.xlsx).


## Wind

The share between onshore and offshore wind is calculated in [wind_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/wind_source_analysis.xlsx). he percentage wind turbines offshore is set to 0% because there is no offshore wind yet. According [The Wind Power](http://www.thewindpower.net/country_maps_en_27_poland.php) all wind farms are still planned. It is assumed that all onshore wind is inland.

The FLH of inland wind turbines are optimized to match the installed capacity according to EWEA.


## Oil products

The IEA energy balance does not report any electricity from main activity oil power plants.


## Debts

- (Main activity heat plants) In general, the calculated fuel inputs for main activity heat plants are highter than the reported fuel inputs.