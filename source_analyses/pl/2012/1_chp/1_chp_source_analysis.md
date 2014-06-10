# 1. CHP 

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


The following changes were made:

- The fuel allocation method is set to IEA. Research is required on the method that is used in Poland.
- According to GUS (2013) the fuel input in "public thermal plants for electricity generation" is 1,318,295.0 TJ; used to produce 527,326.6 TJ electricity. The fuel input in "public thermal plants for heat generation" is 206,084.7 TJ; used to produce 182,833.6 TJ heat.
- According to GUS (2013) the fuel input in "autoproducing thermal plants for electricity generation" is 57,025.6 TJ; used to produce 28,147.1 TJ electricity. The fuel input in "public thermal plants for heat generation" is 31,559.6 TJ; used to produce 24,597.5 TJ heat.
- The total input in both the public and autoproducer plants is 1,612,963 TJ. The produced heat is 207,430 TJ.


The following assumptions are made for autoproduction CHPs:

- (Agriculture) There are only biogas CHPs in agriculture. All shares are set to 100% by default.
- (Households) There are no CHPs in the households sector. All shares are set to 100% by default.
- (Services) There are only biogas CHPs in services sector. All shares are set to 100% by default.
- (Energy Industry) Unsold heat production is reduced to 0% to reduce the error in modelled sold heat production.
- (Industry) Unsold heat production is reduced to 20% to reduce the error in modelled sold heat production.


Potential sources:

- GUS (2013) Energy Statistics 2011-2012
  * Electricity and heat generation in public thermal plants (p. 76-78)
  * Electricity and heat generation in autoproducing thermal plants (p. 78-79)
  * Heat output vs sector and input for autoproducing CHP plants (p. 232)


Issues:

- CHPs are very important in Poland, but also very different (1) compared to other countries. It requires therefore a lot of attention. Currently, there are large % diffrences in the results by fuel. 
- (Autoproducer CHPs) In general, the calculated fuel input for electricity and sold heat production is lower than the reported fuel input. This might be caused by the generally lower overall efficiencies (1).
- (Energy Industry) Percentage of CHP electricity production of gas vs. coal need to be researched.
- (Energy Industry) Shares of gas CHPs need to be researched.
- (Industry) Shares of gas CHPs need to be researched.
- (Main activity CHPs) The calculated fuel input for electricity and sold heat production is lower than the reported fuel input. Furthermore, the calculated sold heat production is higher than the reported sold heat production. Especially for lignite the calculated sold heat production is to high.
- (FLH) Full load hours need to be researched based on installed capacities.

- [SOLVED] (Agriculture) In the agriculture sector the electricity production from biogas (571 TJ, 227%) exceeds the total electricity producting (251 TJ). As a consequence, the electricity production from woodpellets is negative (-320 TJ, -127%). The biogas that is cannot be accounted to agriculture CHPs might be transfered to another sector (still use as CHP) or need to be accounted as greengas (final demand).
- [SOLVED] (Services) In the services sector the electricity production from biogas (3802 TJ TJ, 197%) exceeds the total electricity producting (1934 TJ). As a consequence, the electricity production from woodpellets is negative (-1868 TJ, -97%). Solution idem to agricultural sector.


Notes:

(1) According to http://www.eea.europa.eu/data-and-maps/indicators/combined-heat-and-power-chp-1/combined-heat-and-power-chp-2 there is a large difference between de reported and calculated fuel input of CHPs in Poland. "However, fuel input to CHP plants presents a problem from the statistical reporting.  Whereas CHP electricity generation and CHP heat production provide the CHP output, which are in line with the philosophy of the CHP Directive (2004/8/EC). This requires that a CHP plant’s output is divided into that which is part of the CHP process and that which is not. For the fuel input to CHP this appears not to be the case for all Member States.  The CHP Directive sets a minimum threshold of 75% overall efficiency for the CHP process (lower heating value LHV).  However, for a number of Member States the overall efficiency is very low, for example Slovakia 15.8%, Greece 16.8%, Poland 23.4%, Slovenia 23.1% and Italy 30.8%.")