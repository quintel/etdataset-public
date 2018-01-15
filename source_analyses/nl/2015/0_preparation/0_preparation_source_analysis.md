# 0. Preparation of IEA data

IEA data tables are obtained via [http://wds.iea.org/WDS/Common/Login/login.aspx](http://wds.iea.org/WDS/Common/Login/login.aspx). All IEA data used for the NL 2015 dataset addresses the year 2015.


## NL Energy balance

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Energy Balances of OECD Countries (2017 edition)  / Extended Energy Balances

We obtained an energy balance in TJ for the country “Netherlands”. We downloaded it in `.xls`  and `.csv` formats (Actions >> Download report data >> <choose file format>.

The 2015 edition of the Extended Energy Balances contains 2 extra columns in comparison to the 2013 edition of the Extended Energy Balances (and 1 less than the 2014 edition):

- Peat products
- Oilshale and oil sands

In the 2015 edition of the Extended Energy Balance for the Netherlands 2013, these columns only contain zeros and we decided to remove prior to saving in `.csv` format and importing the Energy Balance in the CHP analysis as these columns are currently not processed by our analyses and would lead to an unwanted relocation of columns. 

Note that in order to import the energy balance the file needs to be saved as `.csv` format in MS Excel as `iea_energy_balance.csv` and placed in the directory: 


    data / <country_code> / <year> / 1_chp / input 

This directory is automatically created by the `analysis_manager` if you select a new country or new year for which to open the CHP analysis.

## Autoproducer table

On the IEA website, click on `Access Services` and log in. Go to:

    Reports / Electricity Information (2017 edition) / OECD, Net Electricity and Heat Production by Autoproducers

We obtained an autoproducer table in TJ for the country "Netherlands". We downloaded it in `.xls`  and `.csv` formats (Actions >> Download report data >> <choose file format>.


## Debts

-The two additional columns in the IEA Extended Energy Balance should be addressed in our analysis, instead of being removed as is currently the case.