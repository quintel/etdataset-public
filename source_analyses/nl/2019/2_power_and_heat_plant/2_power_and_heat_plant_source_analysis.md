# 2. Power and heat plant analysis

The [2_chp_pp_source_analysis.xlsx](../2_power_and_heat_plant/2_chp_pp_source_analysis.xlsx) source analysis is the basis for all but some dashboard values used in the `power_and_heat_plant_analysis`. The sheets `PP - CBS Results by machine` and `Power Plants and CHPs compare` in the source analysis are the most important. This source analysis relies heavily on data on heat and electricity generation and production capacity from the Dutch Centraal Bureau voor Statistiek (CBS). 

The aim of the `2_power_and_heat_plant_analysis` is to makes sure the right technologies per fuel type are used by the ETM to produce electricity. The file `2_chp_pp_source_analysis.xlsx` summarizes CBS data in the output formats found on the `chp_analysis` and ` pp_hp_analysis` 'Results by machine' sheets. This makes comparison easier. 

The `Power Plants and CHPs compare` sheet in the `2_chp_pp_source_analysis.xlsx` file provides an overview of results from the 2015 and 2019 `chp_analysis` and `pp_hp_analysis` and the CBS 2019* data. This makes it easier to compare changes between the 2015 and 2019 ETM datasets for NL as well as comparing the 2019 ETM dataset to the numbers reported by CBS for 2019*.

# 1. Power plants

## Coal and Lignite

**The big problem:** CBS does not provide enough information to determine the installed coal-fired power plant capacity, since coal-fired power production occurs in `steam turbines` and this category also includes biomass and gas-fired plants (both natural and coal-gas). It is not easy to determine the exact gas-fired and biomass-fired capacity or production, since no source provides a good split between CHP and PP production for these categories excluding coal-fired production. </br>
I used Wikipedia to determine the installed capacity of coal-fired power plants in the NL. See [Wikipedia - Kolencentrales in NL](https://nl.wikipedia.org/wiki/Kolencentrales_in_Nederland) for more information on where this data came from. 

CBS provides information on power and heat generation (capacity) from *steam turbines*. This includes biomass, waste, coal, coal gas and some natural gas-fired power plants. 

After subtracting coal and co-firing CHP capacity (from the chp_analysis), the `PP - CBS Results by machine` sheet shows that in 2019 **3361 MWe** of coal and co-firing power plants were installed. The power production by these non-CHP plants is determined by adding some rows (in _red italics_ to the `CBS - data 2019 (edited)` sheet) and making assumptions on CHP and non-CHP efficiencies. 

The installed capacity for coal-fired IGCC in NL is known as there is only one plant that was shut down in 2013. Its production share (0%) for coal-fired electricity can be calculated based from CBS numbers (since IGCC or CCGT is reported as a separate category by CBS).

Ultimately, the technology shares on the dashboard of the `2_power_and_heat_plant_analysis.xlsx`are set to reproduce results by fuel. **Note that the IEA number for main activity non-CHP coal fired power production is much higher than the CBS number in the source analysis.** 

## Gas

Power production from gas-fired steam turbines is also determined by adding some rows to the `CBS - data 2019 (edited)` sheet.   

Ultimately, the technology shares for electricity production by gas plants are optimized to match fuel use. The full load hours are optimized to obtain installed capacities as listed in `2_chp_pp_source_analysis.xlsx`. Note that there is a deficit of 1238.7 MWe from the CHP analysis to compensate for.

**The question is whether we should compensate for the fact that the CHP analysis uses too little natural gas (mostly for main activity plants) by using more in power plants.**

## Nuclear
The total primary fuel demand for nuclear power is much too high. **This means the assumed efficiency of 32% for the 2nd Gen plant is too low.** To fix this, I set the efficiency to 36.93% to exactly match the Eurostat Energy Balance for fuel use on the `Results by fuel` sheet. I set the 3rd gen plant to the same initial efficiency, as this is assumed to have an efficiency at least as good. 

| Technology | Installed capacity (MW) | Efficiency (%) |
| :--------- | ----------------------: | ------: |
| Nuclear 2nd gen   |                      512 |  36.93% |
| Nuclear 3rd gen   |                       0 |    36.93% |

## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. For the Netherlands, this share is easily determined. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production. 

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | -----:| ------: |
| River      |                      37 |  100% |   2,005 |
| Mountain   |                       0 |    0% |   4,492 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers several EU countries.


## Solar

See [solar_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/solar_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers  several EU countries. This mostly provides an estimate of full load hours. The pp_hp_analysis calculated the effective installed capacity based on these and the IEA autoproducer table includes information on the sectors solar PV is installed in. For the 2019 dataset update, I did not update the EU analysis or FLH for solar PV. </br>
Between 2018 and 2019 the total installed capacity of solar PV in NL leapt from 4.61 to 7.17 GWp (end of year). The resulting installed capacity for 2019 from the analysis with FLH 867 is 6.15 GWp, which is short of the end-of-year capacity, but this is not surprising considering the strong growth in installed capacity during 2019. 

## Wind

The detailed overview of all windparks in the Netherlands in the 2015 `2_chp_pp_source_analysis.xlsx` file was removed, as updating this in order to estimate the split between coastal and inland onshore wind turbines was deemed too much work. Instead, we just assumed the same proportional growth in installed capacity for inland and coastal wind. </br>
CBS provides the total production and installed capacity split between onshore and offshore wind turbines. CBS also provides the installed onshore wind capacities and elecricity production per province. This latter information is used to estimate FLH for inland wind turbines. Coastal wind turbine FLH were readjusted to reproduce installed capacities. The FLH of offshore wind can be calculated directly from the installed capacity, since no offshore parks came online in 2019. 

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | -----:| ------: |
| Coastal    |           1,106        | 25.4% |   2,644 |
| Offshore   |             957        | 31.0% |   3,734 |
| Inland     |           2,421        | 43.5% |   2,069 |
   
 
## Full load hours
The FLH for power plants are mostly tweaked to optimize installed capacities according to 2_chp_pp_source_analysis.xlsx. 

# 2. Heat plants
The efficiencies of heat plants were tweaked for better `Results by fuel`. Also, some heat pants that have no installed capacity were changed, because in my opinion their efficiencies are too high. 

| Heat plant |H-eff default | H-eff NL2019 |
| :--  | ----------: | -----------: |
| Gas heater  | 103% | 91.5% | 
| Oil heater | 72% | 92.4% | 
| Oil heater (industry) | 72% | 92.4% | 
| Waste heater | 105% | 72% | 
| Wood pellets heater| 90% | 80% | 

It is unclear to me what some of the heater efficiencies are by default. 

## Allocation heat production local district heating/industry
There is a large heat deficit for industry. In order to minimize this, I assumed allocation of CCGT CHP to be the following:

| Allocation | Share |
| :----------| ----: |
| Residential heat network CCGT CHP | 0% |
| Industry CHP CCGT fuel mix | 100% |

**N.B. This results in a shift in installed capacities and new FLHs:** All Gas CCGT CHPs are now found in industry. I do not know if this makes sense and if this results in side effects, because the industrial CHPs use a different fuel mix.  

| CHP | FLH CHP analysis | FLH new | Installed heat cap CHP analysis (MW) | Installed heat cap new (MW) |
| :-- | :--------------- | ------------------: |  ------------------: | ------------------: |
| Main activity Gas CC CHP | 4975  | 4975 | 2499 | 0 | 
| Industry and Energy inustry Gas CC CHP | 1925 | 3909 | 1343 | 3842 | 

It also does **not** resolve the entire heat deficit. For now we have decided to fix this by also allowing a heat shift from gas-fired heaters for the local district heat network to industry. 

This results in a negligible remaining heat deficit, and the following changes on top of the ones listed above:

| Heat plant | FLH PPHP analysis (fixed) | Allocation gas burner (%) | Installed heat cap CHP analysis (MW) | Installed heat cap new (MW) |
| :-- | :--------------- |  ------------------: |  ------------------: | ------------------: |
| Main activity Gas heater | 2190 | 56.24 | 1379 | 776 | 
| Industry backup gas heater  | N.A. |  43.76| N.A. | N.A. | 

**N.B.**
Please note that since there is no dedicated gas-fired heater for the industrial heat network, the *backup heater* will need to take up the heat shifted from the residential sector. Since this has a heat surplus [see CHP analysis source analysis MD file](../1_chp/1_chp_source_analysis.md), this ultimately results in a better representation of the actual energy balance. The ETM will still show a deficit on the indutrial heat network though. 


## Hydrogen production full load hours and demands
The information here is needed for initialization of hydrogen production technologies that are mostly not installed yet. See Sources for the source analysis used. 

## Debts
1. It remains not easy to determine the actually installed capacity of gas-fired and coal-fired steam turbine power plants (supercritical and ultra-supercritical) from the main CBS source. We have approached CBS to split steam turbine power (and heat!) production by carrier or at least by gas-fired vs coal-fired, but this seems to run into some confidentiality issues.
2. The heat plants have a low number of FLH, which is globally fixed
3. According to the 2019 Energy Balance, the 32.0% nuclear power plant efficiency is too low for Gen 2, resulting in a 15.4% increase in primary nuclear fuel supply comapred to the Eurostat EB. This was fixed by changing the efficiency. **Should this be done globally?**
4. The heat deficit in the industrial heat network is not resolved entirely by shifting Gas CC CHP from Main activity to industry. This will likely need to be solved with better assumptions about Refinery gas. Also, the fact that all CCGT CHPs are now in industry seems wrong. We need to check if this results in changed fuel consumption due to fuel mix.
5. After all, the CHP and PPHP analyses result in `433.610 PJ`of E production. This corresponds to the sum of the `Electricity output (GWh)` line at the bottom of the energy balance, whereas the `Transformation output` line says it is `435.822 PJ`. The difference is a category of E production which Eurostat cannot allocate to a means of production (see: [this issue](https://github.com/quintel/etdataset/issues/890)). For this reason, we have also decided not to allocate it to anything. As a result, the net import-export balance for E will be 2.21 PJ lower than what the EB says. We have included an `Energy Balance check` on the dashboard of the PPHP analysis, to alert the user to this discrepancy.
6. We need to create an industrial gas-fired heater for the industrial heat network besides the back-up heater to shift any heat production from local district heat network gas-fired heat plants to. 
 

## Most important sources
- [Solar PV installed 2018 and 2019](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/84783NED/table?dl=41EC9)

- [CBS statline - Electricity and heat numbers](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/37823WKK/table?dl=521AF)
- [CSB statline - Electricity and heat production by energy carrier](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/80030ned/table?dl=52388)
- [CBS statline - Wind production numbers](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/82610NED/table?dl=52A59)
- [Overview of all Dutch wind parks](http://www.thewindpower.net/country_zones_en_10_netherlands.php)
- [CBS statline - Installed onshore wind capacities and electricity production per province](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/70960NED/table?dl=52A5B)
- [Hydrogen production technologies](nl/2015/energy/power_and_heat_plant_analysis/hydrogen_solar_pv_p2g)
