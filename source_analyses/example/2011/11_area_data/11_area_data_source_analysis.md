## 11. Area data analysis

*The Example country is created to show the whole dataset generation process, including the steps that consider proprietary IEA energy balances. The Example country is therefore based on a *dummy* energy balance that is created from the IEA energy balances of two European countries.*

The assumptions in the Area analysis are filled 'nicely' and are not based on sources.

- `has_agriculture` is set to `true` because there is final demand in the agricultural sector.
- `has_climate` is set to `false` because there is currently only a climate module for NL
- idem for `has_employment`, `has_fce`, `has_merit_order` and `use_network_calculations`


Refer to the source analyses of NL, DE and EU for well-researched examples of the Area data source analyses:

- [NL](../../../nl/2011/11_area_data/11_area_data_source_analysis.md)
- [DE](../../../de/2011/11_area_data/11_area_data_source_analysis.md)
- [EU](../../../eu/2011/11_area_data/11_area_data_source_analysis.md)