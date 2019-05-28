# 3. Primary production analysis

## Time curves

1. The GTS curves are used for natural gas. Numbers are derived by Energiebeheer Nederland from [this GasUnie letter](https://www.rijksoverheid.nl/ministeries/ministerie-van-economische-zaken-en-klimaat/documenten/brieven/2019/01/31/brief-gasunie-over-raming-benodigd-groningenvolume) (31-01-2019)

2. The [NLOG](https://www.nlog.nl/sites/default/files/jaarverslag%20delfstoffen%20en%20aardwarmt%20in%20nederland%20-%202017.pdf) for crude oil

3. The Primes reference scenario in [EC_2016_Trends to 2050 reference scenario 2016](https://refman.energytransitionmodel.com/publications/2096) for woody biomass and crude oil. It is assumed that the time curve for uranium is zero.

Values for 2010, 2011, 2012, 2013 and 2015 are obtained from the IEA energy balance. See the [3\_primary\_production\_source\_analysis.xlsm](3_primary_production_source_analysis.xlsm) for more details. 

There are doubts about the reliability of the Primes data. For the NL 2013 dataset there are substantial differences between Primes data and local sources. See [ETdataset#548](https://github.com/quintel/etdataset/issues/548) for an elaboration in this issue.


## Wood

The domestic production of wood is set to `6.1 PJ`. This value is estimated from the production of 'fuelwood' reported by Eurostat (for_basic database). See [wood\_source\_analysix.xlsx](wood_source_analysis.xlsx).

## Waste

The maximum domestic production of biogenic waste and non-biogenic waste are set to resp. `38,589 TJ` and `31,572 TJ`. These values are estimated from the current volume of 'waste incineration with energy recovery' and the potential available volume for 'waste incineration with energy recovery' (i.e. volumes reported for 'waste incineration without energy recovery' and the 'deposited waste', reported by Eurostat (env_wasmun database). See [waste\_source\_analysix.xlsx](waste_source_analysis.xlsx).

## Waste fats

The demand and max_demand of waste fats is set to `1.38 PJ` since this is the amount of waste fats currently used for biofuel production in the Netherlands, the rest is imported (NEA 2017 "Rapportage Energie voor Vervoer in Nederland 2017").

## Bio-kerosene

Currently no bio-kerosene is produced in the Netherlands, everything is imported (https://www.luchtvaartnieuws.nl/nieuws/categorie/18/technologie/nederland-krijgt-fabriek-voor-biokerosine-skynrg)