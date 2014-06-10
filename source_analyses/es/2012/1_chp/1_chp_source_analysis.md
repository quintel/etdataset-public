# 1. CHP 

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


The following changes were made:

- The fuel allocation method is set to IEA. Research is required on the method that is used in Poland.
- According to http://www.eea.europa.eu/data-and-maps/figures/recalculation-of-chp-fuel-input the fuel input to CHP is appr. 110,000 GWh (reported) or appr. 95,000 GWh (calculated) in 2009, corresponding to resp. 393,000 TJ and 336,000 TJ.
- According to http://www.eea.europa.eu/data-and-maps/figures/chp-share-of-total-heat the CHP heat is 172,689 TJ.


The following assumptions are made for autoproduction CHPs:

- (Agriculture) There is no sold heat production. Percentage of heat that is not sold is therefore set to 100%.
- (Households) There are no CHPs in the households sector. Percentage of heat that is not sold is therefore set to 100%.
- (Services) There is no sold heat production.Percentage of heat that is not sold is therefore set to 100%.
- (Industry) There is no sold heat production. Nevertheless, the percentage of heat that is not sold is set to 70% to avoid negative demands in the other industry (as result of the allocation matrix!).
- (Energy Industry) There is no sold heat production. Percentage of heat that is not sold is therefore set to 100%. Shares of gas CHPs are kept on their default value.


Issues:

- (Autoproducer CHPs) In general the calculated fuel input for electricity and sold heat production is lower than the reported fuel input. This might be caused by the generally lower overall efficiencies.
- (Main activity CHPs) There are no main activity CHPs in Spain. Why?
- (Energy Industry) Percentage of CHP electricity production of gas vs. coal need to be researched.
- (Energy Industry) Shares of gas CHPs need to be researched.
- (Industry) Shares of gas CHPs need to be researched.
- (FLH) Full load hours need to be researched based on installed capacities.
