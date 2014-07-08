# 2. Power and heat plant analysis

## Technology Splits

### Coal plants

CCS (Carbon Capture and Storage) and combined cycle technologies are set to 0. Only Coal Supercritical and Coal Ultra Supercritical are used.
The technology split influences the electrical efficiency of an average coal plant.
Coal ultra supercritical and Coal Supercritical are adjusted until the checks for fuel use are matched best. For more details see the 'Results by fuel' sheet.

Result:
- Coal Ultra supercritical: 20.0%
- Coal Supercritical: 66.1%

Note that the share of coal plants also influences the check "Total fuel input to power plants matches the indicated fuel input (±5%)".


### Lignite plants

Lignite Ultra supercritical: 100% - there is no CCS technology in place. Note that the ETM currently has no 'copnventional' lignite technology available, meaning it is likely to overestimate the efficiency of lignite plants by only using modern ultra-supercritical plants with a relatively high efficiency.


### Gas plants

Please refer to the Excel workbook "capacity validation.xlsx", sheet "Gas plants". From the document [Eurolectric: "Power Statistics & Trends 2011 full report"](http://refman.et-model.com/publications/1836), it is extracted that there are 45,474 MW of Gas Turbines installed in the EU. Note: The source addresses the year 2009 (or older) and the dataset is not complete. The same source also reports that the total production from these gas turbines was about 31 TWh. Note: this number also addresses the year 2009.

Due to the lack of sources, these two figures are used to calibrate gas turbines in the EU dataset:
Full load hours of gas turbines are set to `31 TWh / 45,474 MW = 682 h`.
After setting the FLH of Gas Turbines 682 h, the production share of gas turbines is increased until they reach 45,500 MW installed capacity (results by machine page).

Gas Combined cycle CCS is not available. The share of Gas Combined cycle vs. Gas Ultra supercritical is adjusted so that the IEA fuel consumption is matched as closely as possible (checks):

- Gas Turbine 7.5%
- Gas Combined cycle 73.0%
- Gas Combined cycle CCS 0.0%
- Gas Ultra supercritical 19.5%


### Nuclear plants

Nuclear power plants are adjusted to make the average efficiency match IEA data. Of course, we cannot expect that this will match the actual installed capacity, because the efficiencies of the two nuclear ETM converters may differ in reality.

- Nuclear 2nd gen: 73%
- Nuclear 3rd gen: 27%


### Hydro plants

The ETM does not consider pumped storage as a power producer. Only run-of-river and run-of-mountain hydro power is considered. According to the tables 3.1.1.4 and 3.2.1.4 in [Eurolectric: "Power Statistics & Trends 2011 full report"](http://refman.et-model.com/publications/1836) (pages 82 and 140), hydro river and mountain plants are characterised as follows (see Excel workbook "capacity validation.xlsx", sheet "Hydro plants")

|                  |  Hydro, total  | conventional hydro | of which run-of-river | of which run-of-mountain |
|:-----------------|---------------:|-------------------:|----------------------:|-------------------------:|
| Production, TWh  | 355            | 238                | 115                   | 124                      |
| Capacity, MW     | 142,861        | 100,525            | 28,720                | 70,235                   |

"Hydro, total" refers to all hydro electricity, including pumped mountain storage. "run-of-mountain" is calculated from the other numbers. Note that these numbers are not very accurate as the number of digits may suggest. The research data addresses the year 2009 (or older) and research data is not available for all counties.

The following technology split is set for hydro plants, based on the electricity production:

- Hydro river 48% (115 TWh)
- Hydro mountain 52% (124 TWh)


### Solar plants

Filling in the production share of solar energy is a bit tricky because of the presence of concentrated solar power (CSP) in Spain. Spain should have had roughly 969 MW installed at the end of 2010, see [Wikipedia](http://en.wikipedia.org/wiki/Concentrated_solar_power#Deployment_around_the_world). Upon googling "concentrated solar power full load hours", you will find that FLH of 2000 - 7000 are often reported, for example [here](http://www.solar4science.de/e115374/e115375/infoboxContent115384/KeynotePitz-Paal.pdf). Because CSP plants usually 'follow' the sun (moving mirrors) and new facilities often make use of thermal storage, FLH can be rather high. Since the technology that was installed at the end of 2010 probably did not reach very high FLH on average, we set FLH to 1500 for CSP technology.
The following table shows the effect of assuming certain FLH and electricity production on the installed capacity.

| Plant                  | FLH       | Electricity Production, TJ  | Installed capacity, MW |
|:-----------------------|----------:|----------------------------:|-----------------------:|
| Household sector, PV   | 1,050     | 65,083                      | 17,218                 |
| Services sector, PV    | 1,050     | 48,264                      | 12,768                 |
| Large scale solar PV   | 1,050     | 43,345                      | 11,467                 |
| Large scale solar CSP  | 1,500     | 5,233                       | 969                    |

The FLH of the PV plants follows from [European Commision, Global irradiation and solar electricity potential - Europe](http://re.jrc.ec.europa.eu/pvgis/cmaps/eur.htm). Note that these FLH are based on a performance ratio of 0.75. This is a conservative estimate. In the NL dataset, Quintel assumes a performance ratio of 0.83. --> Further research is needed: What are actual solar PV FLH in the EU (on average, not for optimally inclined systems)?


### Wind

As a breakdown of production is not available, the following trick is used to derive an energetic technology split: First, the FHL of the technologies are defined. Second, the installed capacities per technology are researched. Third, the  technology split (energy) is manipulated until installed capacities are matched.

The report [Europe's onshore and offshore wind energy potential](http://refman.et-model.com/publications/1312) by the European Environment Agency provides insight into the potential of wind power in Europe. How many FLH can be reached and where is the highest potential (geographically)? Based on that source, we assume:

| Plant           | FLH       |
|:----------------|----------:|
| wind inland     | 2,000     |
| wind coastal    | 2,500     |
| wind offshore   | 3,200     |

The document [Wind_in_power_2011_European_statistics.pdf by EWEA](http://www.ewea.org/fileadmin/files/library/publications/statistics/Wind_in_power_2011_European_statistics.pdf) reports the following installed capacity:

|     | Installed Capacity at the end of 2010, MW |
|:----|------------------------------------------:|
| Total eu-27                       |   84,650    |
| of which: offshore and near shore |    2,944    |
| of which: onshore (incl. coastal) |   81,706    |

It is furthermore assumed that 15% of all onshore capacity is installed in coastal regions and that 85% have 'inland' characteristics (no source).
This results in the following technology split:

- Wind turbine coastal: 17.1%
- Wind turbine offshore: 5.3%
- Wind turbine inland	: 77.6%


## Full load hours

In general, there is a lack of research data regarding FLH and installed capacities in the EU.
Many of the following assumptions are based a report by [Prognos: The future role of coal in europe](http://www.euracoal.be/componenten/download.php?filedata=1208519374.pdf&filename=prognos_FutureCoal_070822_final_kurz.pdf&mimetype=application/pdf) (page 119). This report merely publishes assumptions that were made to investigate future scenario of the role of coal in Europe. Nonetheless, the report has proven to supply useful figures for the year 2010.

We use the Excel file "capacity validation.xlsx" to compare the installed capacity that results from the CHP and PP_HP analyses with the literature.


### Coal plants

According to the Prognos report, there were 139,717 MW hard coal plants (incl. CHPs) installed.
We assume here that hard coal includes the co-firing of biomass. The CHP analysis reports 40 GW of coal CHPs (incl. co-firing) (based on the technology split and FLH hours assumed in the CHP analysis). The remaining 100 GW have to be installed in the PP_HP analysis.
In the CHP analysis, the Dutch FLH are scaled down proportionally until the desired capacity is reached:

| Plant | FLH |
|:------|----:|
| Coal/Wood pellets Ultra supercritical co-firing | 4,500 |
| Coal Supercritical  | 4,000 |
| Coal Ultra supercritical  | 4,500 |
| Coal Ultra supercritical CCS  | 6,000 - not relevant |
| Coal Combined cycle  | 2,700 |
| Coal Combined cycle CCS  | 4,500 - not relevant |


### Lignite plants

Prognos reports 58,491 MW lignite plants (incl. CHPs). FLH hours of the converter 'Lignite Ultra supercritical' are adjusted until the desired capacity is reached (together with the installed capacity of the Lignite CHP):

| Plant | FLH |
|:------|----:|
| Lignite Ultra supercritical  | 5500 |
| Lignite Ultra supercritical oxyfuel CCS  | 5500, not relevant |


### Gas plants

As outlined above, there are 45,474 MW of Gas Turbines installed in the EU, which are assumed to operate at 682 FLH.
Prognos reports 152,757 MW of gas plants (excl. CHPs). Based on these assumptions, the remaining installed capacity is filled with the other gas plants. FLH are scaled, until the desired capacity is reached.

| Plant | FLH |
|:------|----:|
| Gas Turbine  | 682 |
| Gas Combined cycle  | 4,800 |
| Gas Combined cycle CCS  | 4,000 |
| Gas Ultra supercritical | 1,800 |


### Nuclear plants

Prognos reports 136,363 MW of nuclear plants. It is assumed that the 3rd generation plants run more or less constantly (8000 FLH). The FLH of the 2nd generation plant are adjusted until the desired total capacity is reached:

| Plant | FLH |
|:------|----:|
| Nuclear 2nd gen  | 6,200 |
| Nuclear 3rd gen  | 8,000 |

Note that the installed capacity of nuclear power plants changed rapidly in the year 2011, at least in Germany (see above).


### Hydro plants

The installed capacities of hydro plants was already mentioned above (total capacity: ~100 GW). Prognos reports 110 GW of hydro energy. FLH are adjusted until the desired installed capacities are reached. It turns out that the capacities reported by EUROLECTRIC lead to rather high FLH for river plants (5,000 FLH). Since the EUROLECTRIC report does not cover all EU countries and does not solely address one year (2009), it is decided to target the 110 GW reported by Prognos:

| Plant | installed capacity, MW | FLH |
|:------|----:|----:|
| river     | 38,720 | 3,800 |
| mountain  | 70,235 | 2,300 |


### Solar PV

FLH for solar PV have been documented above.


### Wind

FLH for wind turbines are documented above, see report [Europe's onshore and offshore wind energy potential](http://refman.et-model.com/publications/1312) by the European Environment Agency


### Other

Prognos reports 58,577 MW of oil plants. Both 'Oil Ultra supercritical' and 'Diesel Engine' consume oil. Their FLH are set to 1,000 and 300, respectively, which brings about the desired capacity.

The FLH of 'Waste Supercritical' and 'Geothermal' are taken directly from the Dutch dataset.


## Validation of CHP and Power and heat plant analysis

After the CHP and PP_HP analysis are filled in, it is possible to evaluate the resulting installed capacities for each type of power/heat plant. For most countries reports on such installed capacities do not distinguish between CHP or non-CHP plants, after all.


### Additional research data

- The website [https://www.destatis.de/DE/ZahlenFakten/Wirtschaftsbereiche/Energie/Erzeugung/Tabellen/Bruttostromerzeugung.html](https://www.destatis.de/DE/ZahlenFakten/Wirtschaftsbereiche/Energie/Erzeugung/Tabellen/Bruttostromerzeugung.html) (Statistisches Bundesamt) also reports electricity production by energy carrier. This may be a useful source for further investigations.
- The [presentation by BDEW](http://refman.et-model.com/publications/1835) gives an extended overview on electricity production. It is a very useful document to get some background information, for example, the regional distribution of solar PV within Germany.

### Validation

The file [capacity_validation.xlsx](capacity_validation.xlsx) summarises the 'results by machine' sheets of the CHP and Power and heat plant analyses. You can see how much electric generation capacity is installed, based on the assumption made in the analysis dashboards.


## Debts

- The Power and heat plant analysis should be validated based on the Platts data.
- **Installed capacity of central heaters**. We need to validate the 'heat deficit' of CHP plants that is passed on to the PP&HP analysis. This heat deficit is then produced by main activity heaters. However, this capacity is not validated and seems rather large.
- Many FLH and installed capacities have not yet been researched very well. This can be improved, if better sources become available.