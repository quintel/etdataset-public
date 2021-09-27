# 3. Primary production analysis

## Biomass potentials

Please have a look at our online documentation for the Dutch biomass potentials: https://docs.energytransitionmodel.com/main/biomass

## Non-biogenic waste

The maximum domestic production of non-biogenic waste are set to `31,572 TJ`. This value is estimated from the current volume of 'waste incineration with energy recovery' and the potential available volume for 'waste incineration with energy recovery' (i.e. volumes reported for 'waste incineration without energy recovery' and the 'deposited waste', reported by Eurostat (env_wasmun database). See 
[waste\_source\_analysix.xlsx](waste_source_analysis.xlsx).

## Time curves

1. The GTS curves are used for natural gas. Numbers are derived by Energiebeheer Nederland from [this GasUnie letter](https://www.rijksoverheid.nl/ministeries/ministerie-van-economische-zaken-en-klimaat/documenten/brieven/2019/01/31/brief-gasunie-over-raming-benodigd-groningenvolume) (31-01-2019)

2. The [NLOG](https://www.nlog.nl/sites/default/files/jaarverslag%20delfstoffen%20en%20aardwarmt%20in%20nederland%20-%202017.pdf) for crude oil

3. The Primes reference scenario in [EC_2016_Trends to 2050 reference scenario 2016](https://refman.energytransitionmodel.com/publications/2096) for woody biomass and crude oil. It is assumed that the time curve for uranium is zero.

Values for 2010, 2011, 2012, 2013 and 2015 are obtained from the IEA energy balance. See the [3\_primary\_production\_source\_analysis.xlsm](3_primary_production_source_analysis.xlsm) for more details. 

There are doubts about the reliability of the Primes data. For the NL 2013 dataset there are substantial differences between Primes data and local sources. See [ETdataset#548](https://github.com/quintel/etdataset/issues/548) for an elaboration in this issue.

