# 6. Residences analysis


## Application split

The application split for residences is obtained from [Enerdata_2014_Energy Efficiency Trends for households in the EU](http://refman.et-model.com/publications/1868). See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).

The [JRC_2012_Energy Efficiency Status Report 2012](http://refman.et-model.com/publications/1844) report is used to refine various assumptions for the technonology splits that the Enerdata report does not provide. The JRC report provides also some information about the electricity use for space cooling, lighting and electrical appliances in 2009. There is some discrepancy, but Odyssee values are used since these are for 2011.

| Application           | Odyssee (TJ) | JRC (TJ)     |
| :-------------------- | -----------: | -----------: |
| Space heating         |    7,480,500 |              |
| Hot water             |    1,611,185 |              |
| Space cooling         |       34,525 |      135,949 |
| Lighting              |      345,254 |      289,253 |
| Cooking               |      690,508 |              |
| Electrical appliances |    1,381,015 |    1,469,407 |


## Space heating 

The technology split for space heating is calculated based on the weighted average of DE, FR, UK and ES. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The percentages are adjusted manually to match the IEA energy demand. 

| Technology                    | Calc. share | Final share |
| :---------------------------- | ----------: | ----------: |
| Condensing combi boiler       |        7.9% |        6.7% |
| Solar thermal panels          |        0.0% |        0.7% | 
| Gas-fired heat pump           |        0.0% |        0.0% |
| Gas-fired micro CHP           |        0.0% |        0.0% |
| District heating              |        3.7% |       11.8% |
| Electricity-driven heat pump  |        0.3% |        0.3% |
| Woodpellets heaters           |       15.0% |       16.0% |
| Electric heaters              |       11.4% |        7.8% |
| Gas-fired heaters             |       43.5% |       34.3% |
| Oil-fired heaters             |       17.8% |       17.4% |
| Coal-fired heaters            |        0.0% |        4.7% |
| Electric heat pump add-on     |        0.4% |        0.4% |


## Hot water

The technology split for hot water is calculated based on the weighted average of DE, FR, UK and ES. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). The percentages are adjusted manually to match the IEA energy demand.

| Technology                    | Calc. share | Final share |
| :---------------------------- | ----------: | ----------: |
| Condensing combi boiler       |        5.5% |        5.0% |
| Solar thermal panels          |        0.0% |        0.7% |
| Gas-fired heat pump           |        0.0% |        0.0% |
| Gas-fired micro CHP           |        0.0% |        0.0% |
| District heating              |        1.7% |        5.8% |
| Electricity-driven heat pump  |        0.2% |        0.2% |
| Woodpellets heaters           |        3.9% |        5.8% |
| Electric heaters              |       36.9% |       31.6% |
| Gas-fired heaters             |       39.6% |       36.2% |
| Oil-fired heaters             |       12.2% |       13.1% |
| Coal-fired heaters            |        0.0% |        1.5% |
| Electric heat pump add-on     |        0.0% |        0.0% |


## Space cooling

There is no data available for space cooling. It is assummed that all space cooling is accomplished by conventional air conditioning.


## Cooking

The [JRC_2012_Energy Efficiency Status Report 2012](http://refman.et-model.com/publications/1844) report provides information about the electricty consumption in residences. According to this study 6.6%  (equivalent to appr. 190,907 TJ) of the electricity consumption is allocated to cooking devices. The share of electricity devices is reduced to match the electricity consumption.

| Technology                | Share |
| :------------------------ | ----: |
| Gas stoves                |   50% |
| Electric stoves           |   25% |
| Electric hologen stoves   |   10% |
| Electric induction stoves |    5% |
| Biomass stoves            |   10% |


## Appliances

The electricity consumption for large appliances (including refrigerators, freezers, washing machines, dishwashers, TVs and dryers) are obtained from [Enerdata_2014_Energy Efficiency Trends for households in the EU](http://refman.et-model.com/publications/1868). The [JRC_2012_Energy Efficiency Status Report 2012](http://refman.et-model.com/publications/1844) report also provides data on the electricity consumption in households. This data is used for the remaining appliances. See also [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx). 

| Technology         | Share  | Source    |
| :------------------| -----: | --------: |
| Dishwashters       |  6.26% | Enerdata  |
| Fridges / Freezers | 25.83% | Enerdata  |
| Washing Machines   | 10.96% | Enerdata  |
| Dryers             |  4.48% | Enerdata  |
| Television         | 12.17% | Enerdata  |
| Computers / Media  | 17.50% | JRC       |
| Vacuum Cleaners    |  5.90% | JRC       |
| Others             | 16.90% | Remaining |


## Other suggested sources

- [CECED_200604_report on Energy Consumption of Domestic Appliances in EU Households.pdf](http://refman.et-model.com/publications/1843)
- [Enerdata_201103_Odyssee European Energy Efficiency trends – Household energy consumption.pdf](http://refman.et-model.com/publications/1842)
- [European Commission_Energy Efficiency Status Report 2012.pdf](http://refman.et-model.com/publications/1844)


## Debts

- There is a difference between the energy consumption for cooling and lighting according to Enerdata and JRC.
- The technology split for lighting is set to the NL 2011 values. Further research is required.
- The "Heater characterization (solar thermal, el. add-on)" is set to the NL 2011 values. Further research is required.
- The "Old / New Houses Split" is set to the NL 2011 values. Further research is required. 


