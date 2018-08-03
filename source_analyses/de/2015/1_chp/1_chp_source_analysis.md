	# 1. CHP analysis

The dashboard assumptions for the first attempt were obtained from the DE 2012 dataset. Please see [the relevant documentation](../../2012/1_chp/1_chp_source_analysis.md) for that source analysis (be careful, it has the same filename as the one you are reading now!).

## Introduction
The dashboard of the CHP analysis is filled based on enriched data from the German BundesNetzAgentur (BNA). The complete list of power plants and CHPs was obtained from BNA and this was enriched with two columns:
  
  1. One columns to specify each plant's ETM technology using inferred guesses from each power plant's 'Block name' field entry in the BNA list for new plants, and the effort made for the 2012 dataset (which uses a document by the Deutsche Institut für Wirtschaftsforschung (DIW) and).
  - One column which estimates, calculates or looks up each plant's gross capacity (the ETM uses gross not nett capacities). 
   
This information and more is all found in [Capacities_DE_Kraftwerksliste_BNetzA_2018_brutto_Leisting.xlsx](../2_power_and_heat_plant/Capacities_DE_Kraftwerksliste_BNetzA_2018_brutto_Leisting.xlsx), which contains a PivotTable to ouput the relevant information to another analysis step called [de_2012_capacity validation_gross.xlsx](../2_power_and_heat_plant/de_2012_capacity validation_gross.xlsx).

**Filters for PivotTable:**

- **Bundesland**: We excluded all Swiss and Austrian plants from the BNA list, but not the ones from Luxemburg as these are part of the German market.
- **Kraftwerksstatus**: in Betrieb + Endgültig stillgeliegt > 2015  
- **Aufnahme der kommerziellen Stromerzeugung** (Start of commercial operation): < 2016,including all blanks

This last analysis is used for both the CHP analysis (Step 1 of data generation process) and the Power Plant and Heat Plant  analysis, as these cannot really be done separately. Since the BNA's definition of what makes a CHP is *machine based* (i.e. is there a heat delivery mechanism installed) and IEA uses *energy based* definitions of whether fuel use and electricity production is from a CHP (i.e. is it co-produced with heat at a certain efficiency at the time of production), one can never get the separate analysis to reproduce the BNA list. All one can hope to achieve is to have the combined CHP and power plant parks in the ETM resemble the combined park from the BNA by technology. The IEA energy balance that needs to be followed mandates the rest.


## Autoproduction CHPs:

- **Agriculture, Households and Services:** There are no CHPs in the agriculture, households and services sector.
- **Energy Industry:** Unsold heat production is set to appr. 95% to reduce the error in modelled sold heat production. 
- **Energy Industry:** The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to: 
    `89.9%`    `0.0%`     `10.1%` 
estimated based on BNA data.
- **Industry: **The unsold heat production of gas CHPs is set to 100% and coal CHPs to 99.35% to reduce the error in modelled sold heat production.  
- **Industry: **The share of gas turbine CHPs, gas engine CHPs and gas combined cycle CHPs are set to: 
    `43.6%`    `1.2%`     `55.2%` 
estimated based on BNA data.

## Main Activity
Nothing can be set here. The chp_analysis reports too much heat production by Main Activity CHPs, but that is due to the fact that we have not updated the estimated total CHP heat production. See **Debts** below.

## Waste incineration
The Services sector does not contain any heat production. Therefore, it does not make sense to “Remove electricity autoproduction with waste carriers from this sector”.

## FLH
- **Agriculture, Households and Services:** There are no CHPs in the agriculture, households and services sector. Setting FLH to standard for NL
- **Industry & Energy Industry:** Setting all gas CHPs to same FLH.The installed capacities fit nicely with the results obtained from the BNA list. 
- **Main activity and Waste incineration:** the installed capacities do not remotely resemble the installed CHP capacities found in the BNA list. This is due to differing definitions of CHP (see above). The FLH were estimated to what seemed reasonable. The PPHP analysis will make up for the shortfall in capacity. 


## Debts
NICE TO HAVE: 

- Total heat production by CHPs and total CHP fuel input should be retrieved from [Statistisches Bundesamt](https://www.destatis.de/DE/ZahlenFakten/Wirtschaftsbereiche/Energie/Erzeugung/Tabellen/KWKAllVersorgJahr.html) at present this link yields 2017 data and it is unclear how to produce 2015 numbers. Perhaps a BDEW source has something for this.
- Biofuels input for unsold heat: the test reveals a small negative energy flow in cell M16 on the `Delta energy balance` sheet. This is the result of the industry unsold heat percentages. Should not affect further analyses.
