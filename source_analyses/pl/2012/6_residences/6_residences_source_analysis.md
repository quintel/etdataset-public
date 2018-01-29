# 6. Residences analysis


## Application split

The application split of the final demand is obtained from the report [Energy efficiency in Poland 2001-2011](http://refman.et-model.com/publications/1872) by the Central Statistical Office of Poland (GUS 2013, p. 23, table 3). See [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). It is assumed that the final demand for cooling is 0 PJ. According to [Energy consumption in households in 2012](http://refman.et-model.com/publications/1870) by the Central Statistical Office of Poland (GUS 2014, p. 100, table 11) the percentage of households with airconditioning is < 1%. Appr. 2% of the households does have mechanical ventilation.


## Space heating

The technology split for space heating is calculated based on [Energy consumption in households in 2012](http://refman.et-model.com/publications/1870) (GUS 2014, p. 96, table 5) and Ecofys data for North-East Europe. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The percentages are adjusted manually to match the IEA energy demand. 

| Application                   | Calc. share | Ecofys | Final share |
| :---------------------------- | ----------: | -----: | ----------: | 
| Condensing combi boiler       |        0.0% |   2  % |       0.00% |
| Solar thermal panels          |        0.0% |      - |       0.02% |
| Gas-fired heat pump (ground)  |        0.0% |      - |       0.00% |
| Gas-fired micro CHP           |        0.0% |      - |       0.00% |
| District heating              |       33.0% |  42  % |      32.21% |
| Electricity-driven heat pump  |        0.0% |   0  % |       0.00% |
| Woodpellets (biomass) heaters |       17.3% |  13  % |      15.11% |
| Electric heaters (resistance) |        2.2% |   0  % |       3.90% |
| Gas-fired heaters             |       10.6% |  12  % |       9.75% |
| Oil-fired heaters             |        0.6% |   7  % |       3.70% |
| Coal-fired heaters            |       36.2% |  24  % |      35.31% |
| Electric heat pump add-on     |        0.0% |      - |        0.0% |


## Hot water

The technology split for hot water is calculated based on [Energy consumption in households in 2012](http://refman.et-model.com/publications/1870) (GUS 2014, p. 96, table 5). See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The percentages are adjusted manually to match the IEA energy demand. 

| Application                   | Calc. share | Ecofys | Final share |
| :---------------------------- | ----------: | -----: | ----------: | 
| Condensing combi boiler       |        0.0% |   2  % |       0.00% |
| Solar thermal panels          |        0.2% |   0  % |       0.29% |
| Gas-fired heat pump (ground)  |        0.0% |   0  % |       0.00% |
| Gas-fired micro CHP           |        0.0% |   0  % |       0.00% |
| District heating              |       23.0% |  42  % |      23.85% |
| Electricity-driven heat pump  |        0.0% |   0  % |       0.00% |
| Woodpellets (biomass) heaters |       11.6% |  13  % |      16.05% |
| Electric heaters (resistance) |        9.7% |   0  % |      10.01% |
| Gas-fired heaters             |       26.7% |  12  % |      17.60% |
| Oil-fired heaters             |        1.7% |   7  % |       4.14% |
| Coal-fired heaters            |       27.1% |  24  % |      28.06% |
| Electric heat pump add-on     |        0.0% |      - |       0.00% |


## Space cooling

There is no data available for space cooling. It is assummed that all space cooling is accomplished by conventional air conditioning.


## Cooking

The technology split for cooking is estimated based on [Energy consumption in households in 2012](http://refman.et-model.com/publications/1870) (GUS 2014, p. 100, table 9). Consumption of coal is aggregated in the biomass stove, consumption of oil is inlcuded in the gas stove. Split between the electric technologies is estimated. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).

| Technology                | Share |
| :------------------------ | ----: |
| Gas stoves                | 77.9% |
| Electric stoves           | 10.0% |
| Electric hologen stoves   | 2.25% |
| Electric induction stoves | 2.25% |
| Biomass stoves            |  7.6% |


## Lighting

A first attempt for the calculation of the technology split for lighting is made based on [Energy consumption in households in 2012](http://refman.et-model.com/publications/1870) in [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The calculated values are not yet used because there is a difference in the normalized efficiency.


## Old and new houses

The split of old and new houses are made determined based on the report [Energy consumption in households in 2012](hhttp://refman.et-model.com/publications/1870) by the Central Statistical Office of Poland (GUS 2014, p. 94, table 4B). See [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).


## Debts

- The technology shares for lighting requires more research.
- The technology shares for appliances requires more research.
