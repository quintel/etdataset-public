# 7. Services analysis
For calculations see: [7&#95;services&#95;source&#95;analysis_2019.xlsx](7_services_source_analysis_2019.xlsx). 


##Final demand split to aplications


Final energy demand used for Space , Space Cooling and and for Lighting are derived from the [RVO energiecijfers](https://energiecijfers.databank.nl/jive?workspace_guid=7f9277c8-426b-460d-8780-c45a3dec57d7):
<li> The final demand for space heating of the RVO is reduced with oil (moved to transport sector) and ambient heat (not part of the final energy demand in the services analysis.)

<li> For the electricity demand of the Central ICT sector the demand of economic sector SBI J is taken. See etdataset [issue #883](https://github.com/quintel/etdataset/issues/883) for a discussion on what falls under Central ICT.

##Space heating
<li>The Percentage of useful heat de livered by the remaining technologies  is caculated in the tab space heatin. CBS is the main source. <li> It is assumed that no gas-fired heat pumps are used. All heat pumps are labeled as 'Electric heat pumps with thermal storage', because the ETM does not have other heat pumps. Due to this the ambient heat is overestimated. 

##Lighting
<li>Lighting is based on a rough estimation of the market penetration of LED. see 2020052021_rough_led_lighting_estimation in folder  source_analysis > residences

##Space cooling
<li> It is assumed that the % of as 'Electric heat pumps with thermal storage' is equal to heating. The other space cooling is assumed to be done with air conditioning. 
