# 0. Preparation of Eurostat data

## Introduction

 This document describes how to prepare the Eurostat energy balance and autoproducer table, so that they can be used as input for the (Research) Analyses that are performed when a country dataset is created. Traditionally, the country dataset creation procedure used the energy balance and autoproducer table from IEA as input for the Analyses, which is why the data from Eurostat needs to be converted to the same format. Some substantial differences exist between both energy balance formats, so it is advised to read this documentation carefully. For the autoproducer table the difference in format is negligible.

## Eurostat Energy Balance

To prepare the energy balance, the following input data is required:

- Eurostat energy balance: Complete energy balances https://doi.org/10.2908/NRG_BAL_C, copy into [Eurostat nrg_bal_c Netherlands 2023 raw.xlsx](./Eurostat nrg_bal_c Netherlands 2023 raw.xlsx)
- Eurosat commodity balance gas: Supply, transformation and consumption of gas https://doi.org/10.2908/NRG_CB_GAS, copy into [Eurostat nrg_cb_gas Netherlands 2023 raw.xlsx](./Eurostat nrg_cb_gas Netherlands 2023 raw.xlsx)
- Eurosat commodity balance oil: Supply, transformation and consumption of oil and petroleum products https://doi.org/10.2908/NRG_CB_OIL, copy into [Eurostat nrg_cb_oil Netherlands 2023 raw.xlsx](./Eurostat nrg_cb_oil Netherlands 2023 raw.xlsx)


The file that handles the conversion is called [0. EB Eurostat to IEA format mapping.xlsx](./0. EB Eurostat to IEA format mapping.xlsx). The input data can be copied directly into the corresponding sheets. The following conversions are done:

- EUROSTAT CB summary: the commodity balances are combined and empty values marked with ":" are set to 0. The share of non-energetic final consumption of chemical and petrochemical industry in total industry is calculated. No manual actions are required in this sheet.
- EUROSTAT EB TJ GWh: for the energy balance empty values marked with ":" are set to 0. The non-energetic final consumption of chemical and petrochemical industry is calculated using the share from the commodity balances. The Gross electricity production flows are converted from TJ to GWh. No manual actions are required in this sheet.
- EUROSTAT EB products IEA: redundant flows are removed and Eurostat products are mapped to IEA products. No manual actions are required in this sheet.
- EUROSTAT EB flows IEA: Eurostat flows are mapped to IEA flows. Note that in the IEA format, some flows are marked with a negative sign. Therefore, the mapping is done with a combination of flows and correspondings signs. For example Flow 1 goes with Sign 1. No manual actions are required in this sheet.
  - The IEA format data has a number of summary product columns that are set to  `x ` to avoid double-counting when the specific data is available
  - Some Analyses in de country dataset generation procedure do not accept `x` as input, which is why a few summary product columns are set to `0`

The sheet `energy_balance` finally provides the data in the format that is required for the ETM analyses. Note that in order to use the energy balance in the ETM analyses, the sheet `energy_balance` needs to be exported to `.csv` format as `energy_balance.csv` and placed in the directory: 

    data / <country_code> / <year> / 1_chp / input 

This directory is automatically created by the `analysis_manager` if you select a new country or new year for which to open the CHP analysis.

## Eurostat Autoproducer Table

To prepare the energy balance, the following input data is required:

- Eurostat autoproducer Electricity: Production of electricity and heat by autoproducers, by type of plant, with SIEC set to Electricity and Unit to GWh, https://doi.org/10.2908/NRG_IND_PEHAP, copy into [Eurostat nrg_ind_pehap electricity GWh Netherlands 2023 raw.xlsx](./Eurostat nrg_ind_pehap electricity GWh Netherlands 2023 raw.xlsx)
- Eurostat autoproducer Heat: Production of electricity and heat by autoproducers, by type of plant, with SIEC set to Heat and Unit to TJ, https://doi.org/10.2908/NRG_IND_PEHAP, copy into [Eurostat nrg_ind_pehap heat TJ Netherlands 2023 raw.xlsx](./Eurostat nrg_ind_pehap heat TJ Netherlands 2023 raw.xlsx)

The file that handles the conversion is called [0. AP Eurostat to IEA format mapping.xlsx](./0. AP Eurostat to IEA format mapping.xlsx). The input data can be copied directly into the corresponding sheets. The following conversions are done:

- EUROSTAT AP plant and products: the autoproducer tables with Electricity in GWh and Heat in TJ are combined into a single table. The plants are mapped to the IEA format. No manual actions are required in this sheet.
- EUROSTAT AP pflows: the flows are mapped to the IEA format. No manual actions are required in this sheet.

The sheet `autoproducer_table` finally provides the data in the format that is required for the ETM analyses. Note that in order to use the autoproducer table in the ETM analyses, the sheet `autoproducer_table` needs to be exported to `.csv` format as `autoproducer_table.csv` and placed in the directory: 


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
