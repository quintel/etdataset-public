# 7. Services analysis


## Application splits

The application split and technology shares for 2015 are calculated in the [7_services_source_analysis.xlsx](7_services_source_analysis.xlsx). 
This is based on the source from the [Heat Roadmap Europe](http://www.heatroadmap.eu/output.php) for all heating and cooling. For more information on this source see the [documentation for the residences source analysis](../6_residences/6_residences_source_analysis.md). No changes were made for lighting as no other sources were found. 

## Space heating

I filled out the whole 'final demand by energy carrier' matrix Based on HRE4 allowing and easy calculation of the space heating and space cooling technology split. The total amount of Final Energy demand for Space heating was a little too high, resulting in small negative demands for several fuels. I reduced the FED for space heating a little (this could be seen as analogue to what was done in residences to correct for the heating-degree days correction) and slightly changed the technology shares untill all checks passed. 

| Technology                 | Final Shares |
| :------------------------- | ----: |
| Gas-fired heaters          | 57.1% |
| Electric heat pumps w TS   | 8.7%  |
| Gas-fired heat pumps       | 0.0%  |
| Electric heaters           | 6.0%  |
| Coal-fired heaters         | 0.7%  |
| Oil-fired heaters          | 27.6% |


## Space cooling

I filled out the whole 'final demand by energy carrier' matrix Based on HRE4 allowing and easy calculation of the space heating and space cooling technology split. 

## Central ICT
This sector was included in the front end. This [excellent source on energy demand for ICT](https://www.borderstep.de/wp-content/uploads/2015/01/Borderstep_Energy_Consumption_2015_Data_Centers_16_12_2015.pdf) determined that the the FED for the ICT sector is 43,200TJ in 2015. 


## Lighting

The following technology split is assumed, based on expert data used for the EU 2011 analysis; see /source_analyses/eu/2012/6_residences/lighting_source_analysis.xlsx

| Technology                  | Share |
| :-------------------------- | ----: |
| Standard fluorescent tubes  | 91.0% |
| Efficient fluorescent tubes | 7.0% |
| LED tubes                   |  1.5% |


## Debts

- The technology split for lighting requires more research.
- Demand for other carriers is appr. 52 PJ. This energy use is not accounted for in the ETM.