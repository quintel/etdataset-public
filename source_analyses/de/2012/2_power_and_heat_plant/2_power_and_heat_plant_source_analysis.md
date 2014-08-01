# 2. Power and heat plant analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.

The Power and heat plant analysis is filled based on enriched data from the German BundesNetzAgentur (BNA). The complete list of power plants and CHPs was obtained from BNA and this was enriched with a column specifying each plant's technology using a document by the Deutsche Institut für Wirtschaftsforschung (DIW) and inferred guesses from each power plant's 'Block name' field entry in the BNA list.
See [de_2012_capacity validation.xlsx](../2_power_and_heat_plant/de_2012_capacity validation.xlsx).

This analysis is used for both the CHP analysis (Step 1 of data generation process) and this analysis, as these cannot really be done separately. Since the BNA's definition of what makes a CHP is *machine based* (i.e. is there a heat delivery mechanism installed) and IEA uses *energy based* definitions of whether fuel use and electricity production is from a CHP (i.e. is it co-produced with heat at a certain efficiency at the tiem of production), one can never get the separate analysis to reproduce the BNA list. All one can hope to achieve is to have the combined CHP and power plant parks in the ETM resemble the combined park from the BNA by technology. The IEA energy balance that needs to be followed mandates the rest.


## Coal 
The electricity production shares from coal-fired technologies are entirely optimized to match fuel use. Also the BNA list specifies that no IGCC plants exist in Germany. The total installed capacity for coal and biomass steam turbines that remain after subtracting CHPs are taken as a target to approach. In the end FLH are slightly tweaked to match these installed capacities better.

| Technology                    | Share | FLH | Comment                 |
| :---------------------------- | ----: |---:| :---------------------- |
| Ultra supercritical co-firing |  9.1% |  5400 | Based on energy balance |
| Ultra supercritical           | 40.0% |  5400 | Optimized for fuel use  |
| Combined cycle                |  0.0% |   N.R | Not present in Germany  |
| Supercritical                 | 50.9% |  3850 | Optimized               |


## Gas

The electricity production shares from gas-fired technologies are entirely optimized to match fuel use. The remaining capacities for each technology after subtracting CHPs are taken as a target to approach. For this purpose FLH have also been slightly changed wrt for example the Dutch dataset. 

| Technology | Share | FLH | Comment| 
| :--------- |------:| ---:|:-------|
| Turbine               |  4.0% |   500 | Optimized for fuel use  |
| Combined cycle        | 80.0% |  4500 | Optimized for fuel use  |
| Engine                |  5.0% |  4500 | Optimized for fuel use  |
| Ultra supercritical   | 11.0% |   700 | Optimized for fuel use  |


## Nuclear

Since there are no 3rd generation nuclear plants yet, the production by 2nd generation nuclear plants is set to 100%. The FLH are set to reflect the installed capacities according to the BNA data.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production. 
As far as Hydro river plants are concerned the FLH have been slightly updated to match the BNA installed capacity. As the Hydro mountain category in the BNA list combined pumped storage and other hydro mountain plants, the calculated installed capacity is much lower than the actual number from BnA. This was ignored for now.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | ----: | ------: |
| River      |                   3,947 (BNA 3,552) | 65.3% |   3,509  (BNA 3,900)|
| Mountain   |                   1,308 | 34.7% |   5,614 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Wind

The analysis for Inland, coastal and offshore installed wind capacities is called: `Wind on and offshore I.xlsx` 
and found in this folder
This leads to the following conclusions:

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | ----: | ------: |
| Wind turbine coastal |         2,196 | 10.4 |   2,400 |
| Wind turbine inland  |        26.981	 | 1.3 |   3,500 |
| Wind turbine inland  |        188  | 88.3 |  1,658 |

For this analysis we assumed the average installed capacity (i.e. the installed capacity that can be said to have produced electricity throughout the year 2012) to be the average of installed capacity on Dec 31st 2011 and Dec 31st 2012. 
Also, I analyzed the % coastal wind parks in Niedersachsen and Schleswig-holstein and used this to make the onshore split into coastal and inland. I performed this analysis by looking at the location of the windparks in these states in Google maps. Assuming Mecklenburg -Vormpommern has a similar share of coastal as does Niedersachsen.

This relies mostly on these sources:

- [ Kraftwerksliste der Bundesnetzagentur - Stand 12.12.2012](http://www.docstoc.com/docs/147959531/Kraftwerksliste-der-Bundesnetzagentur---Stand-12122012)
- Capacities_DE_Kraftwerksliste_BNetzA_12_2012_AW_simplified carriers_corrected techs_final.xlsx
- ÜNB - Szenariorahmen für den Netzentwicklungsplan Strom 2013 - Entwurf 
- http://de.wikipedia.org/wiki/Liste_der_Offshore-Windparks
- http://www.thewindpower.net
- Deutsche Institut für Wirtschaftsforschung, [Electricity Sector Data for Policy-Relevant Modeling](https://www.google.nl/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCAQFjAA&url=http%3A%2F%2Fwww.diw.de%2Fdocuments%2Fpublikationen%2F73%2Fdiw_01.c.440963.de%2Fdiw_datadoc_2014-072.pdf&ei=fjzSU7OsGcmGOPeYgMgO&usg=AFQjCNGG2MpMl64AngyrCAS8kAvJ7HBGdg&bvm=bv.71667212,d.ZWU)

For more information on the differences between these kinds of turbines, see the "?" buttons for these technologies in the [ETM](http://pro.et-model.com/scenario/supply/electricity_renewable/wind-turbines) itself.

## Debts

- Hydro Mountain installed capacity in ETm (~1,380 MWe) is much lower than in BNA list (6,505 MWe). Since the latter combined conventional hydro mountain with pumped storage it was unclear how to solve this.
