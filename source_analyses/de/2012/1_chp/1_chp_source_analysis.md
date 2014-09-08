# 1. CHP analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.

The dashboard of the CHP analysis is filled based on enriched data from the German BundesNetzAgentur (BNA). The complete list of power plants and CHPs was obtained from BNA and this was enriched with a column specifying each plant's technology using a document by the Deutsche Institut für Wirtschaftsforschung (DIW) and inferred guesses from each power plant's 'Block name' field entry in the BNA list.
See [de_2012_capacity validation_gross.xlsx](../2_power_and_heat_plant/de_2012_capacity validation_gross.xlsx).

This analysis is used for both the CHP analysis (Step 1 of data generation process) and this analysis, as these cannot really be done separately. Since the BNA's definition of what makes a CHP is *machine based* (i.e. is there a heat delivery mechanism installed) and IEA uses *energy based* definitions of whether fuel use and electricity production is from a CHP (i.e. is it co-produced with heat at a certain efficiency at the tiem of production), one can never get the separate analysis to reproduce the BNA list. All one can hope to achieve is to have the combined CHP and power plant parks in the ETM resemble the combined park from the BNA by technology. The IEA energy balance that needs to be followed mandates the rest.


## Autoproduction CHPs:

- (Agriculture, Households and Services) There are no CHPs in the agriculture, households and services sector.
- (Energy Industry) Unsold heat production is set to appr. 90% to reduce the error in modelled sold heat production. 
- (Energy Industry) The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to: 
    `56.1%`    `0.3%`     `43.6%` 
estimated based on BNA data.
- (Industry) The unsold heat production of gas CHPs is set to 100% and coal CHPs to 99.5% to reduce the error in modelled sold heat production. This setting results in a CRITICAL error because the biofuels allocated to unsold heat production exceeds the biofuels available in the final demand section. Due to the small energy flows, this does not result in problems in following analyses. 
- (Industry) The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to: 
    `56.1%`    `0.3%`     `43.6%` 
estimated based on BNA data.


## Debts

- (Industry) The unsold heat production of gas CHPs is set to 100% and coal CHPs to 99.5% to reduce the error in modelled sold heat production. This setting results in a CRITICAL error because the biofuels allocated to unsold heat production exceeds the biofuels available in the final demand section. Due to the small energy flows, this does not result in problems in following analyses. 