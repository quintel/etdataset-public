# 4a. Metal industry analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


The following changes were made:

- The steel production is set to 9.579 MT. This value is taken from the [World Steel Assosiation (WSA)](http://www.worldsteel.org/dms/internetDocumentList/statistics-archive/yearbook-archive/Steel-Statistical-Yearbook-2013/document/Steel-Statistical-Yearbook-2012.pdf)(Table 6).
- The share of blast furnaces and electric furnaces is set to resp. 78.6% and 21.4% This value is taken from the WSA (Table 6).
- The aluminium production is set to 0.253 MT. This value is taken from [Wikipedia](http://en.wikipedia.org/wiki/List_of_countries_by_aluminium_production), data from 2009. Beware: you need to fill in the production of aluminium, not of aluminium oxide.


Issues:

- There is a lot of unmodelled coal transformation in the metal sector.
- [SOLVED] The final demand of natural gas in the other industry sector is below zero. Might be result from the usage of other fuels in the metal industry.


