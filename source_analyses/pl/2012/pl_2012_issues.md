# Main issues with the PL 2012 dataset

## General


## Specific

- (Preparation) The three additional columns in the IEA energy balance should be addressed in our analysis. See [0_data_preparation_source_analysis](0_preparation/0_data_preparation_source_analysis.md#debts).

- (CHP, Autoproducer CHPs) In general, the calculated fuel input for electricity and sold heat production is lower than the reported fuel input. This might be caused by the generally lower overall efficiencies. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Main activity CHPs) The calculated fuel input for electricity and sold heat production is lower than the reported fuel input. Furthermore, the calculated sold heat production is higher than the reported sold heat production. Especially for lignite the calculated sold heat production is to high. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Main activity CHPs) The installed capacity of gas CHPs exceeds the installed capacity according to Platts (ETM: 2042 MW, Platts: 780 MW). See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (PP&HP, Main activity heat plants) In general, the calculated fuel inputs for main activity heat plants are highter than the reported fuel inputs. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (PP&HP, Wind) Shares between inland and coastal wind requires research. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (Metal) There is a lot of unmodelled coal transformation in the metal sector. This is cause by an 'overproduction' of cokes. (Transformation output of cokes ovens is appr. 250 PJ, where the final demand is only appr. 27 PJ.) See [4a_metal_industry_source_analysis](4a_metal_industry/4a_metal_industry_source_analysis.md#debts).

- (Metal) Even with 100% coal gas input in the blast furnace burner, the unmodelled final demand of coal gas is 5.8 PJ. See [4a_metal_industry_source_analysis](4a_metal_industry/4a_metal_industry_source_analysis.md#debts).

- (Chemical) Negative final demand for woodpellets. Most likely cause by allocation in CHP analysis. See also [ETdataset#175](https://github.com/quintel/etdataset/issues/175). See [4b_chemical_industry_source_analysis](4a_chemical_industry/4a_chemical_industry_source_analysis.md#debts).

- (Residences) The technology shares for lighting and appliances requires more research. See [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Services) The technology share for lighting requires more research. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).

- (Services) Demand for other carriers is appr. 700 TJ. This energy use is not accounted for in the ETM. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).

- (Area) More research and validation is required. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).

- (Area) Offshore wind potential requires more research. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).

- (Area) Capacity credit parameters need to be updated. See [11_area_data_source_analysis](11_area_data/11_area_data_source_analysis.md#debts).