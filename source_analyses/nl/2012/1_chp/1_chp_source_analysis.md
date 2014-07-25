# 1. CHP 

The dashboard assumptions for the first attempt were obtained from the NL 2011 dataset.


The following changes were made:

- For the fuel allocation the Netherlands uses the method specified by the IEA statistics manual according to an expert at CBS.
- According to CBS the fuel input in CHPs and the heat production by CHPs are respectivly 590,850 TJ and 225,308 TJ. See [1_chp_source_analysis](1_chp_source_analysis.xlsx).

This analysis essentially takes all the information CBS provides on electricity production, fuel use and installed CHP capacity per type of technology and per sector and assigns it to the same format as the sheet `Results by machine` found in the `chp_analysis`. **This inevitably differs** from what the `chp_analysis` outputs on this sheet, as CBS uses* machine statistics* whereas the IEA in its Extended Energy Balance uses *energy statistics* to determine whether electricity is produced by a CHP or a power plant. 

**Machine statistics** essentially treat a plant or device as a CHP if it is determined to be one and henceforth all recorded electricity and heat production is *CHP* electricity and heat production.

**Energy statistics** only consider electricity to be produced by a CHP if it is produced simultaneoulsy with heat at a total efficiency higher than a certain standard (say 80%).

These two methods do not treat electricity the same way from a power plant that delivers heat to a city heating grid in winter, but runs as a normal power plant in summer. CBS registers all its fuel use, electricity and heat production, etc as coming from a CHP. IEA only registers the fuel consumed and the electricity and heat production in those winter months on the `Main activity producer CHP plants` line in the Energy Balance. The rest is in `Main activity producer electricity plants` line.

The 1_chp_source_analysis.xlsx output is nonetheless useful for comparison between CBS and IEA. In the end, however, total installed capacities of power plants and CHPs per technology type is the best one can expect to reproduce after the `chp_analysis` and `pp_hp_analysis` are done. For more information see: [2_power_and_heat_plant](2_chp_pp_source_analysis.xlsx) which is an extension of the 1_chp_source_analysis.xlsx.

The following assumptions are made for autoproduction CHPs:

- (Agriculture) According to the IEA there is no sold heat production in the agricultural sector. Furthermore, all CHPs are the 'Gasmotor' type (CBS), so the percentage of CHP electricity from wood pellets is 0%.
- (Households) According to the IEA there are no CHPs in households.
- (Services) IEA reports waste incineration as part of the services sector, but in the ETM this is Main Activity. We therefore subtract Waste CHP production from the services sector. Only very little CHP electricity production remains after that.
- (Services) The IEA energy balance states that biogas is used in this sector. The ETM only allows use of biogas (i.e. raw biogas) in dedicated biogas CHPs (which do not seel their heat). Combining this with the fact that little CPH electricity production remains in the SErvices sector, this means there can only be biogas CHPs in the Services sector. Since the ETM does not allow biogas CHPs to produce sold heat, there is a mismatch between the modeled sold heat production and the reported sold heat production by IEA.
- (Energy Industry) The unsold heat percentage is set to 0% to reduce the error in modelled sold heat production. The sold heat production is still slightly too low compared what is reported by IEA. This is the result of fixed electricity vs heat efficiencies of the CHPs available in the ETM and the fact that electricity production is leading and heat production by CHPs therefore a result. 
- (Energy Industry) The share of gas turbine CHPs (594%), gas engine CHPs (1.6%) and gas combined cycle CHPs (39.0%) are calculated in the [1_chp_source_analysis](1_chp_source_analysis.xlsx).
- (Industry) The unsold heat percentage is set to 65% for GT and CCGT and 100% for gas engines to reduce the error in modelled sold heat production. The sold heat production is still slightly too low compared what is reported by IEA. See the remark above with Energy Industry.
- (Industry) The share of gas turbine CHPs (24.8%), gas engine CHPs (1.0%) and gas combined cycle CHPs (74.2%) are calculated in the [1_chp_source_analysis.xlsx](1_chp_source_analysis.xlsx).

The full load hours (FLH) are mainly based on data from Energy Matters and considered as constant. THey have not been changed wrt the 2011 analysis.

## Sources
### CBS: 
- By far the most important source for this analysis is the information provided by the Dutch Centraal Bureau voor Statistiek (CBS) this is found at their [Statline site](http://statline.cbs.nl/StatWeb/publication/?VW=T&DM=SLNL&PA=37823WKK&D1=59,1318&D2=a&D3=a&D4=a&D5=l&HD=1309181425&HDR=G4,T&STB=G1,G2,G3).


## Debts

- In general, the calculated fuel input for electricity and sold heat production is lower than the reported fuel input.
