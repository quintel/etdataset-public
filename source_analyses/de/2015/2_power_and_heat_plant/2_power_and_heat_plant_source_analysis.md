# 2. Power and heat plant analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.

The Power and heat plant analysis is filled based on enriched data from the German BundesNetzAgentur (BNA). The complete list of power plants and CHPs was obtained from BNA and this was enriched with two columns:
  
  1. One columns to specify each plant's ETM technology using inferred guesses from each power plant's 'Block name' field entry in the BNA list for new plants, and the effort made for the 2012 dataset (which uses a document by the Deutsche Institut für Wirtschaftsforschung (DIW) and).
  - One column which estimates, calculates or looks up each plant's gross capacity (the ETM uses gross not nett capacities). 
   
All numbers were corrected to represent gross installed capacities. The BNA list was edited and where no data was available for gross capacity, each plant was scaled by a factor calculated from known data for similar type power plants.

Sources for estimation of corresponding gross installed capacities:

- [Energie Chronik](http://www.udo-leuschner.de/energie-chronik/080407d2.htm)
- [Wikipedia](http://de.wikipedia.org/wiki/Eigenbedarf_(Kraftwerk) )

This information and more is all found in [Capacities_DE_Kraftwerksliste_BNetzA_2018_brutto_Leisting.xlsx](../2_power_and_heat_plant/Capacities_DE_Kraftwerksliste_BNetzA_2018_brutto_Leisting.xlsx), which contains a PivotTable to ouput the relevant information to another analysis step called [de_2012_capacity validation_gross.xlsx](../2_power_and_heat_plant/de_2012_capacity validation_gross.xlsx).


**Filters for PivotTable:**

- **Bundesland**: We excluded all Swiss and Austrian plants from the BNA list, but not the ones from Luxemburg as these are part of the German market.
- **Kraftwerksstatus**: in Betrieb + Netzreserve + Sicherheitsbereitschaft + Endgültig stillgeliegt > 2015  
- **Aufnahme der kommerziellen Stromerzeugung** (Start of commercial operation): < 2016,including all blanks

These analyses are used for both the CHP analysis (Step 1 of data generation process) and this analysis, as these cannot really be done separately. Since the BNA's definition of what makes a CHP is *machine based* (i.e. is there a heat delivery mechanism installed) and IEA uses *energy based* definitions of whether fuel use and electricity production is from a CHP (i.e. is it co-produced with heat at a certain efficiency at the tiem of production), one can never get the separate analysis to reproduce the BNA list. All one can hope to achieve is to have the combined CHP and power plant parks in the ETM resemble the combined park from the BNA by technology. The IEA energy balance that needs to be followed mandates the rest.



## Coal 
The electricity production shares from coal-fired technologies are entirely optimized to match fuel use. Also the BNA list specifies that no IGCC plants exist in Germany. The total installed capacity for coal and biomass steam turbines that remain after subtracting CHPs are taken as a target to approach. In the end FLH are slightly tweaked to match these installed capacities better.

| Technology                    | Share | FLH (hrs/yr) | Comment                 |
| :---------------------------- | ----: |---:| :---------------------- |
| Ultra supercritical co-firing |  9.1% |  4,050 | Based on energy balance |
| Ultra supercritical           | 41.0% |  5,000 | Optimized for fuel use  |
| Combined cycle                |  0.0% |   N.R | Not present in Germany  |
| Supercritical                 | 49.9% |  3,600 | Optimized               |


## Gas

The electricity production shares from gas-fired technologies are entirely optimized to match fuel use. The remaining capacities for each technology after subtracting CHPs are taken as a target to approach. For this purpose FLH have also been slightly changed wrt for example the Dutch dataset. 

| Technology | Share | FLH (hrs/yr)| Comment| 
| :--------- |------:| ---:|:-------|
| Turbine               |  4.0% |   375 | Optimized for fuel use  |
| Combined cycle        | 80.0% |  4,400 | Optimized for fuel use  |
| Engine                |  5.0% |  4,500 | Optimized for fuel use  |
| Ultra supercritical   | 11.0% |   700 | Optimized for fuel use  |


## Nuclear

Since there are no 3rd generation nuclear plants yet, the production by 2nd generation nuclear plants is set to 100%. The FLH are set to reflect the installed capacities according to the BNA data.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities from the BNA list and a scaling of FLH in an analysis by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production. 

**N.B.:** We have NOT included Pumpspeicher plants into the Hydro mountain category this year. These will be added as a kind of battery to the flexibility options, hopefully.

| Technology | Installed capacity (MW) | Share | FLH (hrs/yr) |
| :--------- | ----------------------: | ----: | ------: |
| River      |                   3,732 | 90% | 4,576 |
| Mountain   |                    259 | 10% | 7,321 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Wind

The analysis for Inland, coastal and offshore installed wind capacities is called: `20180730_Solar and Wind on and offshore I.xlsx` 
and found in this folder
This leads to the following conclusions:

| Technology | Installed capacity (MW) | Share| FLH (hrs/yr)|
| :--------- | ----------------------: | ----:| ------:|
| Wind turbine coastal |         3,672 | 11.5% |   2,500|
| Wind turbine offshore  |        2,457 |  12.41% |   4,000|
| Wind turbine inland  |          34,839 | 76.1% |   1,730|

For this analysis we assumed the average installed capacity (i.e. the installed capacity that can be said to have produced electricity throughout the year 2012) to be the average of all hours in the year as reported in the 201807_time_series_60min_singleindex_DE_solar_wind.xlsx. 
Also, I analyzed the % coastal wind parks in Niedersachsen, Schleswig-holstein and Mecklenburg-Vorpommern and used this to make the onshore split into coastal and inland. I performed this analysis by looking at the location of the windparks in these states in Google maps. 

For more information on the differences between these kinds of turbines, see the "?" buttons for these technologies in the [ETM](http://pro.et-model.com/scenario/supply/electricity_renewable/wind-turbines) itself. 


## Solar
The analysis for average installed solar PV capacity and FLH is `20180730_Solar and Wind on and offshore I.xlsx`. For this analysis we assumed the average installed capacity (i.e. the installed capacity that can be said to have produced electricity throughout the year 2012) to be the average of all hours in the year as reported in the 201807_time_series_60min_singleindex_DE_solar_wind.xlsx. 

| Technology | Installed capacity (MW) | FLH (hrs/yr)|
| :--------- | ----------------------: | ------:|
| Solar PV |         38,275 | 1,012|

This relies mostly on these sources:

- [Bundesnetzagentur - Power plant list information page](https://www.bundesnetzagentur.de/EN/Areas/Energy/Companies/SecurityOfSupply/GeneratingCapacity/PowerPlantList/PubliPowerPlantList_node.html;jsessionid=C2862D55B8846FD6801ED798624962BC)
- [ Kraftwerksliste der Bundesnetzagentur - Stand 02.02.2018](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/Versorgungssicherheit/Erzeugungskapazitaeten/Kraftwerksliste/Kraftwerksliste_2018_1.xlsx;jsessionid=1D5F9792E7FDCF859099AAD99E002625?__blob=publicationFile&v=3)
- Capacities_DE_Kraftwerksliste_BNetzA_12_2012_brutto_leistung2.xlsx
- 201807_time_series_60min_singleindex_DE_solar_wind.xlsx from: [Open Power System Data.org](https://data.open-power-system-data.org/time_series/2018-06-30/time_series_60min_singleindex.csv) 
- [http://de.wikipedia.org/wiki/Liste_der_Offshore-Windparks](http://de.wikipedia.org/wiki/Liste_der_Offshore-Windparks)
- [http://www.thewindpower.net](http://www.thewindpower.net)
- Deutsche Institut für Wirtschaftsforschung, 2017, update of source below, [Electricity, Heat and Gas Sector Data for Modelling the German System](https://www.diw.de/sixcms/detail.php?id=diw_01.c.574115.de)
- Deutsche Institut für Wirtschaftsforschung, 2014, [Electricity Sector Data for Policy-Relevant Modeling](https://www.google.nl/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCAQFjAA&url=http%3A%2F%2Fwww.diw.de%2Fdocuments%2Fpublikationen%2F73%2Fdiw_01.c.440963.de%2Fdiw_datadoc_2014-072.pdf&ei=fjzSU7OsGcmGOPeYgMgO&usg=AFQjCNGG2MpMl64AngyrCAS8kAvJ7HBGdg&bvm=bv.71667212,d.ZWU)


## Debts

- Hydro Mountain installed capacity in ETM (~1,380 MWe) is much lower than in BNA list (6,505 MWe). Since the latter combined conventional hydro mountain with pumped storage it was unclear how to solve this.
