# 0. Preparation of IEA data

IEA data tables are obtained via [http://data.iea.org/ieastore/default.asp](http://data.iea.org/ieastore/default.asp). All IEA data used for the NL 2013 dataset addresses the year 2013.


## NL Energy balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of OECD Countries (2015 edition)  / Extended Energy Balances

We obtained an energy balance in TJ for the country “Netherlands”.

The 2015 edition of the Extended Energy Balances contains 2 extra columns in comparison to the 2013 edition of the Extended Energy Balances (and 1 less than the 2014 edition):

- Peat products
- Oilshale and oil sands

In the 2015 edition of the Extended Energy Balance for the Netherlands 2013, these columns only contain zeros and we decided to remove prior to importing the Energy Balance in the CHP analysis as these columns are currently not processed by our analyses and would lead to an unwanted relocation of columns.

## Autoproducer table

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2015 edition) / OECD, Net Electricity and Heat Production by Autoproducers

We obtained an autoproducer table in TJ for the country "Netherlands".


## Debts

-The two additional columns in the IEA Extended Energy Balance should be addressed in our analysis, instead of being removed as is currently the case.