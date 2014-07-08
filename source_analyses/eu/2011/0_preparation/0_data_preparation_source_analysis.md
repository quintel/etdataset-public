<!--
  Comment: a confidential version of this source analysis is stored with the IEA data tables of the EU. That confidential version contains actual numbers, which cannot be published, but make the documentation more transparent.
-->

# 0. Preparation of IEA data

IEA data tables are obtained via [http://data.iea.org/ieastore/default.asp](http://data.iea.org/ieastore/default.asp). All IEA data used for the EU27 dataset addresses the year 2011.


## Energy balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of Non-OECD Countries (2013 edition)  / Extended Energy Balances

We obtained an energy balance in TJ for the 'country': “Memo: European Union – 27”.

This energy balance considers the 27 EU countries:
Austria, Belgium, Bulgaria, Cyprus, the Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, the Netherlands, Poland, Portugal, Romania, the Slovak Republic, Slovenia, Spain, Sweden, United Kingdom.

The EU-27 energy_balance contains 2 rows, which have to be removed, prior to using it in the CHP analysis:

- World aviation bunkers
- World marine bunkers

These rows are currently not processed by our analyses and would lead to an unwanted relocation of rows.


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

Since there was no research data available on how much solar PV is installed in each sector (or how much solar energy is produced per sector), the following is assumed:

| Sector        | Electricity production |
| :------------ | :--------------------- |
| Residences    | 40%                    |
| Services      | 30%                    |
| Main activity | 30%                    |

Based on this assumption, the following changes are made to the IEA energy balance

1. "Electricity output (GWh)-main activity producer electricity plants" / "Solar photovoltaics" is reduced to 40% of its original value
* The amount that was removed from 'main activity' is added to autoproducer row: "Electricity output (GWh)-autoproducer electricity plants" / "Solar photovoltaics" is set to 60% of what was formerly 'main activity'.

The relevant 'total' cells to the right are adjusted accordingly. The manipulation of the autoproducer table is described below.


## Autoproducer table

Unfortunately, IEA does not provide a single autoproducer table that addresses all 27 EU countries. Therefore, we had to construct an EU27 autoproducer table based on other IEA data tables.
To track the countries that are excluded and included, please also refer to the Excel file [list_of_EU_countries.xlsx](list_of_EU_countries.xlsx).

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2013 edition) / OECD, Net Electricity and Heat Production by Autoproducers

We obtained an autoproducer in TJ for the 'country' “OECD Europe”.
This OECD Europe autoproducer table addresses 25 countries, 4 of which are not EU-27 members: Iceland, Norway, Switzerland and Turkey.
The autoproducer tables of these 4 non EU-27 counties are bought and subtracted from the OECD Europe table.

This results in an autoproducer table that covers the following 21 EU countries:
Austria, Belgium, the Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Luxembourg, the Netherlands, Norway, Poland, Portugal, the Slovak Republic, Slovenia, Spain, Sweden, Switzerland, Turkey and the United Kingdom.
There are 6 remaining EU27 countries that are not yet considered in the autoproducer table: Cyprus, Malta, Bulgaria, Lithuania, Romania and Latvia.

Cyprus and Malta consume so little energy in comparison to the rest of the EU, that we decide to neglect them in the autoproducer table.
To investigate the significance of the other 4 countries (Bulgaria, Lithuania, Romania and Latvia), we bought several cells of the energy_balance of these 4 countries.

Since IEA data tables are confidential and cannot be re-published by Quintel Intelligence, we cannot reveal the actual numbers here. We can only show how significant the remaining 4 countries are in comparison with the EU27 energy_balance, in relative terms:

|                                                   | Total (BU ,LA ,LI ,RO) / EU27 |
|:--------------------------------------------------|------------------------------:|
| Electricity output (GWh)-main activity producer electricity plants           | 4% |
| Electricity output (GWh)-autoproducer electricity plants                     | 1% |
| Electricity output (GWh)-main activity producer CHP plants                   | 5% |
| Electricity output (GWh)-autoproducer CHP plants                             | 2% |

Conclusion: The electricity output of main activity and autoproduction plants of the disregarded countries contributes to about 5% of the total EU27 countries.

Note that the energy balance is 'leading' in our dataset creation process. The autproducer table is only used to provide a breakdown of the energy reported in the energy_balance. The fact that we disregard 6 countries in the autoproducer table means that our energy distribution over sectors is slightly off, but not our total energy demands.


### Shift of solar PV

The shift of solar PV that was done in the energy balance also has to be reflected in the autoproducer table:
Let us call the new "solar PV" in "Electricity output (GWh)-autoproducer electricity plants" of the energy balance *Z*. A share of Z needs to be added to the corresponding cells in the autoproducer table:

1. "Autoproducer electricity plants", "Residences": add 30% / [gross/net conversion factor] * Z
2. "Autoproducer electricity plants", "Commercial and public service": add 30% / [gross/net conversion factor] * Z

"Total" and "subtotal" cells in the autoproducer table are adjusted accordingly.


## Debts

- There is a lack of research data, telling us how much solar PV capacity is placed in households, services and main activity. The shift of solar PV can be improved if better sources become available.

- It is not known if the autoproducer table is accurate. From our experience with the German dataset, we got the impression that IEA does not report autoproducer production with high accuracy (it may well be that countries do not report autoproduction). It seems that some autoproducer energy flows are reported as main activity in IEA statistics (prime example: solar PV).


