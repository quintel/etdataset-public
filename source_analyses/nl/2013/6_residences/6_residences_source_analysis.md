# 6. Residences source analysis

The residences analysis was greatly improved with respect to the 2012 dataset. I performed a bottom-up analysis of all energy flows in the residences sector per carrier, application and technology. The details can be found in [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).

			## Sources and assumptions		1. I used the split of electricity consumption over the various technologies/applications from 'Energietrends 2014', page 9	   -	I combined the stated categories into the technologies used in the ETM   -	Combined with the final electricity demand from the IEA energy balance, this allowed me to determine the final demand for the technologies   -	I have assumed that 'ventilatie' is the same as cooling2.	I split the final demand for the electric cooking technologies by using data from 'Correctie elektriciteitsverbruik koken (ECN)', table 1 (last colum)3.	The lighting technology splits determined in the NL/2012 dataset are re-used here as they were well-researched within the Energy Productivity project4.	I have combined data from 'Hernieuwbare energie in Nederland 2014' (CBS) and 'IEA HPP Annex 42: Heat Pumps in Smart Grids, Task 1: Market Overview, The Netherlands' (Delta Energy & Environment, 2014) to obtain the final demands for heat pumps				##	Assumptions				1.	Lacking better data, I have assumed that for 'solar thermal' and 'district heating' 80% of the final demand is used for space heating and 20% for hot water2.	I have data to determine the final demand for space heating for heat pumps, but none for final demand for hot water; I assumed the latter to be 25% of the former (80%-20% rule, see 1)3.	I have assumed that oil and coal can only be used for space heating and not for hot water4.	I have assumed that wood pellets are not used for cooking in 20135.	I have assumed that the share of gas-fired water heaters (boilers) is almost equal to the share of electric water heaters (boilers). This allowed me to split of the part of the natural gas for space heating that goes to gas-fired water heaters; the remainder of the gas goes to condensing combi boilers6.	Finally, I have assumed that the share of gas-fired heaters is almost identical to the share of wood pellet heater. This allowed me to split of the part of the natural gas for space heating that goes to gas-fired heaters; the remainder of the gas goes to condensing combi boilers				## Final result					Finally, I used the efficiencies to translate the final demand in a useful demand, using the latter to determine the technology shares for each application. These technology shares are used to fill out the dashboard of the residences analysis.

## Debts

1. The split for solar thermal panels between space heating and hot water needs to be researched.
2. The 'Percentage of useful heat in space heating delivered by solar thermal panel (if household is equipped)' needs to be better researched
3. The 'Percentage of useful heat in hot water delivered by solar thermal panel (if household is equipped)' needs to better researched
4. The split between old and new residences needs to be better researched

## Sources

1. [Energietrends 2014 (ECN)](http://refman.et-model.com/publications/2027)
2. [Correctie elektriciteitsverbruik koken (ECN)](http://refman.et-model.com/publications/2028)
3. [IEA HPP Annex 42: Heat Pumps in Smart Grids - Task 1: Market Overview - The Netherlands](http://refman.et-model.com/publications/2029)
4. [Hernieuwbare energie in Nederland 2014](http://refman.et-model.com/publications/2030)






