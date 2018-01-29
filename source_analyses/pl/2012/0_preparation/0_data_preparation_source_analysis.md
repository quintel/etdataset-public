# 0. Preparation of IEA data

IEA data tables are obtained via [http://data.iea.org/ieastore/default.asp](http://data.iea.org/ieastore/default.asp). All IEA data used for the PL 2012 dataset addresses the year 2012.


## Energy balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of Non-OECD Countries (2014 preliminary edition)  / Extended Energy Balances

We obtained an energy balance in TJ for the country: "Poland".

The 2014 preliminary edition of the Extended Energy Balances contains 3 extra columns in comparison to the 2013 edition of the Extended Energy Balances:

- Peat products
- Oilshale and oil sands
- Bio jet kero

In the PL 2012 Extended Energy Balance, these columns only contain zeros and we decided to remove prior to importing the Energy Balance in the CHP analysis as these columns are currently not processed by our analyses and would lead to an unwanted relocation of columns.


## Autoproducer table

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2014 preliminary edition) / OECD, Net Electricity and Heat Production by Autoproducers

We obtained an autoproducer table in TJ for the country: "Poland".


## Debts

- The three additional columns should be addressed in our analysis.