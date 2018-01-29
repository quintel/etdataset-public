# 2. Power and heat plant analysis

The following notes pertain to the user settings used on the Dashboard of the research analysis Excel file called '2_power_and_heat_plant_analysis.xlsx'.


## Technology Splits

### Coal plants

CCS and combined cycle technologies are set to 0. Only Coal Supercritical and Coal Ultra Supercritical are used.
The technology split influences the electrical efficiency of an average coal plant.
Coal ultra supercritical is adjusted until the checks for fuel use are matched best. For more details see the 'Results by fuel' sheet in the analysis.
Result:

- Coal Ultra supercritical: 35.0%
- Coal Supercritical: 52.6%

Note that the share of coal plants also influences the check "Total fuel input to power plants matches the indicated fuel input (±5%)".


### Lignite plants

Lignite Ultra supercritical: 100% - there is no CCS technology in place. Note that the fact that the ETM has no conventional (supercritical) lignite plant available, means that the efficiency of power production using lignite is likely to be overestimated.


### Gas plants

The document [“Kraftwerke in Deutschland (ab 100 Megawatt elektrischer Leistung)“](http://www.umweltbundesamt.de/sites/default/files/medien/378/dokumente/kraftwerke_de_ab_100_mw.xls) (published on http://www.umweltbundesamt.de/daten/energiebereitstellung-verbrauch/kraftwerke) gives an indication of the share of installed gas plants.
There are several problems with this document: It only lists installed capacity, which is known not to be proportional to electricity production. Furthermore, not all power plants are listed (only > 100 MW, which excludes many wind and solar power locations, but also other fossil plants). As always, there also is an overlap with CHPs in the list. Therefore, the source is not very suitable to derive information about power production and installed capacity per plant. I did not find a a more useful source.
From the document, it is extracted that there are about 2300 MW of Gas Turbines installed in Germany. After setting the FLH of Gas Turbines to the Dutch value (500 FLH), I increased their production share in the 'Dashboard' until they reach about 2300 MW.

Gas Combined cycle CCS are not available in Germany. The share of Gas Combined cycle vs. Gas Ultra supercritical is adjusted so that the IEA fuel consumption is matched as closely as possible (checks):

- Gas Turbine 2.6%
- Gas Combined cycle 87.0%
- Gas Combined cycle CCS 0.0%
- Gas Ultra supercritical 10.5%


### Nuclear plants

Nuclear power plants are adjusted to make the average efficiencies match IEA data. Of course, we cannot expect that this will match the actual installed capacities in Germany, because the efficiencies of the two nuclear ETM converters may differ from reality.

- Nuclear 2nd gen 80.0%
- Nuclear 3rd gen 20.0%


### Hydro plants

The ETM does not consider pumped storage. According to ["Stromerzeugungskapazitäten, Bruttostromerzeugung und Bruttostromverbrauch"](http://refman.et-model.com/publications/1833), there are about 11 GW of hydro capacity - but about half of that is actually pumped storage capacity (not reported in ETM).

The German [Federal Ministry for the Environment](http://www.erneuerbare-energien.de/en/topics/hydropower/general-information/?cHash=816f8cc23fe06c8f81ed0897140ba585) reports that there are 7,300 small (< 1 MW) and 354 medium/large (> 1MW) hydro power stations installed (data from 2006).
Quoting: “Only 12% of the plants are owned by energy utilities, but these generate more than 90% of all hydroelectricity”. And: "20% of the large power stations in Germany are storage power stations, 80% are run-of-river plants."
These figures tell something about the installed capacity, but not about the energy production in river/mountain plants.

Further research data on German hydro energy can be extracted from the EUROLECTRIC report ["Power Statistics & Trends 2011 full report"](http://refman.et-model.com/publications/1836): (pages 141 and 59):

|                  |  Hydro, total  | conventional hydro | of which run-of-river | of which run-of-mountain |
|:----------------:|:--------------:|:------------------:|:---------------------:|:------------------------:|
| Production, TWh  | 24.3           | 18.8               | 16                    |              2.8         |
| Capacity, MW     | 11,027         | 5,317              | 3,810                 |              1507        |

Production: 16 out of 18.8 TWh are produced in run of river plants. (24.3 - 18.8 = 5.5 TWh were 'unconventional', most likely pumped-storage). The following share of river vs. mountain plants is set:
Hydro river 85%  (16 TWh)
Hydro mountain	 15% (2.8 TWh)


### Solar plants

Since "concentrated solar power" is not installed in Germany to a meaningful amount, all main activity solar PV is "Large scale solar PV"


### Wind

Information on wind energy production with spatial resolution could not be found.
Therefore, the energy is distributed over the different turbines in the following way (estimation):

- Wind turbine coastal   2.5%
- Wind turbine offshore	  5.0%
- Wind turbine inland    92.5%

For more information on the differences between these kinds of turbines, see the "?" buttons for these technologies in the [ETM](http://pro.et-model.com/scenario/supply/electricity_renewable/wind-turbines) itself.


## Full load hours

### Coal plants

FLH are different from the NL dataset, as is to be expected.
According to ["BMWI: Stromerzeugungskapazitäten, Bruttostromerzeugung und Bruttostromverbrauch"](http://refman.et-model.com/publications/1833), there were 30.2 GW hard coal power plants installed (incl. co-firing).
There are about 4 GW of coal CHPs in the CHP analysis. The following FLH are chosen, in order to roughly match the 30 GW in total (the last three plant types in the table below do not exist and have NL FLH).

| Plant | FLH |
|:-----:|:---:|
| Coal/Wood pellets Ultra supercritical co-firing | 5500 |
| Coal Supercritical  | 4300 |
| Coal Ultra supercritical  | 5500 |
| Coal Ultra supercritical CCS  | 6000 |
| Coal Combined cycle  | 4600 |
| Coal Combined cycle CCS  | 4500 |


### Lignite plants

According to ["BMWI: Stromerzeugungskapazitäten, Bruttostromerzeugung und Bruttostromverbrauch"](http://refman.et-model.com/publications/1833), there were 24.90 GW lignite power plants installed. FLH are adjusted until that value is matched.

| Plant | FLH |
|:-----:|:---:|
| Lignite Ultra supercritical  | 5760 |
| Lignite Ultra supercritical oxyfuel CCS  | 5972 |


### Gas plants

There are about 13 GW gas CHPs installed. According to ["BMWI: Stromerzeugungskapazitäten, Bruttostromerzeugung und Bruttostromverbrauch"](http://refman.et-model.com/publications/1833), there were 23.9 GW gas power plants installed. A remaining 10.9 GW main activity plants need to be installed.
For gas turbines, it was already assumed above that they have 500 FLH.

| Plant | FLH |
|:-----:|:---:|
| Gas Turbine  | 500 |
| Gas Combined cycle  | 4900 |
| Gas Combined cycle CCS  | 3500 |
|Gas Ultra supercritical  | 3750 |


### Nuclear plants

According to ["BMWI: Stromerzeugungskapazitäten, Bruttostromerzeugung und Bruttostromverbrauch"](http://refman.et-model.com/publications/1833), there were 12.7 GW nuclear power plants installed. However, for the year 2010, a value of 21.5 GW is reported. Therefore, it is decided to model a mean value of 17.1 GW.

| Plant | FLH |
|:-----:|:---:|
| Nuclear 2nd gen  | 6314 |
| Nuclear 3rd gen  | 6314 |

It is assumed that both plant types have the same FLH. FLH of 6300 seem to be a bit low because nuclear plants usually run around the clock (only short maintenance and preferred plant in merit order). It is not known for how many hours nuclear plants were operated in Germany in 2011 (in March 2011, the Fukushima Daiichi nuclear disaster happened, in return Germany's government rapidly changed its nuclear policies). --> more research is needed.


### Hydro plants

Full load hours are adjusted, until the capacity of mountain and river plants meets the data reported by EUROLECTRIC (see above).

| Plant             | capacity (MW) | FLH  |
|:-----------------:|:-------------:|:----:|
| Hydro river       |  3810         | 3852 |
| Hydro mountain    | 1507          | 1718 |


### Solar PV

From the file ["Solar radiation and photovoltaic electricity potential"](http://refman.et-model.com/publications/1834), the factor "Yearly sum of solar electricity generated by 1kWp system with performance ratio 0.75 [kWh/kWpeak]" is extracted: 955 kWh/kWpeak.
This factor is equivalent to FLH (FLH are defined as annual production / installed capacity).
These FLH are used for all solar technologies.

| Plant | FLH |
|:-----:|:---:|
| Large scale solar PV  | 955 |
| Households solar PV  | 955 |
| Services solar PV  | 955 |
| Large scale solar CSP  | 955 |

Note that a performance ratio of 0.75 is comparatively low. In the NL model, Quintel assumes a performance ratio of 0.83. Assuming a performance ratio of 0.83 would result in 1055 FLH in Germany. --> Further research is needed: What are actual solar PV FLH in Germany (on average, not for optimally inclined systems)?


### Wind

According to ["BMWI: Stromerzeugungskapazitäten, Bruttostromerzeugung und Bruttostromverbrauch"](http://refman.et-model.com/publications/1833), the installed capacity was 27.2 GW in 2010 and 29.1 GW in 2011.
By applying the 'old' FLH defined in the German dataset found in Quintel's 'Input Excel', a total installed capacity of 27.8 GW is reached:

| Plant | FLH |
|:-----:|:---:|
| Wind turbine coastal  | 2400 |
| Wind turbine offshore  | 3300 |
| Wind turbine inland  | 1700 |


### Other

The FLH of all other technologies

- Oil Ultra supercritical
- Diesel Engine
- Waste Supercritical
- Geothermal

are taken from the NL dataset and not changed.


## Validation of CHP and Power and heat plant analysis

After the CHP and PP_HP analysis have both been filled in, it is possible to evaluate the resulting installed capacities for each type of power/heat plant. For most countries reports on such installed capacities do not distinguish between CHP or non-CHP plants, after all.


### Additional data:

- The website of the [Statistisches Bundesamt](https://www.destatis.de/DE/ZahlenFakten/Wirtschaftsbereiche/Energie/Erzeugung/Tabellen/Bruttostromerzeugung.html) also reports electricity production by energy carrier. This may be a useful source for further investigations.
- The [presentation by BDEW](http://refman.et-model.com/publications/1835) gives an extended overview on electricity production. It is a very useful document to get some background information, for example, the regional distribution of solar PV within Germany.


### Validation

The file [capacity_validation.xlsx](capacity_validation.xlsx) summarises the 'results by machine' sheets of the CHP and Power and heat plant analyses. You can see how much electric generation capacity is installed, based on the assumption made in the analysis dashboards.


## Suggested improvement

* **Installed capacity of central heaters**. We need to validate the 'heat deficit' of CHP plants that is passed on to the PP. HP analysis. This heat deficit is then produced by main activity heaters. However, this capacity is not validated and seems rather large.