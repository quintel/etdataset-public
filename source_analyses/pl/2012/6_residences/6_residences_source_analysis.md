# 6. Residences analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


The following changes were made:

- The application split of the final demand is obtained from the report "Energy efficiency in Poland 2001-2011" by the Central Statistical Office of Poland (GUS 2013, p. 23, table 3). See source analysis.

- The split of old and new houses are made determined based on the report "Energy consumption in households in 2012" by the Central Statistical Office of Poland (GUS 2014). See source analysis.


Potential sources:

- GUS (2012) Municipal infrastructure in 2011 (xls)
  * Sold heat to residential buildings and public offices (Table 19)
  * Capacity and production of thermic boilers by fuel type (Table 22)
- GUS (2014) Energy consumption in households in 2012
  * Final demand: Table 36 (p. 125). Consumption is substantially higher compared to energy balance!
  * Application shares: Table 4.1 (p. 73) based on survey; Table 5.1 (p. 81) based on energy balance
  * Space heating: Figure 2.1 (p. 33), Table 5 (p. 96), Table 6 (p. 97), Table 8 (p. 99)
  * Hot water: Figure 2.2 (p. 34), Table 5 (p. 96), Table 6 (p. 97), Table 8 (p. 99)
  * Ventilation: Table 11 (p. 100)
  * Cooking: Figure 2.3 (p. 35), Table 5 (p. 96), Table 9 (p. 99)
  * Lighting: Figure 2.4 (p. 37), Table 13 (p. 101)
  * Appliances
  * Number of households: Table 1 (p. 92)
  * Construction periods: Table 3-B (p. 94)
  * Solar collectors and heat pumps: Table 30-31 (p. 120)

Issues:

- The final demand of cooling is not reported and might be included in the final demand for applicances.

- The technology shares need to be researched. The Odyssee data provides to little information.

- [SOLVED] There are #DIV/0 errors in the csv_heater_electricity and csv_water_electricity files because the electricity consumption for space heating and hot water is 0 TJ as result of technology shares of 0%.
