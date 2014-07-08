# 6. Residences analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


## Application split

TThe application split of the final demand is obtained from the report "Energy efficiency in Poland 2001-2011" by the Central Statistical Office of Poland (GUS 2013, p. 23, table 3). See [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). It is assumed that the final demand for cooling is 0 PJ. Accoriding to "Energy consumption in households in 2012" by the Central Statistical Office of Poland (GUS 2014) the percentage of households with airconditioning is < 1%. Appr. 2% of the households does have mechanical ventilation.


## Space heating


The technology split for space heating is calculated based on "Energy consumptions in households in 2012" (GUS 2014, p. 96, table 5) and Ecofys data for North-East Europe. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The percentages are adjusted manually to match the IEA energy demand. 

| Application                   | Calc. share | Ecofys | Final share |
| :---------------------------- | ----------: | -----: | ----------: | 
| Condensing combi boiler       |        0.0% |   4.1% |        2.0% |
| Solar thermal panels          |        0.0% |      - |        0.1% |
| Gas-fired heat pump (ground)  |        0.0% |      - |        0.0% |
| Gas-fired micro CHP           |        0.0% |      - |        0.0% |
| District heating              |       33.0% |  34.1% |       31.7% |
| Electricity-driven heat pump  |        0.0% |   0.0% |        0.0% |
| Woodpellets (biomass) heaters |       17.3% |  10.6% |       15.6% |
| Electric heaters (resistance) |        2.2% |   0.0% |        3.4% |
| Gas-fired heaters             |       10.6% |  19.3% |        7.9% |
| Oil-fired heaters             |        0.6% |   9.4% |        3.5% |
| Coal-fired heaters            |       36.2% |  22.4% |       35.8% |
| Electric heat pump add-on     |        0.0% |      - |        0.0% |


## Hot water

The technology split for hot water is calculated based on "Energy consumptions in households in 2012" (GUS 2014, p. 96, table 5). See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The percentages are adjusted manually to match the IEA energy demand. 

| Application                   | Calc. share | Final share |
| :---------------------------- | ----------: | ----------: | 
| Condensing combi boiler       |        0.0% |        0.0% |
| Solar thermal panels          |        0.2% |        0.1% |
| Gas-fired heat pump (ground)  |        0.0% |        0.0% |
| Gas-fired micro CHP           |        0.0% |        0.0% |
| District heating              |       23.0% |       23.2% |
| Electricity-driven heat pump  |        0.0% |        0.0% |
| Woodpellets (biomass) heaters |       11.6% |       11.5% |
| Electric heaters (resistance) |        9.7% |       10.5% |
| Gas-fired heaters             |       26.7% |       20.9% |
| Oil-fired heaters             |        1.7% |        5.2% |
| Coal-fired heaters            |       27.1% |       28.6% |
| Electric heat pump add-on     |        0.0% |        0.0% |


## Space cooling

There is no data available for space cooling. It is assummed that all space cooling is accomplished by conventional air conditioning.


## Cooking

The technology split for cooking is estimated based on "Energy consumption in households in 2012" (GUS 2014, p. 100, table 9). Consumption of coal is aggregated in the biomass stove, consumption of oil is inlcuded in the gas stove. Split between the electric technologies is estimated. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).

| Technology                | Share |
| :------------------------ | ----: |
| Gas stoves                | 77.9% |
| Electric stoves           | 10.0% |
| Electric hologen stoves   | 2.25% |
| Electric induction stoves | 2.25% |
| Biomass stoves            |  7.6% |


## Old and new houses

The split of old and new houses are made determined based on the report "Energy consumption in households in 2012" by the Central Statistical Office of Poland (GUS 2014). See [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).


## Debts

- The technology shares for lighting requires more research.
- The technology shares for appliances requires more research.
