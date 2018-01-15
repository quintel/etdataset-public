# 4a. Metal industry analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


## Steel

- The steel production is set to 13.639 MT. This value is taken from the [World Steel Assosiation (WSA)](http://refman.et-model.com/publications/1878) (Table 6).
- The share of blast furnaces and electric furnaces is set to resp. 25.1% and 74.9% This value is taken from the [WSA](http://refman.et-model.com/publications/1878) (Table 6).


## Aluminium

- The aluminium production is set to 0.07 MT. This value is taken from [Wikipedia](http://en.wikipedia.org/wiki/List_of_countries_by_aluminium_production), data from 2009. Beware: you need to fill in the production of aluminium, not of aluminium oxide.


## Debts

- [SOLVED] The final demand of natural gas in the other industry sector is below zero. Might be result from the usage of other fuels in the metal industry. See https://github.com/quintel/etdataset/issues/491.
- There is a lot of unmodelled coal transformation in the metal sector.


