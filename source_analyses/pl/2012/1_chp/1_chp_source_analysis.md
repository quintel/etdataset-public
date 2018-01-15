# 1. CHP 

The energy balance and the Platts data for Poland do not match. Were the Platts database reports a substantial amount of main activity power plants (30,308 MW), the IEA energy balance only reports electricity by main activity CHPs. Therefore, only the installed capacity per commodity is matched based on Platts data for Poland. 

See [pl_2012_installed_capacities.xlsm](../2_power_and_heat_plant/pl_2012_installed_capacities.xlsm).

| Commodity | Power plant capacity | CHP capacity | Total capacity |
| :-------- | -------------------: | -----------: | -------------: |
| Coal      |               26,105 |        5,598 |         31,703 |
| Gas       |                   15 |          765 |            780 |
| Oil       |                  400 |         n.a. |            400 |
| Waste     |                 n.a. |            9 |              9 |
| Hydro     |                1,785 |         n.a. |          1,795 |
| Wind      |                1,750 |         n.a. |          1,750 |


- The fuel allocation method is set to IEA. Research is required on the method that is used in Poland.
- According to [GUS_201310_Energy statistics 2011, 2012](http://refman.et-model.com/publications/1873) the fuel input in "public thermal plants for electricity generation" is 1,318,295.0 TJ; used to produce 527,326.6 TJ electricity. The fuel input in "public thermal plants for heat generation" is 206,084.7 TJ; used to produce 182,833.6 TJ heat.
- According to [GUS_201310_Energy statistics 2011, 2012](http://refman.et-model.com/publications/1873) the fuel input in "autoproducing thermal plants for electricity generation" is 57,025.6 TJ; used to produce 28,147.1 TJ electricity. The fuel input in "public thermal plants for heat generation" is 31,559.6 TJ; used to produce 24,597.5 TJ heat.
- The total input in both the public and autoproducer plants is 1,612,963 TJ. The produced heat is 207,430 TJ.


## Autoproduction CHPs

- (Agriculture) There are only biogas CHPs in agriculture. All shares are set to 100% by default.
- (Households) There are no CHPs in the households sector. All shares are set to 100% by default.
- (Services) There are only biogas CHPs in services sector. All shares are set to 100% by default.
- (Energy Industry) Unsold heat production is reduced to 0% to reduce the error in modelled sold heat production.
- (Industry) Unsold heat production is reduced to 20% to reduce the error in modelled sold heat production.


## Main activity CHPs

The installed capacity based on the default full load hours (FLH) is already in line with the total installed capacities per commodity. The FLH are slightly optimized to match the installed coal capacity. The installed gas capacity exceeds the installed capacity reported by Platts (ETM: 2042 MW, Platts: 780 MW). This deviation cannot be corrected using the FLH.


## Debts

- (Autoproducer CHPs) In general, the calculated fuel input for electricity and sold heat production is lower than the reported fuel input. This might be caused by the generally lower overall efficiencies [(1)](#notes).
- (Main activity CHPs) The calculated fuel input for electricity and sold heat production is lower than the reported fuel input. Furthermore, the calculated sold heat production is higher than the reported sold heat production. Especially for lignite the calculated sold heat production is to high.
- (Main activity CHPs) The installed capacity of gas CHPs exceeds the installed capacity according to Platts (ETM: 2042 MW, Platts: 780 MW).


## Notes

(1) According to the [EEA](http://www.eea.europa.eu/data-and-maps/indicators/combined-heat-and-power-chp-1/combined-heat-and-power-chp-2) there is a large difference between de reported and calculated fuel input of CHPs in Poland. "However, fuel input to CHP plants presents a problem from the statistical reporting.  Whereas CHP electricity generation and CHP heat production provide the CHP output, which are in line with the philosophy of the CHP Directive (2004/8/EC). This requires that a CHP plant’s output is divided into that which is part of the CHP process and that which is not. For the fuel input to CHP this appears not to be the case for all Member States.  The CHP Directive sets a minimum threshold of 75% overall efficiency for the CHP process (lower heating value LHV).  However, for a number of Member States the overall efficiency is very low, for example Slovakia 15.8%, Greece 16.8%, Poland 23.4%, Slovenia 23.1% and Italy 30.8%.")