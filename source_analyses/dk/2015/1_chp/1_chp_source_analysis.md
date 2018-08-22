



# 1. CHP\_source\_analysis - README FIRST
dd: 17/08/2018


## Purpose of this source analysis
This source analysis helps you determine the right dashboard values for the `chp_analysis`, the first step in the data generation proces for any country dataset. The `chp_analysis` attempts to specify the energy use and production of CHPs in a country's energy system. All power and heat production that remains in the EB after subtraction of the CHP power and heat by definition is relegated to dedicated power plants and heat plants respectively.

Although the CHP analysis is quite complex, *using* it is not: note that there is not much freedom to change things in the `chp_analysis`. The `results_by_fuel` sheet should have errors as small as possible, but since we have chosen not to allow the adjustment of technical proporties of CHPs, there is little room for manoeuvre. The `results_by_machine` sheets should match the best source (CBS) for installed capacities by fuel and by type. Just follow the steps outlined in `How to use ...` and you will be fine.

This *source* analysis essentially takes all the information [Energinet Analysis Assumption 2017](2017_Energinet_Analysis_Assumptions_2017.xlsx) fuel use and installed CHP capacity per type of technology and per sector and assigns it to the same format as the sheet `Results by machine` found in the `chp_analysis`. **This inevitably differs** from what the `chp_analysis` outputs on this sheet, as CBS uses* machine statistics* whereas the IEA in its Extended Energy Balance uses *energy statistics* to determine whether electricity is produced by a CHP or a power plant. 

- **Machine statistics** essentially treat a plant or device as a CHP if it is determined to be one and henceforth all recorded electricity and heat production is *CHP* electricity and heat production.
- **Energy statistics** only consider electricity to be produced by a CHP if it is produced simultaneoulsy with heat at a total efficiency higher than a certain standard (say 80%).

Although the `1_chp_source_analysis.xlsx` output differs from that of the `chp_analysis`, it is nonetheless useful for comparison between Energinet and IEA. **In the end, however, total installed capacities of power plants and CHPs per technology type is the best one can expect to reproduce after the `chp_analysis` and `pp_hp_analysis` are done.** For more information see: [the power and heat plant source analysis](../2_power_and_heat_plant/2_chp_pp_source_analysis.xlsx) which is an extension of the `1_chp_source_analysis.xlsx`.

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
 
## Assumptions
The following assumptions are made for autoproduction CHPs:
- All the local CHPs have 375 full load hours to reproduce their electritity supply and their estimated capacity of 2.5GW 

## Debts

- Denmark has a very unique energy system with a lot of central CHPs. These CHPs follow a certein heat demand, but can also function as dispatchable unit. In the ETM the central CHPS are dispatachble, which makes it hard to reproduce the this unique situation at this moment. 
- The CHP's technical specs which are fixed in our analysis have a higher efficiency resulting in lower heat supply. This results in 60 PJ of heat production by and heat plants
- Not much information is present about the local CHP's. At this moment the dashboard inputs are set to reproduce the results by fuels as best as possible. This has resulted in maybe unrealistic distributions of CHP type. For example the dataset has no wood pellet CHPs in the Agricultural sector, but does have quite some gas. 
- The energy balance of has Autoproducer oil outside the industry (fuel oil in agriculture 119.99 TJ). The CHP analysis does not (yet) support the autoproducer fuel oil utside the industrial sector. This is not yet accounted for. 
- The biogas CHP electricity production in households and services cannot be sold. This makes it impossible to reach the sold heat stated in the Energy Balance.  


## Sources
### Energinet: 
- By far the most important source for this analysis is the information provided by [Energinet Analysis Assumption 2017](2017_Energinet_Analysis_Assumptions_2017.xlsx) 


