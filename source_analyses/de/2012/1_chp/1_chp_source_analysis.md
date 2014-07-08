# 1. CHP analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.

The CHP and Power and heat plant analysis are based on Platts data. See [de_2012_installed_capacities.xlsm](../2_power_and_heat_plant/de_2012_installed_capacities.xlsm).


## Autoproduction CHPs:

- (Agriculture, Households and Services) There are no CHPs in the agriculture, households and services sector.
- (Energy Industry) Unsold heat production is set to appr. 90% to reduce the error in modelled sold heat production. 
- (Energy Industry) The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to resp. 44%, 1% and 55%, estimated based on Platts data.
- (Industry) The unsold heat production of gas CHPs is set to 100% and coal CHPs to 99.5% to reduce the error in modelled sold heat production. This setting results in a critical error because the biofuels allocated to unsold heat production exceeds the biofuels available in the final demand section. Due to the small energy flows, this does not result in problems in following analyses. 
- (Industry) The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to resp. 44%, 1% and 55%, estimated based on Platts data.


## Debts

- (Industry) The unsold heat production of gas CHPs is set to 100% and coal CHPs to 99.5% to reduce the error in modelled sold heat production. This setting results in a critical error because the biofuels allocated to unsold heat production exceeds the biofuels available in the final demand section. Due to the small energy flows, this does not result in problems in following analyses. 