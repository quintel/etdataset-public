# 1. CHP

The following changes were made:

- According to [EEA](http://www.eea.europa.eu/data-and-maps/figures/chp-share-of-total-heat) the CHP share of total heat generation in France is 8.1% in 2009.
- According to [EEA](http://www.eea.europa.eu/data-and-maps/figures/recalculation-of-chp-fuel-input) the fuel input to CHP is appr. 102,850 GWh in 2009, corresponding to 370,260 TJ.
- According to [EEA](http://www.eea.europa.eu/data-and-maps/figures/chp-share-of-total-heat) the CHP heat is 197,435 TJ


The following assumptions are made for autoproduction CHPs:

- (Agriculture) There are very little CHPs in agriculture, which are mainly biogas CHPs (92.5%). The remaining production is done by gas CHPs. All shares are set to 100% by default.
- (Households) There are no CHPs in the households sector. All shares are set to 100% by default.
- (Services) Share of remaining CHP electricity production by gas CHPs and wood pellet CHPs are set to resp. 55% and 45% to optimize sold heat prodcution.
- (Energy Industry) Unsold heat production is increasd to 55% to reduce the error in modelled sold heat production.
- (Energy Industry) The share of gas turbine CHPs and gas combined cycle CHPs are set to resp. 65% and 35%, estimated based on Platts data (combined cycle 1060 MW, gas turbine 1819 MW).
- (Industry) Unsold heat production is increased to 100% to reduce the error in modelled sold heat production. The share of gas turbine CHPs and gas combined cycle CHPs are set to resp. 65% and 35%, estimated based on Platts data.

See [fr_2012_installed_capacities.xlsm](../2_power_and_heat_plant/fr_2012_installed_capacities.xlsm).


## Debts

- In general the calculated fuel input for electricity and sold heat production and the calculated sold heat production is lower than the reported fuel input and reported sold heat production.
