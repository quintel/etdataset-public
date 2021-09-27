# 0. Preparation of Eurostat data

## Introduction

 This document describes how to prepare the Eurostat energy balance and autoproducer table, so that they can be used as input for the (Research) Analyses that are performed when a country dataset is created. Traditionally, our country dataset creation procedure used the energy balance and autoproducer table from IEA as input for the Analyses, which is why the data from Eurostat needs to be converted to the same format. Some substantial differences exist between both energy balance formats, so it is advised to read this documentation carefully. For the autoproducer table the difference in format is negligible.

 The file that handles the conversion is called [nl 2019 - EUROSTAT to ETM - EB AP.xlsx](./nl 2019 - EUROSTAT to ETM - EB AP.xlsx), denoted here as the "conversion file".

## Eurostat Commodity Balance Oil and Commodity Balance Gas

Download Eurostat Commodity Balance Oil and Commodity Balance Gas:

- Go to: [https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/main-tables](https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/main-tables)
- Use keyword `NRG_CB_OIL` to open Data Browser for oil
- Use keyword `NRG_CB_GAS` to open Data Browser for gas
- Select `country` and `year of interest` as page
- Select all `Energy balance` products as columns
- Select flows as rows: final consumption - non-energy use and final consumption - industry sector - chemical and petrochemical - non-energy use
- Download datasheets
- Paste Oil data into sheet `EUROSTAT CB OIL`
- Paste Gas data into sheet `EUROSTAT CB GAS`
- **Make sure that the flows and product labels of the pasted data matches the structured data at the bottom of the sheet**

These commodity balances are used to calculate the ratio between total non-energy use in final consumption and non-energy in final consumption by the chemical and petrochemical industry. This ratio is then multiplied with the total non-energy use in the energy balance to give 'Memo: Non-energy use chemical/petrochemical'.
It is only done for oil and gas products, since only these products have non-energy use in the chemical/petrochemical industry, all other products are set to `0`.

## Eurostat Energy Balance

Download Eurostat Energy Balances:

1. Go to: [https://ec.europa.eu/eurostat/web/energy/data/energy-balances](https://ec.europa.eu/eurostat/web/energy/data/energy-balances)
- Select the file for country of interest, select the sheet for year of interest
- Paste sheet data into the sheet `EUROSTAT EB ktoe` of the conversion file
- The rows of the balance are called `flows`, the columns are called `products`
- The data pasted into the sheet 'EUROSTAT EB ktoe' is then converted from ktoe to TJ and GWh in the 'EUROSTAT EB TJ GWh' sheet. Unique labels are added to the flows in this sheet, the products labels are already unique.
- **N.B.: Make sure that the flows and product labels of the pasted data in 'EUROSTAT EB ktoe' match this format**

The conversion file maps the unique flows and products labels from Eurostat to corresponding IEA format labels in the 'EUROSTAT EB conversion IEA' sheet. This mapping has been done by comparing the documentation of Eurostat and IEA definitions. Supplementary information on definitions from Eurostat can be found on [https://ec.europa.eu/eurostat/ramon/](https://ec.europa.eu/eurostat/ramon/).

`+` or `-` signs are added to the sheet:

- `Export`, `International maritime bunkers`, `International aviation` are marked as negative because the Eurostat data has a column with algebraic signs, in which these are already marked negative
- Transformation outputs are marked as negative because the IEA format uses transformation processes, which is the net result of transformation input and transformation output
- Stock changes are marked as negative because this matched with the difference between the top-down calculation of final demand and the bottom-up calculation of final demand

Using the algebraic signs and the unique labels, the Eurostat format data is read from `EUROSTAT EB TJ GWh` and automatically converted to IEA format data in `EUROSTAT EB conversion IEA`. No manual actions are required in this sheet.

- The IEA format data has a number of summary product columns that are set to  `x ` to avoid double-counting when the specific data is available
- Some Analyses in de country dataset generation procedure do not accept `x` as input, which is why a few summary product columns are set to `0`

The sheet `EUROSTAT EB format IEA` finally reads out the data from `EUROSTAT EB conversion IEA` that is necessary for the ETM analyses. Note that in order to use the energy balance in the ETM analyses, the sheet `EUROSTAT EB format IEA` needs to be exported to `.csv` format as `energy_balance.csv` and placed in the directory: 


    data / <country_code> / <year> / 1_chp / input 

This directory is automatically created by the `analysis_manager` if you select a new country or new year for which to open the CHP analysis.

## Eurostat Autoproducer table

Download Eurostat Autoproducer table: 

- [https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/main-tables](https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/main-tables)
- Use keyword `NRG_IND_PEHAP` to open Data Browser
- Select `country` and `year of interest` as page
- Select all `Energy balance` products as columns
- Select all `SIEC` as rows with all `Type of plants` as subrows
- Download datasheet with GWh selected as `Unit of measure`
- Paste GWh data into sheet EUROSTAT AP table GWh
- Download datasheet with TJ selected as `Unit of measure`
- Paste TJ data into sheet `EUROSTAT AP table TJ`

Here is the [direct link](https://ec.europa.eu/eurostat/databrowser/bookmark/3683e491-c52f-4475-b691-c87a17febf0f?lang=en&page=time:2015) to this table. However, it is not sure if this link stays available.

The sheets `EUROSTAT AP table GWh` and `EUROSTAT AP table TJ` are combined to a single autoproducer table in the sheet `EUROSTAT AP table TJ GWh`. In the sheet `EUROSTAT AP conversion IEA` the Eurostat data format is converted to the IEA data format. 

The sheet `EUROSTAT AP format IEA` finally reads out the data from  `EUROSTAT AP conversion IEA` that is necessary for the ETM analyses. Note that in order to use the autoproducer table in the ETM analyses, the sheet `EUROSTAT AP format IEA` needs to be exported to `.csv` format as `autoproducer_table.csv` and placed in the directory: 


    data / <country_code> / <year> / 1_chp / input 

This directory is automatically created by the `analysis_manager` if you select a new country or new year for which to open the CHP analysis.

## Debts

### Differences in notation Eurostat and IEA

- Transformation processes: Eurostat has both transformation proces input and output, instead of the net result of transformation processes. **Debt:** change ETM analyses so that additional information can be used.
- Transfers: Eurostat has specific flows for backflows and products transferred input and output, and recovered and recycled products instead of a single flow 'Transfers'. **Debt:** further investigate and improve modelling of the (petro)chemical industry based on additional information.
- Oil refineries: Eurostat has specific flows under Refineries & petrochemical industry, instead of a seperate flow for Oil refineries alone. **Debt:** further investigate and improve modelling of the (petro)chemical industry based on additional information.
- Petrochemical industry: Eurostat has specific flows under Refineries & petrochemical industry, instead of a seperate flow for Oil refineries alone. **Debt:** further investigate and improve modelling of the (petro)chemical industry based on additional information.
- Chemical heat for electricity production: Eurostat has derived heat for electricity production as transformation input and other sources as transformation output. **Debt:** discussion with Eurostat has made it clear that allocating this input and output to the transformation process "Chemical heat for electricitiy production" is not correct. A different approach has to be found for this (see: [this issue](https://github.com/quintel/etdataset/issues/890)).

### Additional data Eurostat

At some point we will want to make use of the additional information that is found in the Eurostat Energy Balance w.r.t. the IEA energy balance. Some are listed below:

- Flow: Transformation input: liquid biofuels blended
- Flow: Transformation output: liquid biofuels blended
- Product: Peat and peat products
- Product: Oil shale and oil sands
- Product: Blended biogasoline
- Product: Blended biodiesels
- Product: Pure bio jet kerosene
- Product: Blended bio jet kerosene
- Product: Ambient heat (heat pumps)
- **Debt:** decide how this additional data can be used.

### Missing data Eurostat
- Product: Other sources
- **Debt:** allocate these other sources when more information about their origin is known. Currently this is not the case (see: [this issue](https://github.com/quintel/etdataset/issues/890)). It leads to a deficit in the total electricity production determined by the power and heat plant analysis.