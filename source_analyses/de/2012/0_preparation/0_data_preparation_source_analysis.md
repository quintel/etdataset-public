<!--
  Comment: a confidential version of this source analysis is stored with the IEA data tables of the EU. That confidential version contains actual numbers, which cannot be published, but make the documentation more transparent.
-->

# 0. Preparation of IEA data

IEA data tables are obtained via [http://data.iea.org/ieastore/default.asp](http://data.iea.org/ieastore/default.asp). All IEA data used for the DE 2012 dataset addresses the year 2012.


## Energy balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of Non-OECD Countries (2014 preliminary edition)  / Extended Energy Balances

We obtained an energy balance in TJ for the country “Germany”.

The 2014 preliminary edition of the Extended Energy Balances contains 3 extra columns in comparison to the 2013 edition of the Extended Energy Balances:

- Peat products
- Oilshale and oil sands
- Bio jet kero

In the DE 2012 Extended Energy Balance, these columns only contain zeros and we decided to remove prior to importing the Energy Balance in the CHP analysis as these columns are currently not processed by our analyses and would lead to an unwanted relocation of columns.


### Shift of solar PV

In the original IEA energy balance, all "Solar photovoltaics" is listed under "Electricity output (GWh)-main activity producer electricity plants". This will cause all solar PV to be installed in the main activity sector, no solar PV panels will be shown in the residential or services sector.

To fix this issue, we decided to manipulate the IEA energy balance. Some "Solar photovoltaics" energy is moved from the row "Electricity output (GWh)-main activity producer electricity plants" to the row "Electricity output (GWh)-autoproducer electricity plants"

When manipulating any cells in the energy balance and autoproducer table, one needs to be very careful not to mess up the 'total' cells in the table. Furthermore, a manipulation of energy in the energy balance has to be reflected in the autoproduer table:

The autoproducer table reports ***net*** energy production, while the energy balance shows ***gross*** energy flows.
Therefore, a gross/net conversion factor has to be calculated *first*. The gross/net conversion factor is calculated with the original IEA data tables, prior to making any changes!

````
gross/net conversion factor =
	Divide[
		Energy balance ("Electricity output (GWh)-autoproducer electricity plants"(Total))
		,
		Autoproducer table ("Autoproducer electricity plants"(Total net production))
	]
````

This factor is required when manipulating solar PV production in the autoproducer table.

The cumulative market segmentation reported by [EPIA](hhttp://refman.et-model.com/publications/1876) is used to determine the solar PV production breakdown in the sectors:

| Sector         | Percentage |
| :------------- | ---------: |
| Ground mounted |      24.9% |
| Industrial     |      10.7% |
| Commercial     |      51.8% |
| Residential    |      12.7% |

It is assumed that ground mounted PV is Main activity production. Furthermore, industrial and commercial are aggregated in Services.

| Sector         | Percentage |
| :------------- | ---------: |
| Residences     |      12.7% |
| Services       |      62.4% |
| Main activity  |      24.9% |

Based on this assumption, the following changes are made to the IEA energy balance

1. "Electricity output (GWh)-main activity producer electricity plants" / "Solar photovoltaics" is reduced to 24.9% of its original value
* The amount that was removed from 'main activity' is added to autoproducer row: "Electricity output (GWh)-autoproducer electricity plants" / "Solar photovoltaics" is set to 75.1% of what was formerly 'main activity'.

The relevant 'total' cells to the right are adjusted accordingly. The manipulation of the autoproducer table is described below.


## Autoproducer table

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2014 preliminary edition) / OECD, Net Electricity and Heat Production by Autoproducers

We obtained an autoproducer table in TJ for the country “Germany”.


### Shift of solar PV

The shift of solar PV that was done in the energy balance also has to be reflected in the autoproducer table:
Let us call the new "solar PV" in "Electricity output (GWh)-autoproducer electricity plants" of the energy balance '*Z*'. A share of Z needs to be added to the corresponding cells in the autoproducer table:

1. "Autoproducer electricity plants", "Residences": add 12.7% / [gross/net conversion factor] * Z
2. "Autoproducer electricity plants", "Commercial and public service": add 62.4% / [gross/net conversion factor] * Z

"Total" and "subtotal" cells in the autoproducer table are adjusted accordingly.


## Debts

- The three additional columns in the Extended Energy Balance that were removed should actually be addressed in our analysis and not be removed.