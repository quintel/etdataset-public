# 1. CHP analysis


The following decisions were made on the dashboard:

- It is not known which CHP fuel allocation method is used for the IEA EU-27 energy balance. It is decided to choose the "IEA" fuel allocation method.

- According to http://www.eea.europa.eu/data-and-maps/figures/chp-share-of-total-heat the CHP share of total heat generation in EU is 15.2% in 2009.
- According to http://www.eea.europa.eu/data-and-maps/figures/recalculation-of-chp-fuel-input the fuel input to CHP is appr. 2,284,170 GWh in 2009, corresponding to 8,223,012 TJ.
- According to http://www.eea.europa.eu/data-and-maps/figures/chp-share-of-total-heat the CHP heat is 2,926,488 TJ


The following assumptions are made for autoproduction CHPs:

- (Agriculture) The unsold heat percentage is set to 99.65% to reduce errors in modelled sold heat production. It is assumed that 70% of the remaining electricity production is by gas CHPs and 30% by wood pellet CHPs. 
- (Households) The unsold heat percentage is set to 60% to reduce errors in modelled sold heat production. It is assumed that 70% of the remaining electricity production is by gas CHPs and 30% by wood pellet CHPs. 
- (Services) The unsold heat percentage is set to 0% to reduce errors in modelled sold heat production. IEA reports more sold heat in this sector than the analysis calculates. The check "The modeled sold heat production matches the statistical data (±5%)" cannot be matched. It is assumed that 70% of the remaining electricity production is by gas CHPs and 30% by wood pellet CHPs.
- (Energy Industry) The unsold heat percentage is set to 47% to reduce errors in modelled sold heat production. It is assumed that 90% of the electricity is produced by gas CHPs and 10% by coal CHPs. 
- (Energy Industry) The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to resp. 31.2%, 2.7% and 66.1%, estimated based on Platts data.
- (Industry) The unsold heat percentage is set to 69.5% to reduce errors in modelled sold heat production.
- (Industry) The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to resp. 31.2%, 2.7% and 66.1%, estimated based on Platts data.
- (Waste incineration) "Remove electricity autoproduction with waste carriers from this sector" is set to 'Services". (Setting it to "Industry" does not improve the checks significantly. Choosing "Services" seems to be the better choice since waste incineration is more likely to take place in an industrial than in a "Commercial and public services" sector).

See [eu_2011_installed_capacities.xlsm](../2_power_and_heat_plant/eu_2011_installed_capacities.xlsm).


## Depts

- Generally, the fuel input for electricity and sold heat production is too low. This indicates that the the CHPs in the EU might have lower efficiencies than those defined in the ETM.
- The fuel allocation method should be researched.
- (Services) The sold heat production in the services sector is not sufficient. The CHPs in the EU might have a lower electrical efficiency than those defined in the ETM.
