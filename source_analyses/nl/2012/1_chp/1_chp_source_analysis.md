# 1. CHP 

The dashboard assumptions for the first attempt were obtained from the NL 2011 dataset.


The following changes were made:

- For the fuel allocation the Netherlands uses the metoth specified by the IEA statistics manual according to an expert at CBS.
- According to CBS the fuel input in CHPs and the heat production by CHPs are respectivly 590,850 TJ and 225,308 TJ. See [1_chp_source_analysis](1_chp_source_analysis.xlsx).


The following assumptions are made for autoproduction CHPs:

- (Agriculture) According to the IEA there is no sold heat production in the agricultural sector. Furthermore, all CHPs are the 'Gasmotor' type (CBS), so the percentage of CHP electricity from wood pellets is 0%.
- (Households) According to the IEA there are no CHPs in households.
- (Services) According to the IEA there are only biogas CHPs in the Services sector. Since the ETM does not allow biogas CHPs to produce sold heat, there is a mismatch between the modelled sold heat production and the reported sold heat production by IEA.
- (Energy Industry) The unsold heat percentage is set to 0% to reduce the error in modelled sold heat production. The sold heat production is still slightly too low compared what is reported by IEA. This is the result of fixed electricity vs heat efficiencies of the CHPs available in the ETM and the fact that electricity production is leading and heat production by CHPs therefore a result. 
- (Energy Industry) The share of gas turbine CHPs (30.1%), gas engine CHPs (1.1%) and gas combined cycle CHPs (68.8%) are calculated in the [1_chp_source_analysis](1_chp_source_analysis.xlsx).
- (Industry) The unsold heat percentage is set to 65% to reduce the error in modelled sold heat production. The sold heat production is still slightly too low compared what is reported by IEA. See the remark above with Energy Industry.
- (Industry) The share of gas turbine CHPs (30.1%), gas engine CHPs (1.1%) and gas combined cycle CHPs (68.8%) are calculated in the [1_chp_source_analysis.xlsx](1_chp_source_analysis.xlsx).

The full load hours (FLH) are mainly based on data from Energy Matters and considered as constant.


## Debts

- In general, the calculated fuel input for electricity and sold heat production is lower than the reported fuel input.
