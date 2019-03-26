# 6. Residences source analysis

The residences analysis was greatly improved in 2013 with respect to the 2012 dataset. JB performed a bottom-up analysis of all energy flows in the residences sector per carrier, application and technology. The details can be found in [6_residences_source_analysis.xlsx](6_residences_source_analysis.xlsx).

			## Sources and assumptions		1. I used the split of electricity consumption over the various technologies/applications from 'Energietrends 2015', page 9	   -	I combined the stated categories into the technologies used in the ETM   -	Combined with the final electricity demand from the IEA energy balance, this allowed me to determine the final demand for the technologies   -	I have assumed that 'ventilatie' is the same as cooling2.	I split the final demand for cooking technologies by using data Energietrends 2015 and combine this with average kWh use for electric cooking and shares and efficiencies of electric cooking technologies. 3.	The lighting technology splits determined in the NL/2012 dataset are re-used here as they were well-researched within the Energy Productivity project4.	I have combined CBS data on total installed capacity of heatpumps and Berenschot data on total number of HHP's to obtain the final demands for heat pumps and split this final demand over the 3 HP technologies.			##	Assumptions				1.	The split for FD for space heating and electiricity is based on the Energiecijfers databank (see tab application split)2.	I have assumed that oil and coal can only be used for space heating and not for hot water3.	I have assumed that wood pellets are not used for cooking in 20154.	Finally, I have assumed that the share of gas-fired heaters for both water and space heating is half the share of wood pellet heater for space heating				## Final result					Finally, I used the efficiencies to translate the final demand in a useful demand, using the latter to determine the technology shares for each application. These technology shares are used to fill out the dashboard of the residences analysis.
## Housing types
Split of residences in housing types is based on an analysis of BAG data by Kadaster.

Average gas demand per household is used as a proxy to estimate average heat demand per housing type.

The residence split + average heat demand per housing type is used in the Residences analysis to determine how much of total useful space heating demand goes to each housing type.

## Debts

1. The 'Percentage of useful heat in hot water delivered by solar thermal panel (if household is equipped)' needs to better researched


## Sources

1. [Energiecijfers databank](https://energiecijfers.databank.nl/jive?cat_open_var=db_ggv_hh&var=db_ggv_hh&geolevel=nederland&favorite=nederland_1)
2. [Energietrends 2016 (ECN)](https://refman.energytransitionmodel.com/publications/2068)
3. [Correctie elektriciteitsverbruik koken (ECN)](http://refman.et-model.com/publications/2028)
4. [CBS statline heat pumps](http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=82380NED&D1=2,5-6&D2=a&D3=1&D4=21&HDR=T&STB=G2,G1,G3&VW=T)
5. [Routekaart hybride warmtepomp](https://refman.energytransitionmodel.com/publications/2069)
6. [CBS average gas demand per housing type] (http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=81528NED&D1=0&D2=1-5&D3=0&D4=5&HDR=G1&STB=G2,G3,T&VW=T)
7. [Kadaster housing type split] (https://www.kadaster.nl/documents/20838/88047/Productbeschrijving+Woningtypering/a72e071a-e7af-4b93-aef2-a211de0f2056)







