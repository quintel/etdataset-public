# 4a. Metal industry analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


The following changes were made:

- The steel production is TEMPORARY set to 5 MT to avoid a negative final demand for natural gas in the other metal industry. This negative final demand is caused by overconsumption of gas in the electric furnace. See https://github.com/quintel/etdataset/issues/491. The correct production is 13.639 MT. This value is taken from the [World Steel Assosiation (WSA)](http://www.worldsteel.org/dms/internetDocumentList/statistics-archive/yearbook-archive/Steel-Statistical-Yearbook-2013/document/Steel-Statistical-Yearbook-2012.pdf)(Table 6).
- The share of blast furnaces and electric furnaces is set to resp. 25.1% and 74.9% This value is taken from the WSA (Table 6).
- The aluminium production is set to 0.07 MT. This value is taken from [Wikipedia](http://en.wikipedia.org/wiki/List_of_countries_by_aluminium_production), data from 2009. Beware: you need to fill in the production of aluminium, not of aluminium oxide.


Issues:

- [CRITICAL] The final demand of natural gas in the other industry sector is below zero. Might be result from the usage of other fuels in the metal industry. See https://github.com/quintel/etdataset/issues/491.
- There is a lot of unmodelled coal transformation in the metal sector.


