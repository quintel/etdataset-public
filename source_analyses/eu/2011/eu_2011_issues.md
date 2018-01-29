# Main issues with the EU 2012 dataset

## General


## Specific

- (Preparation) - There is a lack of research data, telling us how much solar PV capacity is placed in households, services and main activity. The shift of solar PV can be improved if better sources become available. See [0_data_preparation_source_analysis](0_preparation/0_data_preparation_source_analysis.md#debts).

- (Preparation) It is not known if the autoproducer table is accurate. From our experience with the German dataset, we got the impression that IEA does not report autoproducer production with high accuracy (it may well be that countries do not report autoproduction). It seems that some autoproducer energy flows are reported as main activity in IEA statistics (prime example: solar PV). See [0_data_preparation_source_analysis](0_preparation/0_data_preparation_source_analysis.md#debts).

- (CHP) Generally, the fuel input for electricity and sold heat production is too low. This indicates that the the CHPs in the EU might have lower efficiencies than those defined in the ETM. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Services) The sold heat production in the services sector is not sufficient. The CHPs in the EU might have a lower electrical efficiency than those defined in the ETM. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (PP&HP, Lignite) For lignite power plants the installed capacity is even with FLH of 8000 h slightly higher compared to the installed capacity reported by Platts. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).


- (PP&HP) Installed capacity of central heaters: We need to validate the 'heat deficit' of CHP plants that is passed on to the PP&HP analysis. This heat deficit is then produced by main activity heaters. However, this capacity is not validated and seems rather large. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (PP&HP) Many FLH and installed capacities have not yet been researched very well. This can be improved, if better sources become available. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (Chemical) Negative final demand for woodpellets. Most likely cause by allocation in CHP analysis. See also [ETdataset#175](https://github.com/quintel/etdataset/issues/175). See [4b_chemical_industry_source_analysis](4a_chemical_industry/4a_chemical_industry_source_analysis.md#debts).

- (Residences) There is a difference between the energy consumption for cooling and lighting according to Enerdata and JRC. See [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Residences) The technology splits for space cooling and lighting requires research. See [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Residences) The split between old en new houses need to be researched. nSee [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Services) The technology split for lighting requires more research. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).

- (Services) Demand for other carriers is appr. 42 PJ. This energy use is not accounted for in the ETM. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).

- (Area) More research and validation is required. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).

- (Area) Onshore and offshore wind potential requires more research. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).

- (Area) Capacity credit parameters need to be updated. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).