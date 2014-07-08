# 11. Area analysis

The following sections document the dashboard inputs in the [Area analysis](../../../../analyses/11_area_analysis.xlsx)area_analysis.xlsx" research analysis:


## General

Some general settings are filled in. These keys are of a technical nature and are used by ETengine and ETmodel.


### ETM modules

These settings determine which modules are turned on/off in ETM.

- analysis_year: is set to 2011, this is the base year (present) that the dataset addresses.
- has_agriculture: TRUE
- has_buildings: TRUE
- has_climate: FALSE, the climate slider module is only applicable to the NL model.
- has_coastline: TRUE
- has_cold_network: FALSE
- has_electricity_storage: FALSE, the storage module is only applicable to the NL model.
- has_employment: FALSE, employment figures have not been researched for EU.
- has_fce: FALSE, the Fuel Chain Emissions module is only applicable to NL.
- has_industry	: TRUE
- has_lignite: TRUE, the EU model has lignite power plants.
- has_merit_order: TRUE
- has_metal: TRUE, the EU model has an industry sub sector 'metal'.
- has_mountains: TRUE, allows for hyrdo mountain power plants
- has_old_technologies: TRUE, allows for 2nd generation nuclear power plants
- has_other: TRUE, the EU has other sector.
- has_solar_csp: TRUE, allows for concentrated solar power.
- has_import_export: TRUE, the EU model displays the import/export module.
- use_network_calculations: FALSE, network calculations are not researched for EU - not part of the data generation process yet.


### Area

- areable_land: obtained from the [World Factbook](https://www.cia.gov/library/publications/the-world-factbook/geos/ee.html).
- coast_line: obtained from the [World Factbook](https://www.cia.gov/library/publications/the-world-factbook/geos/ee.html).
- land_available_for_solar: equal to areable_land.
- number_of_inhabitants: based on Eurostat demo_gind database.
- offshore_suitable_for_wind
- onshore_suitable_for_wind: based on Ecofys data.


### Built environment

Most keys are copied directly from the NL dataset. Only the keys that address 'number of ...' are updated to the EU figures:

- number_buildings: estimated based on floor area from ENTRANZE and floor_area:number_of_buildings ratio in NL.
- number_households: based on the Eurostat lfst_hhnhtych database
- roof_surface_available_pv: scaled figure, based on the NL ratio for solar roof surface / number or residences.
- roof_surface_available_pv_buildings: scaled figure, based on the NL ratio of solar PV on houses/buildings


### CO<sub>2</sub>

See Excel file: "201312_EU27 GHG emissions IPCC format 1990 & 2011.xlsx""
- co2_emission_1990: Extracted from IPCC CRF report for EU 27. Sum of sectors 1A + 2.2.C + 6.6.C
- co2_emission_electricity_1990: set to NL value
- co2_percentage_free: set to NL value
- co2_price: set to NL value

Research data for the EU suggest that total emissions should be 3.55 GT whereas the ETM calculates 3.38 GT. The shortfall in the calculation appears to be a combination of quite a few factors, such as all the assumtpions made in filling in the research analyses, but also the assumed emission factors for fuels, which are more or less global variables in the ETM, but apparently can vary per country (according to national statistics agencies).


### Employment

This module is currently turned off for the EU. Numbers would have to be researched.


### Networks

All keys are set to NL figures. Some of these keys are only relevant if the network module is turned on.


## Debts

- More research and validation is required.
- Onshore and offshore wind potential requires more research.