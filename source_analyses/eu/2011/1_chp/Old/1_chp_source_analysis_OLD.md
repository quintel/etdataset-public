# 1. CHP analysis

The following decisions were made on the dashboard:


## Technology splits

1. It is not known which CHP fuel allocation method is used for the IEA EU27 energy balance. It is decided to choose the "IEA" fuel allocation method. See: documentation on 'introduction' sheet in the 'chp analysis' Excel file for more information on fuel allocation methods.
* Total heat production by CHPs is not known. A dummy number of 10,000,000 TJ is filled in. This value does not actually influence the analysis, but it should be improved.
* The total heat production is set to a dummy number of 20,000,000 TJ. This value does not actually influence the analysis, but it should be improved.
* Agriculture sector: Only the fuels *gas* and *biogas* are relevant for the agriculture sector. The cell "Percentage of heat from wood pellet CHPs that is not sold" is not relevant. The cell "Percentage of remaining CHP electricity production by gas CHPs" has to be set to 100%, otherwise a critical check fails. The only remaining cell "Percentage of heat from gas CHPs that is not sold" is adjusted to make the dashboard check "The modeled sold heat production matches the statistical data (±5%)" pass.
* Household sector: Similar to Agriculture sector. *Wood pellets* are not relevant, and "Percentage of remaining CHP electricity production by gas CHPs" has to be set to 100%, otherwise a critical check fails. "Percentage of heat from gas CHPs that is not sold" is adjusted to optimise the check "The modeled sold heat production matches the statistical data (±5%)".
* Services Sector: "Percentage of heat from wood pellet CHPs that is not sold" is not relevant, while "Percentage of remaining CHP electricity production by gas CHPs" has to be set to 100% (critical check). "Percentage of heat from gas CHPs that is not sold" is set to 0%. IEA reports more sold heat in this sector than the analysis calculates. The check "The modeled sold heat production matches the statistical data (±5%)" cannot be matched.
* Energy Industry Sector: It is assumed that coal CHPs sell all their heat production in this sector ("Percentage of heat from coal CHPs that is not sold" = 0%). It is further assumed that "Percentage of CHP electricity production of gas vs. coal in energy industry CHPs" = 90% (no source). The last three cells in the industry sector ("Percentage of CHP electricity production by gas turbine", "... gas engine" and "... gas combined cycle CHPs") provides a breakdown for gas-fuelled CHPs. These cells are filled with figures from the NL dataset, because of lacking EU data. The remaining cells ("Percentage of heat from gas turbine", "... gas engine" and "... gas combined cycle CHPs") are set in the following way: It is assumed that all three percentages are of the same magnitude (assumption, no data available). They are adjusted until the check "The modeled sold heat production matches the statistical data (±5%)" is optimised.
* Industry Sector: This sector filled in in the same order as the Energy Industry sector: First, the "Percentage of heat from coal CHPs that is not sold" is set to 0% (Assumption: Coal CHPs in Industry do not sell heat). Second, the percentages of CHP electricity production by gas turbine, gas engine and gas combined cycle CHPs are set to NL figures (no EU data available). Third, the Percentages of heat from gas turbine, gas engine and gas combined cycle CHPs are set to equal numbers and adjusted until the check "The modeled sold heat production matches the statistical data (±5%)" is optimised.
* Waste incineration: "Remove electricity autoproduction with waste carriers from this sector" is set to 'Services". (Setting it to "Industry" does not improve the checks significantly. Choosing "Services" seems to be the better choice since waste incineration is more likely to take place in an industrial than in a "commercial and public services" sector).


## Checks

1. in the Services sector, the check "The modeled sold heat production matches the statistical data (±5%)" fails. This is caused directly by the figures provided by the autoproducer table. Autoproducer CHP plants produce both heat and electricity. To match the average electric and heat efficiency (ratio of heat/power production) reported by IEA, the Services Sector only has two CHPs to choose from (in the CHP analysis). It is not possible to match the heat efficiency that is suggested in the autoproducer table. Therefore, the check fails.
* Several checks in the 'results' section fail:
 - 'Total fuel input matches the indicated fuel input (±5%)' fails because of differing ETM converter and  EU CHPs efficiencies. This problem cannot be fixed easily. One would have to introduce a series of new converters that have slightly different efficiencies (as it is done in the PP_HP analysis, where coal can be burnt in plants with different efficiencies).
 - The checks "Total sold heat production matches the indicated heat production (±5%)", "Mismatch in Autoproducers Sector. Number of differences to IEA data larger than 5%" and "Mismatch in Main activity and Waste sector. Number of differences to IEA data larger than 5%" also fail because of differing CHP efficiencies.
 * The last check fails because the correction of the energy balance leads to negative final demands for some carriers. This problem is caused by the CHP analysis. It can most likely not be solved by changing country specific assumptions.


## Full Load hours

All FLH are taken from the NL dataset without further source analyses.
There is very little data available on the installed capacity of CHPs in the EU-27 countries. This decision only affects he installed capacities for each type (and hence investment costs, etc). It has no impact on the energy flows.
A report by Prognos was found that forecasts installed capacity of power plants (they build scenarios to evaluate the future role of coal in the energy mix). See: [Prognos: The future role of coal in europe](http://www.euracoal.be/componenten/download.php?filedata=1208519374.pdf&filename=prognos_FutureCoal_070822_final_kurz.pdf&mimetype=application/pdf). On page 119, they provide figures for the installed capacities and annual production of gas CHPs for the year 2010:

| Technology | Capacity (MW) | Production (GWh) | FLH (h)     |
| :----------| ------------: | ---------------: | ----------: |
| Gas CHPs   |        42,235 |          385,323 | ***9,123*** |

The provided numbers result in FLH *above 8760*!
This issue is being discussed on Github, see [https://github.com/quintel/etdataset/issues/348](https://github.com/quintel/etdataset/issues/348).

As a temporary solution, all gas CHP FLH are set to 8000 h, which seems very large, but yields about 45 GW installed capacity.


## Potential sources

[Eurolectric: "Power Statistics & Trends 2011 full report"](http://refman.et-model.com/publications/1836) also published data addressing CHPs, but it is not complete and time-consuming to evaluate (there is no EU27 table, but only data for individual countries).


## Depts

- Which CHP allocation method is used? We chose IEA without a proper source telling us to do so.
- THe CHP analysis should be validated based on the Platts data for the EU.
