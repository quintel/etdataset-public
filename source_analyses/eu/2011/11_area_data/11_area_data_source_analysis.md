# 11. Area analysis

The following sections document the dashboard inputs in the [Area analysis](../../../../analyses/11_area_analysis.xlsx)area_analysis.xlsx" research analysis:


## General

Some general settings are filled in. These keys are of a technical nature and are used by ETEngine and ETModel.


### ETM modules

These settings determine which modules are turned on/off in ETModel.

- analysis_year: is set to 2011. This is the base year (present) that the dataset addresses.
- has_agriculture: TRUE
- has_buildings: TRUE
- has_climate: FALSE. The climate slider module is only applicable to the NL model.
- has_coastline: TRUE
- has_cold_network: FALSE
- has_electricity_storage: FALSE. The storage module is only applicable to the NL model.
- has_employment: FALSE. Employment figures have not been researched for EU.
- has_fce: FALSE. The Fuel Chain Emissions module is only applicable to NL.
- has_industry	: TRUE
- has_lignite: TRUE. The EU model has lignite power plants
- has_merit_order: TRUE
- has_metal: TRUE. The EU model has an industry sub sector 'metal'.
- has_mountains: TRUE. Allows for hyrdo mountain power plants
- has_old_technologies: TRUE. Allows for 2nd generation nuclear power plants
- has_other: TRUE. EU has other sector.
- has_solar_csp: TRUE. Allows for concentrated solar power.
- has_import_export: TRUE. EU model displays the import/export module.
- use_network_calculations: FALSE. Network calculations are not researched for EU - not part of the data generation process yet.


### Area

Most of the area attributes are found in the [CIA Factbook](https://www.cia.gov/library/publications/the-world-factbook/geos/ee.html).
Only the 'land_available_for_solar' is not researched properly. The NL value is scaled up, according to the land surface ratio of the EU and NL.


### Built environment

Most keys are copied directly from the NL dataset. Only the keys that address 'number of ....' are updated to EU figures:

- number_buildings: After the number_households is known, the number_buildings is scaled up according to the EU/NL ratio of number_households.
- number_households: Go to the Eurostat website > Statistics > Population > Data > Database > Population > Census > Private househoulds by size, composition and presence of elderly members. This provides the total number of residences in the EU (per country). This information is also included in "11_area_data_source_analysis.xlsx", sheet "number of residences". It turns out that the total number of residences is 190,912,746.
- number_of_existing_households: same as number_households.
- number_of_new_residences: breaking down number_households accoding to NL percentage_of_new_houses (equivalent to applying the NL key percentage_of_new_houses
- number_of_old_residences: number_households - number_of_new_households
- roof_surface_available_pv: Scaled figure, based on the NL ratio for solar roof surface / number or residences.
- roof_surface_available_pv_buildings: Scaled figure, based on the NL ratio of solar PV on houses/buildings


### CO<sub>2</sub>

See Excel file: "201312_EU27 GHG emissions IPCC format 1990 & 2011.xlsx""
- co2_emission_1990: Extracted from IPCC CRF report for EU 27. Sum of sectors 1A + 2.2.C + 6.6.C
- co2_emission_electricity_1990: set to NL value
- co2_percentage_free: set to NL value
- co2_price: set to NL value

Research data for EU27 suggest that total emissions should be 3.55 GT whereas the ETM calculates 3.38 GT. The shortfall in the calculation appears to be a combination of quite a few factors, such as all the assumtpions made in filling in the research analyses, but also the assumed emission factors for fuels, which are more or less global variables in the ETM, but apparently can vary per country (according to national statistics agencies).


### Employment

This module is currently turned off for EU27. Numbers would have to be researched.


### Transport

km_per_car
km_per_truck

Keys are set to NL figures. These are not terribly relevant, as they are only used to convert final demand for fuel into useful energy (car and truck kilometres). This will have and effect when comparing the impact of cars and trucks with strongly varying efficiencies.


### Networks

All keys are set to NL figures. Some of these keys are only relevant if the network module is turned on.


## Shortcomings

Many keys are not researched properly, see explanations above. Especially, the keys that are based on an EU/NL scaling should be researched properly.