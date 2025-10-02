# 2. Power and heat plant analysis
dd: 28 May 2025

The [2_chp_pp_source_analysis.xlsx](../2_power_and_heat_plant/2_chp_pp_source_analysis.xlsx) source analysis is the basis for all but some dashboard values used in the `power_and_heat_plant_analysis`. The sheets `PP - CBS Results by machine` and `Power Plants and CHPs compare` in the source analysis are the most important. This source analysis relies heavily on data on heat and electricity generation and production capacity from the Dutch Centraal Bureau voor Statistiek (CBS). 

The aim of the `2_power_and_heat_plant_analysis` is to makes sure the right technologies per fuel type are used by the ETM to produce electricity. The file `2_chp_pp_source_analysis.xlsx` summarizes CBS data in the output formats found on the `chp_analysis` and ` pp_hp_analysis` 'Results by machine' sheets. This makes comparison easier. 

The `Power Plants and CHPs compare` sheet in the `2_chp_pp_source_analysis.xlsx` file provides an overview of results from the 2019 and 2023 `chp_analysis` and `pp_hp_analysis` and the CBS 2023** data. This makes it easier to compare changes between the 2019 and 2023 ETM datasets for NL as well as comparing the 2023 ETM dataset to the numbers reported by CBS for 2023**.

# 1. Power plants

## Coal and Lignite

**The big problem:** CBS does not provide enough information to determine the installed coal-fired power plant capacity, since coal-fired power production occurs in `steam turbines` and this category also includes biomass and gas-fired plants (both natural and coal-gas). It is not easy to determine the exact gas-fired and biomass-fired capacity or production, since no source provides a good split between CHP and PP production for these categories excluding coal-fired production. </br>
I used Wikipedia to determine the installed capacity of coal-fired power plants in the NL. See [Wikipedia - Kolencentrales in NL](https://nl.wikipedia.org/wiki/Kolencentrales_in_Nederland) for more information on where this data came from. 

CBS provides information on power and heat generation (capacity) from *steam turbines*. This includes biomass, waste, coal, coal gas and some natural gas-fired power plants. 

After subtracting coal and co-firing CHP capacity (from the chp_analysis), the `PP - CBS Results by machine` sheet shows that in 2023 **3361 MWe** of coal and co-firing power plants were installed. The power production by these non-CHP plants is determined by adding some rows (in _red italics_ to the `CBS - data 2023 (edited)` sheet) and making assumptions on CHP and non-CHP efficiencies. 

The installed capacity for coal-fired IGCC in NL is known as there is only one plant that was shut down in 2013. Its production share (0%) for coal-fired electricity can be calculated based from CBS numbers (since IGCC or CCGT is reported as a separate category by CBS).

Ultimately, the technology shares on the dashboard of the `2_power_and_heat_plant_analysis.xlsx`are set to reproduce results by fuel. 

## Gas

Power production from gas-fired steam turbines is also determined by adding some rows to the `CBS - data 2023 (edited)` sheet.   

Ultimately, the technology shares for electricity production by gas plants are optimized to match fuel use. The full load hours are optimized to obtain installed capacities as listed in `2_chp_pp_source_analysis.xlsx`. 
Note that there is a deficit of `436.4 MWe` from the CHP analysis to compensate for at least partly with gas-fired capacity (see `2_chp_pp_source_analysis.xlsx`sheet `CHP - CBS Results by machine`cell `N77`). Note also that the `Coal gas combined cycle` capacity of `835 MWe` which was determined from MIDDEN has been subtracted from the CCGT installed capacity according to CBS. Before this plant was included in the ETM in the recent Steel project, no such plant existed and extra gas capacity was assumed to fire the coal gasses from steel production.


## Nuclear
The total primary fuel demand for nuclear power is too high. To fix this, I set the efficiency to 36.83% to exactly match the Eurostat Energy Balance for fuel use on the `Results by fuel` sheet. I set the 3rd gen plant to the same initial efficiency, as this is assumed to have an efficiency at least as good. 

| Technology | Installed capacity (MW) | Efficiency (%) |
| :--------- | ----------------------: | ------: |
| Nuclear 2nd gen   |                      512 |  36.83% |
| Nuclear 3rd gen   |                       0 |    36.83% |

## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. For the Netherlands, this share is easily determined. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production. 

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | -----:| ------: |
| River      |                      37 |  100% |   1,840 |
| Mountain   |                       0 |    0% |   4,492 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx). This is located in the EU source analysis as this analysis covers several EU countries.


## Solar

I used the FLH suggested by the Dutch Begrippenkader RES. The pp_hp_analysis calculated the effective installed capacity based on these and the Eurostat autoproducer table includes information on the sectors solar PV is installed in. For the 2023 dataset update, I did not update the EU analysis or FLH for solar PV. </br>

## Wind

The CBS sources provided in the `2_chp_pp_source_analysis.xlsx` speak for themselves.    
 
## Full load hours
The FLH for power plants are mostly tweaked to optimize installed capacities according to `2_chp_pp_source_analysis.xlsx`. 

# 2. Heat plants
The efficiencies of heat plants were tweaked for better `Results by fuel`. Also, some heat pants that have no installed capacity were changed, because in my opinion their efficiencies are too high. 

It is unclear to me what some of the heater efficiencies are by default. 

## Allocation heat production local district heating/industry
There is a large heat deficit for industry. I made assumptions to minimize the deficit, but could not reduce the deficit to 0. 

**N.B. This results in a shift in installed capacities and new FLHs:** All Gas CCGT CHPs are now found in industry. I do not know if this makes sense and if this results in side effects, because the industrial CHPs use a different fuel mix.  

| Industry and Energy industry Gas CC CHP | 1750 | 3912 | 1229 | 3728 


## Hydrogen production full load hours and demands
The information here is needed for initialization of hydrogen production technologies that are mostly not installed yet. See Sources for the source analysis used. 

## Debts
1. It remains not easy to determine the actually installed capacity of gas-fired and coal-fired steam turbine power plants (supercritical and ultra-supercritical) from the main CBS source. We have approached CBS to split steam turbine power (and heat!) production by carrier or at least by gas-fired vs coal-fired, but this seems to run into some confidentiality issues.
2. The heat plants have a low number of FLH, which is globally fixed
4. The heat deficit in the industrial heat network is partly resolved by shifting Gas CC CHP from Main activity to industry. However, the fact that most CCGT CHPs are now in industry seems wrong. This will likely need to be solved with better assumptions about Refinery gas. We need to check if this results in changed fuel consumption due to fuel mix.
6. We need to create an industrial gas-fired heater for the industrial heat network besides the back-up heater to shift any heat production from local district heat network gas-fired heat plants to. 
 

## Most important sources
- [Hydrogen production technologies](nl/2015/energy/power_and_heat_plant_analysis/hydrogen_solar_pv_p2g)
- See the `2_chp_pp_source_analysis.xlsx`
