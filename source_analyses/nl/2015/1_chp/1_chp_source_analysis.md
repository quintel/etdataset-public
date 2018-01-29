# 1. CHP\_source\_analysis - README FIRST
dd: 08/09/2017

## Purpose of this source analysis
This source analysis helps you determine the right dashboard values for the `chp_analysis`, the first step in the data generation proces for any country dataset. The `chp_analysis` attempts to specify the energy use and production of CHPs in a country's energy system. All power and heat production that remains in the EB after subtraction of the CHP power and heat by definition is relegated to dedicated power plants and heat plants respectively.

Although the CHP analysis is quite complex, *using* it is not: note that there is not much freedom to change things in the `chp_analysis`. The `results_by_fuel` sheet should have errors as small as possible, but since we have chosen not to allow the adjustment of technical proporties of CHPs, there is little room for manoeuvre. The `results_by_machine` sheets should match the best source (CBS) for installed capacities by fuel and by type. Just follow the steps outlined in `How to use ...` and you will be fine.

This *source* analysis essentially takes all the information CBS provides on electricity production, fuel use and installed CHP capacity per type of technology and per sector and assigns it to the same format as the sheet `Results by machine` found in the `chp_analysis`. **This inevitably differs** from what the `chp_analysis` outputs on this sheet, as CBS uses* machine statistics* whereas the IEA in its Extended Energy Balance uses *energy statistics* to determine whether electricity is produced by a CHP or a power plant. 

- **Machine statistics** essentially treat a plant or device as a CHP if it is determined to be one and henceforth all recorded electricity and heat production is *CHP* electricity and heat production.
- **Energy statistics** only consider electricity to be produced by a CHP if it is produced simultaneoulsy with heat at a total efficiency higher than a certain standard (say 80%).

These two methods do not treat electricity the same way from a power plant that delivers heat to a city heating grid in winter, but runs as a normal power plant in summer. **CBS** registers all its fuel use, electricity and heat production, etc as associated with a CHP. **IEA** only registers the fuel consumed and the electricity and heat production in those winter months on the `Main activity producer CHP plants` line in the Energy Balance. The rest is in `Main activity producer electricity plants` line.

Although the `1_chp_source_analysis.xlsx` output differs from that of the `chp_analysis`, it is nonetheless useful for comparison between CBS and IEA. **In the end, however, total installed capacities of power plants and CHPs per technology type is the best one can expect to reproduce after the `chp_analysis` and `pp_hp_analysis` are done.** For more information see: [the power and heat plant source analysis](../2_power_and_heat_plant/2_chp_pp_source_analysis.xlsx) which is an extension of the `1_chp_source_analysis.xlsx`.

## How to use the CHP analysis
0. Make sure you have performed a `git up` on etsource. Make sure you are using the right branch on etdataset and you have performed a `git up` there as well
1. Read the `0_preparation_source_analysis.md` in the step `0_preparation` for instructions on how to prepare the input data for the CHP analysis
2. Open the CHP analysis through the `analysis_manager.xlsm` using the macro buttons
3. Import all data and then start tweaking the results using the output of the source analysis 

## How to use this source analysis
1. Update data on the `CBS data 20xx` sheet in the source analysis by downloading and pasting this from CBS (see Sources below)
2. Remove all `-` from empty cells on the `CBS data 20xx` sheet (empty cells can give errors too), in case you get `Value!` errors on `Results by machine`
3. Update `technical_specs` for CHPs from the `chp_analysis` (which in turn imports these from your local etsource repository)
4. Input dashboard values to optimize sold heat on `Results by fuel` and installed capacities on `Results by machine` in the `chp_analysis`
   1. First set the `Percentage of el. prod. with waste carriers that is removed from Services and Industry sectors` so that `Sold heat production` in industry is non-negative. Also try and reproduce the Services sector installed electrical capacity from CBS. The FLH for industrial CHPs need to be optimized for installed capacity, but that option is not logical in the Services sector so I determined it is best to fix capacities for Services here.
   2. Then set the input in `E41` so that `wood_pellets` demand in industry is as close to zero as possible. If it is too large this will result in coal (and co-firing) CHP installed capacity
   3. Then try and optimize `Results by fuel` sold heat producion and fuel use all around by fiddling with the other dashboard values (see `Assumptions` section in this documentation)
   4. Compare resulting installed capacities according to CBS and according to the `Results by machine` sheet in the `chp_analysis`. Try and optimize `Results by machine` for all sectors (mostly Agriculture, Industry and Main activity, changing FLH for Services is not so logical as these are must-run CHPs) by adjusting the FLH on the dashboard. They should fit the CBS results found in the `chp_source_analysis`. Any mismatch between CBS's machine statistics and IEA's energy statistics should become apparent.
5. As mentioned before: output inevitably differs from CBS

## Changes
The following changes were made w.r.t. the 2013 dataset:

- According to CBS the fuel input in CHPs and the heat production by CHPs are respectivly 499,940 TJ and 191,950 TJ. See [1_chp_source_analysis](1_chp_source_analysis.xlsx).
- The `Percentage of el. prod. with waste carriers that is removed from Services sector` value was changed to 93.4%, to optimize `Results by fuel`.
- The percentage of unsold heat in the industry sectors were changed slightly to better reproduce sold heat statistics    
- CHP FLH were re-estimated to reproduce the installed capacities reported by CBS's machine statistics. This does not result in large errors for the `power_and_heat_plant_analysis`results. 

 
## Assumptions
The following assumptions are made for autoproduction CHPs:

- **Agriculture:** According to the IEA there is no sold heat production in the agriculture sector. Furthermore, all CHPs are the 'Gasmotor' type (CBS), so the percentage of CHP electricity from wood pellets is 0%.
- **Households:** According to the IEA Autoproducer table there are no CHPs in households.
- **Services:** IEA reports waste incineration as part of the services sector, but in the ETM this is Main Activity. We therefore subtract Waste CHP production from the services sector. Only very little CHP electricity production remains after that. The `chp_analysis` dashboard requires you to assume what percentage of electricity production with waste carriers should be subtracted from the services sector. The subtraction itself occurs on the `fuel_aggregation` sheet in the `chp_analysis`. 
- **Services:** The IEA energy balance states that biogas is used in this sector. The ETM only allows use of biogas (i.e. raw biogas) in dedicated biogas CHPs (whose heat is not sold, but utilized locally). Combining this with the fact that little CPH electricity production remains in the Services sector, this means that almost all electricity production in this sector must be from biogas CHPs. Since the ETM does not allow biogas CHPs to produce sold heat, there is a mismatch between the modeled sold heat production and the reported sold heat production by IEA.
- **Energy Industry:** The unsold heat percentage is set to 0% to reduce the error in modelled sold heat production. The sold heat production is still slightly too low compared what is reported by IEA. This is the result of fixed electricity vs heat efficiencies of the CHPs available in the ETM and the fact our dataset generation procedure takes electricity production to be leading. Consequently heat production by CHPs is  merely a result. 
- **Energy Industry:** The share of gas turbine CHPs (56%), gas engine CHPs (2%) and gas combined cycle CHPs (43%) are calculated in the [1\_chp\_source\_analysis](1_chp_source_analysis.xlsx).
- **Industry:** The unsold heat percentage is set to 100% for GT and gas engines and 98% for CCGT to reduce the error in modelled sold heat production. The sold heat production is still slightly too low compared what is reported by IEA. See the remark above with Energy Industry.
- **Industry:** The share of gas turbine CHPs (26%), gas engine CHPs (1.0%) and gas combined cycle CHPs (73%) are calculated in the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx).



## Sources
### CBS: 
- By far the most important source for this analysis is the information provided by the Dutch Centraal Bureau voor Statistiek (CBS) this is found at their [Statline site](http://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=37823WKK&D1=5-9,13-18&D2=a&D3=a&D4=a&D5=l&HDR=G4,T&STB=G1,G2,G3&VW=T).


## Debts

- The sold heat deficit is quite large (26 PJ) and half of this comes from the waste incineration CHPs. There is nothing you can do about this, as it results directly from the energy balance and the heat and el. efficiencies of the CHP. Another large contributor are Main Activity plants, but this has the same cause and cannot be improved here. It probably reflects the face that these plants have flexible el. and heat efficiency ratios in reality, whereas in the ETM they they fixed ones. This deficit is passed on to the PP&HP analysis, where dedicated heat plants will generate the heat needed without producing electricity.   
- In general, the calculated fuel input for electricity and sold heat production is lower than the reported fuel input.
- The removal of electricity and heat production by CHPs that incinerate waste from the Services or Industry sector is an oversimplification. Unfortunately the Autoproducer table does not shed any light onto where waste is incinerated in Autoproducing CHP plants. It cannot all be done in the Services sector, as this does not produce enough power to account for this. Perhaps biogenic waste is also fired in the agriculture and industry sectors (food and tobacco). It might be a good idea to:
  - subtract some biogenic waste powered electricity production by CHPs from the Agriculture and Industry sectors first: biogenic waste should be 54 or 55% of all waste incineration
  - determine the remaining biogenic and non-biogenic waste-fired electricity produciton in CHPs
  - subtract this from the Service sector (check if electricity production is still positive)
