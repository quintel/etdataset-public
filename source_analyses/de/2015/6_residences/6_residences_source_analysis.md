# 6. Residences analysis

The dashboard assumptions for lighting and appliances, insulation and old/new residences were not updated, but re-used from the 2012 dataset, as no good sources were readly available.
All other data were changed quite considerably, due to a lucky find of an excellent source at: [Heat Roadmap Europe](http://www.heatroadmap.eu/output.php). This contains very details data on heating, hot water, cooking and cooling for the Residences, Services and Industry sectors. These include both applications splits of final demand and carrier/technology splits within these applications. An [extensive Excel file](http://www.heatroadmap.eu/resources/HRE4%20Exchange%20Template%20WP3_v22b_website.xlsx) was downloaded from this website, which contains all this data for different EU countries in 2015. 

The only 'downside' of this data, is that for comparison reasons, space heating and cooling data seems to be corrected for heating-degree days. This means that final energy demand for space heating and space cooling is 'normalized' or corrected for hotter or colder years. For the ETM, since we rely on *actual* energy use i nthe IEA Extended Energy Balance and try to reproduce hourly dynamics in the market, we somehow need to undo this correction. 
  

## Application split

The final demand for space heating, hot water, cooking and cooling can be retrieved from the source mentioned above (this was done on the sheet 'HRE 4 source' of the [residences source analysis](./6_residences_source_analysis_de.xlsx). The final energy demand for lighting and appliances was taken as is from [DESTATIS - "Energieverbrauch der privaten Haushalte" table](https://www.destatis.de/DE/ZahlenFakten/GesamtwirtschaftUmwelt/Umwelt/UmweltoekonomischeGesamtrechnungen/MaterialEnergiefluesse/Tabellen/EnergieverbrauchHaushalte.html). The total sum of Final Demand that results is too high, but since space heating and cooling have been corrected for heating-degree days, this is to be expected. Since space cooling is a tiny amount of energy, I decided to correct final demand for space heating, so the total final demand matched IEA statistics.  

**Results: Final energy demand for:
**

|Application|Unit  |Value | 
| :---------- | :----------: | ------------: |
|Space heating|TJ|1,510,964|
|Hot water|TJ|383,471|
|Space cooling|TJ|441|
|Lighting|TJ|39,600|
|Cooking heating|TJ|88,267|
|Electrical Appliances|TJ|201,600|


## Space heating

The technology and carrier split for space heating was retrieved from the source mentioned above and filled out in the 'Final demand per energy carrier' matrix format. This uses the efficiencies of each device to calculate the percentages (which relate to useful demand). These were filled in to the Dashboard of the 6_residences_analysis.xlsx'. In orde to pass the tests on this sheet, I made some small adjustments manually to space heating only.

| Technology                    | Calc. share 2012 | Final share 2012 | Calc. share 2015 | Final share 2015|
| :---------------------------- | ----------: | ----------: | ----------:| ----------:|
| Condensing combi boiler       |       14.0% |       13.7% |      29.75% |      13.72% | 
| Solar thermal panels          |        0.0% |        1.3% |      0.05% |      13.72% |
| Electric heat pump (ground)  |        0.0% |        0.0% |      0.00% |      13.72% |
| Gas-fired micro CHP           |        0.0% |        0.0% |      0.00% |      13.72% |
| District heating              |       10.0% |        9.2% |      10.33% |      13.72% |
| Electricity-driven heat pump  |        0.0% |        0.0% |      2.33% |      13.72% |
| Woodpellets (biomass) heaters |       14.0% |       14.6% |      11.46% |      13.72% |
| Electric heaters (resistance) |        3.0% |        1.5% |      4.25% |      13.72% |
| Gas-fired heaters             |       31.0% |       30.2% |      14.87% |      13.72% |
| Oil-fired heaters             |       28.0% |       27.8% |      25.57% |      13.72% |
| Coal-fired heaters            |        0.0% |        1.7% |      1.38% |      13.72% |
| Hybrid heat pump			     |        0.0% |        0.0% |      0.00% |      13.72% |


## Hot water

See Space Heating.

| Technology                    | Calc. share 2012 | Final share 2012 | Calc. share 2015 |Final share 2015|
| :---------------------------- | ----------: | ----------: | ----------:| ----------:|
| Condensing combi boiler       |       12.0% |       12.6% |28.05%|28.05%
| Solar thermal panels          |        0.0% |        1.3% |7.77%|7.77%|
| Electric heat pump (ground)  |        0.0% |        0.0% |0.00%|0.00%|
| Gas-fired micro CHP           |        0.0% |        0.0% |0.00%|0.00%|
| District heating              |        4.4% |        4.6% |14.46%|14.46%|
| Electricity-driven heat pump  |        0.3% |        0.3% |2.03%|2.03%|
| Woodpellets (biomass) heaters |        3.4% |        3.7% |3.05%|3.05%|
| Electric heaters (resistance) |       29.6% |       24.2% |5.95%|5.95%|
| Gas-fired heaters             |       30.5% |       32.1% |13.92%|13.92%|
| Oil-fired heaters             |       19.9% |       20.9% |24.26%|24.26%|
| Coal-fired heaters            |        0.00% |        0.3% |0.00%|0.00%|
| Fuel cells     |        0.00% |        0.00% |0.00%|0.00%|
| Hybrid heat pump     |        0.00% |        0.00% |0.00%|0.00%|


## Cooking
See Space Heating.

| Technology                    | Calc. share 2015 |
| :---------------------------- | ----------:|
|Gas stoves|2.92%|
|Electric stoves (resistance)|84.16%|
|Electric halogen stoves|5.34%|
|Electric induction stoves|7.57%|
|Biomass stoves|0.00%|



## Debts

- Technology splits for lighting and appliances need to be researched.
- Split between old en new houses needs to be researched and insulation constants.