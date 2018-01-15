<!--
  Comment: a confidential version of this source analysis is stored with the IEA data tables of the EU. That confidential version contains actual numbers, which cannot be published, but make the documentation more transparent.
-->

# 0. Preparation of IEA data

IEA data tables are obtained via [http://data.iea.org/ieastore/default.asp](http://data.iea.org/ieastore/default.asp). All IEA data used for the DE dataset addresses the year 2011.


## German energy balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of OECD Countries (2013 edition) / Extended Energy Balances

We obtained an energy balance in TJ for the 'country': “Germany”.


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

There is not much research data available that allows for an estimate of how much PV capacity is installed in which sector. This [source](https://www.proteus-solutions.de/~Unternehmen/News-PermaLink:tM.F04!sM.NI41!Article.954426.asp) is used to estimate the following solar PV production breakdown in the sectors:

| Sector   | Size of installation | Ratio of solar PV electricity production |
|:-------|:-------------------|:---------------------------------------:|
| Residences | smaller than 30 kWp | 50% |
| Services |  10 - 30 kWp          | 35% |
| Main activity | > 30 kWp         | 15% |

Based on this assumption, the following changes are made to the IEA energy balance

1. "Electricity output (GWh)-main activity producer electricity plants" / "Solar photovoltaics" is reduced to 15% of its original value
* The amount that was removed from 'main activity' is added to autoproducer row: "Electricity output (GWh)-autoproducer electricity plants" / "Solar photovoltaics" is set to 85% of what was formerly 'main activity'.

The relevant 'total' cells to the right are adjusted accordingly. The manipulation of the autoproducer table is described below.


## German autoproducer table

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2013 edition) / OECD, Net Electricity and Heat Production by Autoproducers

We obtained an autoproducer table in TJ for the 'country' “Germany”.


### Shift of solar PV

The shift of solar PV that was done in the energy balance also has to be reflected in the autoproducer table:
Let us call the new "solar PV" in "Electricity output (GWh)-autoproducer electricity plants" of the energy balance '*Z*'. A share of Z needs to be added to the corresponding cells in the autoproducer table:

1. "Autoproducer electricity plants", "Residences": add 50% / [gross/net conversion factor] * Z
2. "Autoproducer electricity plants", "Commercial and public service": add 35% / [gross/net conversion factor] * Z

"Total" and "subtotal" cells in the autoproducer table are adjusted accordingly.

## Shortcomings

There is a lack of research data, telling us how much solar PV capacity is placed in households, services and main activity. The shift of solar PV can be improved if better sources become available.
