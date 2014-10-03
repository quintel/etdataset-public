# Main issues with the ES 2012 dataset

## General

## Specific

- (Preparation) The three additional columns in the IEA energy balance should be addressed in our analysis. See [0_data_preparation_source_analysis](0_preparation/0_data_preparation_source_analysis.md#debts).

- (Preparation) PV shift might be required; see [https://github.com/quintel/etdataset/issues/535](https://github.com/quintel/etdataset/issues/535).

- (CHP, Autoproducer CHPs) In general the calculated fuel input for electricity and sold heat production is lower than the reported fuel input. This might be caused by the generally lower overall efficiencies. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Main activity CHPs) There are no main activity CHPs in Spain. Why? See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Energy Industry) Percentage of CHP electricity production of gas vs. coal need to be researched. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Energy Industry) Shares of gas CHPs need to be researched. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, Industry) Shares of gas CHPs need to be researched. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (CHP, FLH) Full load hours need to be researched based on installed capacities. See [1_chp_source_analysis](1_chp/1_chp_source_analysis.md#debts).

- (PP&HP) Dashboard assumptions should be researched based on an overview of installed capacities to validate the technology share and full load hours. See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (PP&HP, Solar) It seems that conversion of solar thermal to electricity is not correctly covered by the PP&HP analysis. See [ETdataset#495](https://github.com/quintel/etdataset/issues/495). See [2_power_and_heat_plant_source_analysis](2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md#debts).

- (Metal) There is a lot of unmodelled coal transformation in the metal sector.  See [4a_metal_industry_source_analysis](4a_metal_industry/4a_metal_industry_source_analysis.md#debts).

- (Chemical) Negative final demand for woodpellets. Most likely cause by allocation in CHP analysis. See also [ETdataset#175](https://github.com/quintel/etdataset/issues/175). See [4b_chemical_industry_source_analysis](4a_chemical_industry/4a_chemical_industry_source_analysis.md#debts) and [5_industry_source_analysis](5_industry/5_industry_source_analysis.md#debts).

- (Residences) There is a large discrepancy between the Ecofys data and the optimized values w.r.t. space heating and hot water: share of electric technologies is lower, share of oil technologies is higher. See [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Residences) Split between old en new houses need to be researched. See [6_residences_source_analysis](6_residences/6_residences_source_analysis.md#debts).

- (Services) Demand for other carriers is appr. 21 PJ. This energy use is not accounted for in the ETM. See [7_services_source_analysis](7_services/7_services_source_analysis.md#debts).