# Main issues with the FR 2012 dataset

## General


## Specific

- (Preparation) The three additional columns in the IEA energy balance should be addressed in our analysis. See [0_data_preparation_source_analysis](0_preparation/0_data_preparation_source_analysis.md#debts).

- (CHP) In general the calculated fuel input for electricity and sold heat production and the calculated sold heat production is lower than the reported fuel input and reported sold heat production. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (PP&HP, Wind) Shares between inland and coastal wind requires research. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (Metal) There is some unmodelled coal transformation as result of 'overproduction' of cokes. Nevertheless, cokes production in the cokes oven < cokes input in blast furnace and + final demand. Consequently, there is appr 20 PJ cokes import in France. See [4a_metal_industry_source_analysis](4a_metal_industry/4a_metal_industry_source_analysis.md#debts).

- (Chemical) Negative final demand for woodpellets. Most likely cause by allocation in CHP analysis. See also [ETdataset#175](https://github.com/quintel/etdataset/issues/175). See [4b_chemical_industry_source_analysis](4a_chemical_industry/4a_chemical_industry_source_analysis.md#debts).

- (Residences) The technology splits for space cooling, lighting, cooking and appliances requires research. See [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Residences) The split between old en new houses need to be researched. nSee [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Services) The technology split for lighting requires more research. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).
- (Services) Demand for other carriers is appr. 12 PJ, from which 11,644 TJ is municipal waste and 622 TJ is geothermal. This energy use is not accounted for in the ETM. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).

- (Other) Allocation is incomplete and incorrect (e.g. electricity use for pipeline transport is allocated into oil). See [10_other_source_analysis](10_other/10_other_source_analysis.md#debts). See also [ETdataset#295](https://github.com/quintel/etdataset/issues/295).

- (Area) More research and validation is required. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).

- (Area) Onshore and offshore wind potential requires more research. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).

- (Area) Capacity credit parameters need to be updated. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).