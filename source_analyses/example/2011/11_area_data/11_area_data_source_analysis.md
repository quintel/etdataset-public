## 11. Area data analysis

*The Example country is created to show the whole dataset generation process, including the steps that involve obtaining and preparing energy balances - either the proprietary IEA energy balance, or the open source Eurostat enery balance. The Example country is based on a dummy energy balance that is created from the IEA energy balances of two European countries.*

The assumptions in the Area analysis are filled 'nicely' and are not based on sources.

- `has_agriculture` is set to `true` because there is final demand in the agricultural sector.
- `has_climate` is set to `false` because there is currently only a climate module for NL
- idem for `has_employment`, `has_fce`, `has_merit_order` and `use_network_calculations`

## CO<sub>2</sub> emissions

This [European Environmental Agency download site](http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-7/national-greenhouse-gas-inventories-ipcc-common-reporting-format-sector-classification/ascii-delimited-zip/at_download) allows you to download the IPCC Common reporting Format Greenhouse gas emissions for many European countries. 

The source analysis [201409_EEA_NL GHG emissions IPCC format 1990 & 2012.xlsx](../../../nl/2012/11_area/201409_EEA_NL GHG emissions IPCC format 1990 & 2012.xlsx) provides a good method for calculating energetic CO<sub>2</sub> emissions and does so for NL 2012 and 1990. Be sure to apply some filters to the immense file downloaded from the above link. 
Filter by:

- Country_code: NL
- Pollutant_name: CO2
- Year: 1990

Note that this method also allows you to verify if your dataset produces decent CO<sub>2</sub> emissions for the `present_year` (i.e. 2012 for this dataset).

[Energeia](http://www.energeia.nl/) provides regular updates on CO2 ETS prices (look for news items on STEMMING).

We usually use the Cal 16 forward price.

_________

Refer to the source analyses of NL, DE and EU for well-researched examples of the Area data source analyses:

- [NL](../../../nl/2011/11_area_data/11_area_data_source_analysis.md)
- [DE](../../../de/2011/11_area_data/11_area_data_source_analysis.md)
- [EU](../../../eu/2011/11_area_data/11_area_data_source_analysis.md)