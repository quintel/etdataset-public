# 2. Power and heat plant analysis

The Power and heat plant analysis is filled based on the Platts data. See [eu_2011_installed_capacities.xlsm](../2_power_and_heat_plant/eu_2011_installed_capacities.xlsm).


## Coal

Platts reports electricity production by coal plants using combined cycle (1,535 MW) and steam turbines (62,645 MW). Is is assumed that the electricity production is proportional to the installed capacity. The share of Combined cycle is therefore set to 1.6. The shares of Ultra supercritical and Supercritical are optimized to match the coal use. 

| Technology                    | Share | Comment                 |
| :---------------------------- | ----: | :---------------------- |
| Ultra supercritical co-firing | 13.9% | Based on energy balance |
| Ultra supercritical           | 20.0% | Optimized               |
| Combined cycle                |  1.6% | Based on Platts         |
| Supercritical                 | 64.5% | Optimized               |

The full load hours (FLH) for the coal power plants are slightly reduced to reflect the installed capacity according to Platts.


### Lignite

Platts reports electricity production by lignite plants using steam turbines (29,245 MW). The FLH of the lignite plants are increased to 8000 h to come close to the installed capacities according to Platts. Modelled installed capacities are still slightly to high (31,544 MW).


## Gas

An initial split of the electricity production is based on the default FLH and the installed capacities reported by Platts for the Turbine, Combined cycle, Engine and Ultra supercritical. With the default FLH and the intial share, the calculated fuel input was too low. The share of the Ulta supercritical (lower efficiency) is therefore increased and the Combined cycle (high efficiency) is decreased. Increase of the production with Ultra supercritical resulted in an increase in installed capacity. The FLH of the Ultra supercritical are therefore increased to ensure a installed capacity that matches the Platts data.

| Technology | Capacity | Default FLH | Initial share | Final share | Final FLH |
| :------------------ | -----: | ----: | ----: | ----: | ----: |
| Turbine             |  6,354 |   700 |  1.2% |  1.2% | 1,850 |
| Combined cycle      | 87,744 | 4,200 | 98.0% | 69.1% | 5,350 |
| Engine              |    286 |   700 |  0.1% |  0.1% | 1,200 |
| Ultra supercritical |  5,988 |   700 |  1.1% | 35.0% | 2,850 |


## Nuclear

Since there are no 3rd generation nuclear plants yet, the production by 2nd generation nuclear plants is set to 100%. The FLH are set to 8,000 h to reflect the installed capacities according to Platts.


### Hydro plants

The ETM does not consider pumped storage as a power producer. Only Run-of-river and Run-of-mountain hydro power is considered. According to the tables 3.1.1.4 and 3.2.1.4 in [Eurolectric_2011_Power Statistics & Trends 2011 full report](http://refman.et-model.com/publications/1836) (p. 82, 140), hydro river and mountain plants are characterised as follows: 

|                 | Total hydro | Conventional | Of which Run-of-river | Of which Run-of-mountain |
| :-------------- | ----------: | -----------: | --------------------: | -----------------------: |
| Production, TWh |         355 |          238 |                   115 |                      124 |
| Capacity, MW    |     142,861 |      100,525 |                28,720 |                   70,235 |

See also [capacity_validation.xlsx](/Old/capacity_validation.xlsx), sheet "Hydro plants".

"Total hydro" refers to all hydro electricity, including pumped mountain storage. "Run-of-mountain" is calculated from the other numbers. Note that these numbers are not very accurate as the number of digits may suggest. The research data addresses the year 2009 (or older) and research data is not available for all counties.

The following technology split is set for hydro plants, based on the electricity production. The FLH are estimated based on Platts data (installed capacity 96,210 MW).

| Technology | Share | FLH (h) |
| :--------- | ----: | ------: |
| River      | 48.0% |   4,150 |
| Mountain   | 52.0% |   2,650 |


## Solar

See [solar_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/solar_source_analysis.xlsx).


### Wind

The share between onshore and offshore wind is calculated in [wind_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/wind_source_analysis.xlsx). It is assumed that all onshore wind is inland. FLH for wind are based on the report [Europe's onshore and offshore wind energy potential](http://refman.et-model.com/publications/1312) by the European Environment Agency.


## Debts

- For lignite power plants the installed capacity is even with FLH of 8000 h slightly higher compared to the installed capacity reported by Platts.