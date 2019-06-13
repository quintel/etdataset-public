# 3. Primary production analysis

## Time curves

The timecurves for the NL/2013 dataset are based on the NL/2015 dataset which is based on:

1. The GTS curves are used for natural gas. Numbers are derived by Energiebeheer Nederland from [this GasUnie letter](https://www.rijksoverheid.nl/ministeries/ministerie-van-economische-zaken-en-klimaat/documenten/brieven/2019/01/31/brief-gasunie-over-raming-benodigd-groningenvolume) (31-01-2019)

2. The [NLOG](https://www.nlog.nl/sites/default/files/jaarverslag%20delfstoffen%20en%20aardwarmt%20in%20nederland%20-%202017.pdf) for crude oil

3. The Primes reference scenario in [EC_2016_Trends to 2050 reference scenario 2016](https://refman.energytransitionmodel.com/publications/2096) for woody biomass and crude oil. It is assumed that the time curve for uranium is zero.

Values for 2010, 2011, 2012, 2013 and 2015 are obtained from the IEA energy balance. See the [3\_primary\_production\_source\_analysis.xlsm](3_primary_production_source_analysis.xlsm) for more details. 

There are doubts about the reliability of the Primes data. For the NL 2013 dataset there are substantial differences between Primes data and local sources. See [ETdataset#548](https://github.com/quintel/etdataset/issues/548) for an elaboration in this issue.


## Wood

The domestic production of wood is set to `2,551 PJ`. This value is estimated from the production of 'fuelwood' reported by Eurostat (for_basic database). See [wood_source_analysix.xlsx](wood_source_analysis.xlsx).


## Waste

The maximum domestic production of biogenic waste and non-biogenic waste are set to resp. `34,513 TJ` and `28,238 TJ`. These values are estimated from the current volume of 'waste incineration with energy recovery' and the potential available volume for 'waste incineration with energy recovery' (i.e. volumes reported for 'waste incineration without energy recovery' and the 'deposited waste', reported by Eurostat (env_wasmun database). See [waste_source_analysix.xlsx](waste_source_analysis.xlsx).