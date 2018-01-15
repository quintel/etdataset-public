# 1. CHP analysis

The following decisions were made on the dashboard:


## Technology splits

1. Germany uses the `Protermo` fuel allocation method to report CHP statistics. This information is found on page 9 of the [AGEB_201008_Preface to the energy balances](http://refman.et-model.com/publications/1845) file. There it is referred to as 'the Finnish method'.
* Total heat production by CHPs: Based on [Statistisches Bundesamt](https://www.destatis.de/DE/ZahlenFakten/Wirtschaftsbereiche/Energie/Erzeugung/Tabellen/KWKAllVersorgJahr.html), the total CHP heat production is set to  345,414 TJ.
* Based on an assumed average CHP heat efficiency of 35% (compare technical_specs sheet), the total heat production is converted to 986,897 TJ total fuel input.
* The Agriculture, Households and Services sectors are not relevant for DE when it comes to CHPs. Shares are set to 100%, but do not have any effect. The reason is that the 'autoproducer table' has no production by autoproducer CHPs in these sectors. Note that we are not convinced the IEA autoproducer table is all correct.
* The Services sector does not contain any heat production. Therefore, it does not make sense to “Remove electricity autoproduction with waste carriers from this sector”.
* Shares for the Energy industry and Energy sectors:
 * The share group at the top is adjusted to best fit the checks on the results sheets
 * The 'Percentage of CHP electricity production...' cells are not changed and filled with NL values
* Waste incineration: "Remove electricity autoproduction with waste carriers from this sector" is set to 'Industry". (no energy use in Services, see above)


## Checks

1. in the Services sector, the check "The modeled sold heat production matches the statistical data (±5%)" fails. This is due to an inconsistency within the autoproducer table itself. While the 'Commercial and public service' and 'Non-specified - other' cells do not report any electricity production in CHPs, the autoproducer claims that these sectors do produce about 7 PJ heat via CHPs. This is a contradiction and cannot be solved easily. --> One could manipulate the autoproducer table and claim that the heat must then be produced by heat plants, instead of CHP. Or one introduces a certain amount of electricity production by CHP....
* Several checks in the 'results' section fail.
  * 'Total fuel input matches the indicated fuel input (±5%)' fails because of differing global ETM converter efficiencies and average German CHPs. This problem cannot be fixed easily. One would have to introduce a series of new converters that have slightly different efficiencies (as it is done in the PP_HP analysis, where coal can be burnt in plants with different efficiencies).
  * The checks 'Total sold heat production matches the indicated heat production (±5%)', 'Mismatch in Autoproducers Sector. Number of differences to IEA data larger than 5%' and 'Mismatch in Main activity and Waste sector. Number of differences to IEA data larger than 5%' also fail because of differing CHP efficiencies.
  * The last check fails because the correction of the energy balance leads to negative final demands for some carriers. This problem is caused by the CHP analysis. It can most likely not be solved by changing country specific assumptions.


## Full Load hours

All FLH are taken from the NL dataset without further source analyses. Note that this is not likely to be correct as mostly the area formerly known as DDR makes more extensive use of CHP for city grid heating than anywhere in the Netherlands. Only the following changes are visible:
 * Industry & Energy industry / Coal CHP has 5000 FLH instead of 7000
 * Main activity / Coal CHP has 4000 FLH instead of 4500