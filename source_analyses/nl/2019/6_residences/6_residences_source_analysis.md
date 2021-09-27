# 6. Residences source analysis

 The details can be found in [6_residences_source_analysis_2019.xlsx](6_residences_source_analysis_2019.xlsx).
	

##Sources and assumptions	
	
1.	The Applicance split is based on the [RVO energiecijfers databank](https://energiecijfers.databank.nl/jive?workspace_guid=0f55ab62-f953-4173-9991-c8dae422b7a4) 

2.	The split of electricity is done based on the following steps: 
	1. [Eurostat](https://ec.europa.eu/eurostat/web/energy/data/database) is used disaggregated final electricity consumption in households - quantities for electricity demand of Cooling, Cooking, Space heating and Hot Water. 
	2. Electricity for lighting is based on the [RVO energiecijfers databank](https://energiecijfers.databank.nl/jive?workspace_guid=0f55ab62-f953-4173-9991-c8dae422b7a4) 
	3. The remaining of the electricity demand is split the various technologies/applications from [Energietrends 2016, page 9] (https://refman.energytransitionmodel.com/publications/2068)
	4. I  combined the stated categories into the technologies used in the ETM
3. The lighting technology splits are estimated based on the % market share. 
4. 	I have used data from [CBS -statline](https://opendata.cbs.nl/#/CBS/nl/dataset/82379NED/table?dl=520DA) to obtain the final demands for heat pumps heating and cooling. The split between heatpumps ground/air for cooling is not known. Basing it on capacity or the share for heating would give a too large ambient heat demand. 
	
## Housing types
Split of residences in housing types is based on an analysis of BAG data by Kadaster.

Average gas demand per household is used as a proxy to estimate average heat demand per housing type.

The residence split + average heat demand per housing type is used in the Residences analysis to determine how much of total useful space heating demand goes to each housing type.
	
	
##Other assumptions	
	
1.	The split for FD for space heating and electiricity is based on the Energiecijfers databank (see tab application split)
2.	I have assumed that oil and coal can only be used for space heating and not for hot water
3.	I have assumed that wood pellets are not used for cooking in 2019
4.	I have assumed that the share of gas-fired heaters for space heating is half the share of wood pellet heater for space heating. The hot water for gas-fired heaters is based on the applicance split between space heating and hot water. 
	
	
##Final result	
	
Finally, I used the efficiencies to translate the final demand in a useful demand, using the latter to determine the technology shares for each application
	
##Improvements/Debts
1. The cooling split to technologies could be improved. Data is missing at this moment. The assumptions is that heat pump ground and air cool the same amount. 
2. The electricity split between tv, computers, dishwashers etc can be improved. An old source 'Energietrends 2016' used. 
3. Not a good source is known for the % of led lighting in houses. Now it is based on the market % LED-lighting for households and residences
4. The split between hybrid heat pumps and heat pumps is not known. The 2015 source is used: [Routekaart hybride warmtepomp](https://refman.energytransitionmodel.com/publications/2069)
5. The amount natural gas used by gas fire heaters is not known. Now it is similar to the 2015 dataset. Maybe an overestimation.


## Sources

1. [RVO energiecijfers databank](https://energiecijfers.databank.nl/jive?workspace_guid=0f55ab62-f953-4173-9991-c8dae422b7a4) 
2. [Energietrends 2016 (ECN)](https://refman.energytransitionmodel.com/publications/2068)
3. [Correctie elektriciteitsverbruik koken (ECN)](http://refman.et-model.com/publications/2028)
4. [CBS statline heat pumps](http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=82380NED&D1=2,5-6&D2=a&D3=1&D4=21&HDR=T&STB=G2,G1,G3&VW=T)
5. [Routekaart hybride warmtepomp](https://refman.energytransitionmodel.com/publications/2069)
6. [CBS average gas demand per housing type] (http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=81528NED&D1=0&D2=1-5&D3=0&D4=5&HDR=G1&STB=G2,G3,T&VW=T)
7. [Kadaster housing type split] (https://www.kadaster.nl/documents/20838/88047/Productbeschrijving+Woningtypering/a72e071a-e7af-4b93-aef2-a211de0f2056)
8. [CBS -statline](https://opendata.cbs.nl/#/CBS/nl/dataset/82379NED/table?dl=520DA) 
