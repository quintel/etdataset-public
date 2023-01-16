# 1. CHP\_source\_analysis - README FIRST
dd: 14/12/2022 (update after split of local CHPs for agriculture)

## Purpose of this source analysis
This source analysis helps you determine the right dashboard values for the `chp_analysis`, the first step in the data generation proces for any country dataset. The `chp_analysis` attempts to specify the energy use and production of CHPs in a country's energy system. All power and heat production that remains in the EB after subtraction of the CHP power and heat by definition is relegated to dedicated power plants and heat plants respectively.

###Using the `chp_analysis`
Although the CHP analysis is quite complex in structure and it takes a while to understand everything it does, *using* it is not difficult: note that there is not much freedom to change things in the `chp_analysis`. The `results_by_fuel` sheet should have errors as small as possible, but since we have chosen not to allow the adjustment of technical proporties of CHPs, there is little room for manoeuvre. The `results_by_machine` sheets should match the best source (CBS) for installed capacities by fuel and by type. Just follow the steps outlined in `How to use ...` and you will be fine.

###Using the `chp_source_analysis`
This *source* analysis essentially takes all the information CBS provides on electricity production, fuel use and installed CHP capacity per type of technology and per sector and assigns it to the same format as the sheet `Results by machine` found in the `chp_analysis`. **This inevitably differs** from what the `chp_analysis` outputs on this sheet, as CBS uses *machine statistics* whereas the IEA in its Extended Energy Balance uses *energy statistics* to determine whether electricity is produced by a CHP or a power plant. 

- **Machine statistics** essentially treat a plant or device as a CHP if it is determined to be one and henceforth all recorded electricity and heat production is *CHP* electricity and heat production.
- **Energy statistics** only consider electricity to be produced by a CHP if it is produced simultaneoulsy with heat at a total efficiency higher than a certain standard (say 80%).

**Answer (Marek Sturc):** Eurostat treats CHPs the same way as the *national statistical agency* that chooses how to treat CHPs. Eurostat will provide a more detailed table outline exactly what power and heat is produced per unit. In this, they will also specify </br> 
`... of which as CHP`  and </br>
`... of which as PP`

These two methods do not treat electricity the same way from a power plant that delivers heat to a city heating grid in winter, but runs as a normal power plant in summer. **CBS** registers all its fuel use, electricity and heat production, etc as associated with a CHP. **IEA** only registers the fuel consumed and the electricity and heat production in those winter months on the `Main activity producer CHP plants` line in the Energy Balance. The rest is in `Main activity producer electricity plants` line.

Although the `1_chp_source_analysis.xlsx` output differs from that of the `chp_analysis`, it is nonetheless useful for comparison between CBS and IEA. **In the end, however, total installed capacities of power plants and CHPs per technology type is the best one can expect to reproduce after the `chp_analysis` and `pp_hp_analysis` are done.** For more information see: [the power and heat plant source analysis](../2_power_and_heat_plant/2_chp_pp_source_analysis.xlsx) which is an extension of the `1_chp_source_analysis.xlsx`.

## How to use the CHP analysis
0. Make sure you have performed a `git pull` on etsource. Make sure you are using the right branch on etdataset and you have performed a `git pull` there as well
1. Read the `0_preparation_source_analysis.md` in the step `0_preparation` for instructions on how to prepare the input data for the CHP analysis
2. Open the CHP analysis through the `analysis_manager.xlsm` using the macro buttons
3. Import all data and then start tweaking the results using the output of the source analysis 

## How to use the CHP *source* analysis
0. Open the [CHP source analysis](./1_chp_source_analysis.xlsx) in this folder.
1. Update data on the `CBS data 20xx` sheet in the source analysis by downloading and pasting this from CBS (see Sources below)
2. Remove all `-` from empty cells on the `CBS data 20xx` sheet (empty cells can give errors too), in case you get `Value!` errors on `Results by machine`
3. Update `technical_specs` for CHPs from the `chp_analysis` (which in turn imports these from your local etsource repository)
4. Input dashboard values to optimize sold heat on `Results by fuel` and installed capacities on `Results by machine` in the actual `chp_analysis`
   1. First set the `Percentage of el. prod. with waste carriers that is removed from Industry sector` as high as possible without making the IEA result for `Sold heat production` in industry negative. Also try and reproduce the local heat network installed electrical capacity from CBS. The FLH for local and industrial CHPs need to be optimized for installed capacity as well, so this is takes a bit of playing around, but most of the FLH fiddling is done in step 4 below.
   2. Then set the input in `E41` so low that `wood_pellets` demand in industry is as close to zero as possible. If it is too large this will result in coal (and co-firing) CHP installed capacity
   3. Then try and optimize `Results by fuel` sold heat producion and fuel use all around by fiddling with the other dashboard values (see `Assumptions` section in this documentation)
   4. Compare resulting installed capacities according to CBS and according to the `Results by machine` sheet in the `chp_analysis`. Try and optimize `Results by machine` for all sectors (mostly local heat network CHPs, Industry and Main activity) by adjusting the FLH on the dashboard. They should fit the CBS results found in the `chp_source_analysis`. Any mismatch between CBS's machine statistics and IEA's energy statistics should become apparent. **N.B.** For Main activity CHPs the FLH were optimized to reproduce these installed capacities as well as possible, but in the PPHP analysis some CCGT CHP capacity will be shifted from `energy` to `industry` in order to reduce the heat deficit in the industrial heat network.
   5. At the very end, you can tweak efficiencies of CHPs to get better results on `Results by fuel`.  
5. As mentioned before: output *inevitably* differs from CBS

## Changes
The following changes were made w.r.t. the 2015 dataset:

- According to CBS the fuel input in CHPs and the heat production by CHPs are respectivly 502,617 TJ and 174,191 TJ. See [1_chp_source_analysis](1_chp_source_analysis.xlsx).
- The `Percentage of el. prod. with waste carriers` that is removed from Services sector value was changed to 39.45% to optimize `Results by fuel`.
- The percentage of unsold heat in the industry sectors were changed back to 100% to better reproduce sold heat statistics. This is not available for the coal gas CHP, but since this is a dedicated CHP connected to the Steel sector it will not much affect the heat balance for industry. It does result in an ugly `FALSE` for the Industry sector sold heat production. The absolute error is tiny, though.     
- CHP FLH were re-estimated to reproduce the installed capacities reported by CBS's machine statistics. </br>
**N.B.** As an exception, this was not done for Main activity coal and co-firing plants, as these were chosen to represent the 600 MWe of the Amer 9 power plant (see sources). This does not result in large errors for the `power_and_heat_plant_analysis`results. 
- Finally, for some CHPs the efficiencies were tweaked to improve the `Results by fuel`. See below.

 
## Assumptions
The following assumptions are made for autoproduction CHPs:

- **Agriculture:** According to the IEA there is no sold heat production in the agriculture sector. Furthermore, almost all of the CHPs are the 'Gasmotor' type (CBS), so the percentage of CHP electricity from wood pellets is close to 0%. The [1\_chp\_source\_analysis](1_chp_source_analysis.xlsx) calculates its share.
- **Households:** According to the IEA Autoproducer table there are no CHPs in households.
- **Services:** IEA reports waste incineration as part of the services sector, but in the ETM this is Main Activity. We therefore subtract Waste CHP production from the services sector. Less CHP electricity production remains after that. The `chp_analysis` dashboard requires you to assume what percentage of electricity production with waste carriers should be subtracted from the services sector. The subtraction itself occurs on the `fuel_aggregation` sheet in the `chp_analysis`. 
- **Services:** The IEA energy balance states that biogas is used in this sector. The ETM only allows use of biogas (i.e. raw biogas) in dedicated biogas CHPs (whose heat is not sold, but utilized locally). Combining this with the fact that less CHP electricity production remains in the Services sector, this means that a fair bit of the electricity production in this sector must be from biogas CHPs. Since the ETM does not allow biogas CHPs to produce sold heat, there is a mismatch between the modeled sold heat production and the reported sold heat production by IEA.
- **Energy Industry:** The unsold heat percentage is set to 0% to reduce the error in modelled sold heat production. After adjusting the efficiencies, the sold heat production is slightly too high compared what is reported by Eurostat, but the absolute difference is less than 1 PJ. This is the result of the fact our dataset generation procedure takes electricity production to be leading. Consequently heat production by CHPs is  merely a result. 
- **Energy Industry:** The share of gas turbine CHPs (58.9%), gas engine CHPs (0%) and gas combined cycle CHPs (41.1%) are calculated in the [1\_chp\_source\_analysis](1_chp_source_analysis.xlsx).
- **Industry:** The unsold heat percentage is set to 100% for GT and gas engines and 100% for CCGT. This cannot be used to reduce the error in modelled sold heat production, since that is due to coal gas. The sold heat production is still slightly too low compared what is reported by IEA. See the remark above with Energy Industry.
- **Industry:** The share of gas turbine CHPs (21.9%), gas engine CHPs (0.9%) and gas combined cycle CHPs (77.1%) are calculated in the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx).
- **Full load hours:**
  - Agriculture CHPs optimized to match the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx). 
  - Heat network CHPs optimized to match the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx). There is an initial discrepancy between electricity production from the Services sector as reported by CBS and by reported Eurostat. The [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx) shows that according to CBS there was 1,799 TJ electricity produced by CHPs in the Services sector. The `Fuel mixes` sheet in the `chp_analysis` shows that according to Eurostat, w/o waste, there was 9,735 TJ electricity produced by CHPs in the Services sector. This is likely caused by a difference in defition between central/decentral from CBS and main activity/autoproducer in Eurostat. The effect is that, even with 8500 FLHs for the heat network CHPs, the resulting installed capacities for the Gas CHP and Biogas CHP are much higher than what is stated by CBS.
  For the wood pellets CHPs, the installed capacitiy is ~50 MWe too high. This is the result of moving wood pellets out of industry (see step 2 above).
   - Industry & Energy industry CHPs optimized to match the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx). Since the source analysis does not contain the coal gas CHP yet, this was assumed to be included in the total `Gas CC CHP` installed capacity for this sector according to CBS.
   - Main acivity FLH for `coal` and `co-firing` cannot meet the installed capacity in the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx) without having super low FLH. The number in the source analysis is suspect, so I chose to instead set FLH to represent the MWe of the Amer 9 power plant. This is listed as the only coal-fired (and biomass co-firing) CHP in NL. </br>
Also, it is likely that quite a few MWe are in fact gas-fired steam turbine CHPs , which are not available in the ETM. </br>

This means the deficit of 5,385 - 4,147 = 1239 MWe in gas-fired steam turbine CHP capacity **will have to becompensated in `2_chp_pp_analysis.xlsx`. Results by machine** to represent the entire NL power and CHP production park. **This deficit is passed onto the PPHP source analysis.**

### Efficiency adjustments of CHPs
The following CHP-efficiencies were adjusted for better results on the `Results by fuel` sheet. This is done at the very end, since otherwise there are too many variables to play with.

**Adjustments autoproducer CHPs**

| CHP | E-eff default | H-eff default | E-eff NL2019 | H-eff NL2019 |
| :-- | :----------- | -----------: |  ----------: | -----------: |
| Agriculture - Gas CHP | 43% | 47% | 39% | 50% |
| Agriculture - Biogas CHP | 43% | 47% | 42% | 39% |
| Agriculture - Wood pellets CHP | 29% | 82% | 7% | 44% |
| Heat network local - Gas CHP | 43%  | 47% | 39% | 50% | 
| Heat network local - Biogas CHP | 43%  | 47% | 42% | 39% | 
| Heat network local - Wood pellets CHP | 29%  | 82% | 18.3% | 47% | 
| Industry & EI - Gas turbine CHP | 38% | 42% | 27% | 35% | 
| Industry & EI - Gas combined cycle CHP | 46% | 42% | 43.3% | 30.5% | 

Industry Gas CC CHP efficiencies need to be identical to Main activity Gas CC CHPs (see below).
This takes care of the fuel use and sold heat production in all autoproducers, but per sector there are still some deviations. This is mainly in the Industry and Energy industry, due to the fact that E and H-production from `coal_gas` was moved to the industry sector (See `Fuel mixes` and `Industry` sheets and more gas therefore needs to be used there to compensate for the unused `coal_gas`. 

These tweaks do impact the installed heat capacities of the CHPs relative to the installed electric capacities, of course. Since the latter are fixed based on production and FLH, the installed heat capacities change. 

Note that the Biogas CHP for local heat networks cannot be tweaked very well, since its production and fuel use is determined differently from that of other carriers. See the sheets `Fuel mixes` and `Services` for more information. I did tweak a bit however.

**Adjustments main activity and waste incineration CHPs**

| CHP | E-eff default | H-eff default | E-eff NL2019 | H-eff NL2019 |
| :-- | :----------- | -----------: |  ----------: | -----------: |
| Gas combined cycle CHP | 46%  | 42% | 43.3% | 30.5% | 
| Coal CHP | 40%  | 15% | 44% | 13% | 
| Co-firing CHP | 37% | 15% | 40% | 15% | 
| Waste CHP | 27% | 15% | 20.45% | 19.95% | 

This takes care of the worst deficits in fuel use and sold heat production, *except for wood pellets*. Since these are assumed to be co-fired in a fixed ratio to coal in co-firing CHPs, it is hard to lower fuel use of coal (initially it was too high) and at the same time raise fuel use of wood pellets. I have prioritized coal use, as this is important for CO<sub>2</sub>-emissions.


## Sources
### CBS: 
- By far the most important source for this analysis is the information provided by the Dutch Centraal Bureau voor Statistiek (CBS) this is found at their [CBS Statline - Electricity and heat production and means of production](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/37823WKK/table?dl=521AF). 
- [CBS Statline - Electricity and heat production by carrier](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/80030ned/table?dl=52388)
- For the coal fired CHP capacity (Amer 9): [Wikipedia: List of Dutch power plants](https://nl.wikipedia.org/wiki/Lijst_van_elektriciteitscentrales_in_Nederland)

## Debts

- Fuel use of wood pellets in Main activity CHPs is too low as is heat production from wood pellets. This is likely caused by the assumption that wood pellets are always co-fired in CHPs with coal. We probably need to allow for these to be used for direct use of wood pellets in CHPs and heaters.
- In general, the calculated fuel input for electricity and sold heat production is slightly lower than the reported fuel input. This was mostly remedied by changing the efficiencies.
- The removal of electricity and heat production by CHPs that incinerate waste from the Services or Industry sector is an oversimplification. Unfortunately the Autoproducer table does not shed any light onto where waste is incinerated in Autoproducing CHP plants. It cannot all be done in the Services sector, as this does not produce enough power to account for this. Perhaps biogenic waste is also fired in the agriculture and industry sectors (food and tobacco). It might be a good idea to:
  - subtract some biogenic waste powered electricity production by CHPs from the Agriculture and Industry sectors first: biogenic waste should be 54 or 55% of all waste incineration
  - determine the remaining biogenic and non-biogenic waste-fired electricity produciton in CHPs
  - subtract this from the Service sector (check if electricity production is still positive)
  - I am not entirely clear about the impact of moving CHPs from `energy` to `industry` done in the `2_power_and_heat_plant_analysis.xlsx` on energy flows. See the [2_power_and_heat_plant_analysis documentation](../2_power_and_heat_plant/2_power_and_heat_plant_source_analysis.md) for more information.
- In the end the CHP analysis results in a heat surplus on the local district heat network. See [etdataset issue #874](https://github.com/quintel/etdataset/issues/874#issuecomment-882432201). In the PPHP analysis it is possible to shift heat production from CHPs and heat plants to industrial CHPs and heat plants if there is a heat deficit on the industrial heat network (there usually is).
- As discussed under the header "Assumptions > Full load hours" there is a discrepancy between the produced electricity by CHPs in the Services sector as stated by CBS and by Eurostat. We should ask CBS if they have the data used for the [1\_chp\_source\_analysis.xlsx](1_chp_source_analysis.xlsx) in the same format as they provide to Eurostat. This would allow us to better compare installed capacities.
