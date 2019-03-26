# 3. Primary production analysis

## Timecurves

The timecurves for the NL/2013 dataset are based on the nl/2015 dataset which is based on:

1. The [NLOG](http://refman.et-model.com/publications/1880) for natural gas and crude oil

2. The Primes reference scenario in [EC\_2013\_Trends to 2050 reference scenario 2013](http://refman.et-model.com/publications/1874) for woody biomass. It is assumed that the time curve for uranium is zero.

Values for 2010, 2011, 2012 and 2013 are obtained from the IEA energy balance. See the [3\_primary\_production\_source\_analysis.xlsm](3_primary_production_source_analysis.xlsm) for more details. 

There are doubts about the reliability of the Primes data. For the NL 2013 dataset there are substantial differences between Primes data and local sources. See [ETdataset#548](https://github.com/quintel/etdataset/issues/548) for an elaboration in this issue.


## Wood

The domestic production of wood is set to `6.1 PJ`. This value is estimated from the production of 'fuelwood' reported by Eurostat (for_basic database). See [wood\_source\_analysix.xlsx](wood_source_analysis.xlsx).

## Waste

The maximum domestic production of biogenic waste and non-biogenic waste are set to resp. `38,589 TJ` and `31,572 TJ`. These values are estimated from the current volume of 'waste incineration with energy recovery' and the potential available volume for 'waste incineration with energy recovery' (i.e. volumes reported for 'waste incineration without energy recovery' and the 'deposited waste', reported by Eurostat (env_wasmun database). See [waste\_source\_analysix.xlsx](waste_source_analysis.xlsx).

## Waste fats

The demand and max_demand of waste fats is set to `1.38 PJ` since this is the amount of waste fats currently used for biofuel production in the Netherlands, the rest is imported (NEA 2017 "Rapportage Energie voor Vervoer in Nederland 2017").

## Bio-kerosene

Currently no bio-kerosene is produced in the Netherlands, everything is imported (https://www.luchtvaartnieuws.nl/nieuws/categorie/18/technologie/nederland-krijgt-fabriek-voor-biokerosine-skynrg)