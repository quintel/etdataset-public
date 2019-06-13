DATAPACKAGE: TIME SERIES
===========================================================================

https://doi.org/10.25832/time_series/2019-05-15

by Open Power System Data: http://www.open-power-system-data.org/

Package Version: 2019-05-15

Load, wind and solar, prices in hourly resolution

This data package contains different kinds of timeseries data relevant for
power system modelling, namely electricity consumption (load) for 37
European countries as well as wind and solar power generation and
capacities and prices for a growing subset of countries. The timeseries
become available at different points in time depending on the sources. The
data has been downloaded from the sources, resampled and merged in a large
CSV file with hourly resolution. Additionally, the data available at a
higher resolution (Some renewables in-feed, 15 minutes) is provided in a
separate file. All data processing is conducted in python and pandas and
has been documented in the Jupyter notebooks linked below.

The data package covers the geographical region of 37 European countries.

We follow the Data Package standard by the Frictionless Data project, a
part of the Open Knowledge Foundation: http://frictionlessdata.io/


Documentation and script
===========================================================================

This README only contains the most basic information about the data package.
For the full documentation, please see the notebook script that was used to
generate the data package. You can find it at:

https://nbviewer.jupyter.org/github/Open-Power-System-Data/datapackage_timeseries/blob/2019-05-15/main.ipynb

Or on GitHub at:

https://github.com/Open-Power-System-Data/datapackage_timeseries/blob/2019-05-15/main.ipynb

License and attribution
===========================================================================

Attribution:
    Attribution in Chicago author-date style should be given as follows:
    "Open Power System Data. 2019. Data Package Time series. Version
    2019-05-15. https://doi.org/10.25832/time_series/2019-05-15. (Primary
    data from various sources, for a complete list see URL)."


Version history
===========================================================================

* 2019-05-15 Update with 2018 data
* 2018-06-30 Fixed missing price data
* 2018-03-13 Include data for 2017 where available from primary sources and include hourly load from ENTSO-E Power Statistics
* 2017-07-09 include ENTSO E transparency, RTE, APG
* 2017-03-06  update datasets up to 2016-12-31 and reformat output files
* 2016-10-28 harmonized column names for wind generation
* 2016-10-27 Included data from CEPS and PSE
* 2016-07-14 Included data from Energinet.DK, Elia and Svenska Kraftnaet


Resources
===========================================================================

* [Package description page](http://data.open-power-system-data.org/time_series/2019-05-15/)
* [ZIP Package](http://data.open-power-system-data.org/time_series/opsd-time_series-2019-05-15.zip)
* [Script and documentation](https://github.com/Open-Power-System-Data/datapackage_timeseries/blob/2019-05-15/main.ipynb)
* [Original input data](http://data.open-power-system-data.org/time_series/2019-05-15/original_data/)


Sources
===========================================================================

* ENTSO-E Data Portal and Power Statistics
* TransnetBW
* RTE
* Terna
* Elexon
* 50Hertz
* TenneT
* Energinet.dk
* CEPS
* National Grid
* PSE
* Elia
* ENTSO-E Transparency
* Svenska Kraftnaet
* Amprion
* APG


Field documentation
===========================================================================


time_series_15min_singleindex.csv
---------------------------------------------------------------------------

* utc_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%SZ
    - Description: Start of timeperiod in Coordinated Universal Time
* cet_cest_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%S%z
    - Description: Start of timeperiod in Central European (Summer-) Time
* AT_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Austria in MW as published on ENTSO-E Transparency Platform
    - Source:
* AT_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Austria in MW as published on ENTSO-E Transparency Platform
    - Source:
* AT_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Austria in EUR
    - Source:
* AT_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Austria in MW
    - Source:
* AT_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Austria in MW
    - Source:
* BE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Belgium in MW as published on ENTSO-E Transparency Platform
    - Source:
* BE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Belgium in MW as published on ENTSO-E Transparency Platform
    - Source:
* BE_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Belgium in MW
    - Source:
* BE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Belgium in MW
    - Source:
* BE_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Belgium
    - Source:
* DE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Germany in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Germany in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Germany in MW
    - Source:
* DE_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Germany in MW
    - Source:
* DE_solar_profile
    - Type: number
    - Description: Share of solar capacity producing in Germany
    - Source:
* DE_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Germany in MW
    - Source:
* DE_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Germany in MW
    - Source:
* DE_wind_profile
    - Type: number
    - Description: Share of wind capacity producing in Germany
    - Source:
* DE_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in Germany in MW
    - Source:
* DE_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Germany in MW
    - Source:
* DE_wind_offshore_profile
    - Type: number
    - Description: Share of wind_offshore capacity producing in Germany
    - Source:
* DE_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Germany in MW
    - Source:
* DE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Germany in MW
    - Source:
* DE_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Germany
    - Source:
* DE_50hertz_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in 50Hertz (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_50hertz_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in 50Hertz (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_50hertz_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_offshore_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind_offshore generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in 50Hertz (control area) in MW
    - Source:
* DE_AT_LU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in DE-AT-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_AT_LU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in DE-AT-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_AT_LU_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in DE-AT-LU (bidding zone) in MW
    - Source:
* DE_AT_LU_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in DE-AT-LU (bidding zone) in MW
    - Source:
* DE_AT_LU_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in DE-AT-LU (bidding zone) in MW
    - Source:
* DE_LU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in DE-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_LU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in DE-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_LU_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in DE-LU (bidding zone) in MW
    - Source:
* DE_LU_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in DE-LU (bidding zone) in MW
    - Source:
* DE_LU_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in DE-LU (bidding zone) in MW
    - Source:
* DE_amprion_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Amprion (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_amprion_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Amprion (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_amprion_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Amprion (control area) in MW
    - Source:
* DE_amprion_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in Amprion (control area) in MW
    - Source:
* DE_amprion_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Amprion (control area) in MW
    - Source:
* DE_amprion_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in Amprion (control area) in MW
    - Source:
* DE_amprion_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Amprion (control area) in MW
    - Source:
* DE_tennet_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in TenneT GER (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_tennet_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in TenneT GER (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_tennet_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in TenneT GER (control area) in MW
    - Source:
* DE_transnetbw_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in TransnetBW (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_transnetbw_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in TransnetBW (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_transnetbw_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in TransnetBW (control area) in MW
    - Source:
* HU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Hungary in MW as published on ENTSO-E Transparency Platform
    - Source:
* HU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Hungary in MW as published on ENTSO-E Transparency Platform
    - Source:
* HU_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Hungary in MW
    - Source:
* LU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Luxembourg in MW as published on ENTSO-E Transparency Platform
    - Source:
* LU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Luxembourg in MW as published on ENTSO-E Transparency Platform
    - Source:
* NL_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Netherlands in MW as published on ENTSO-E Transparency Platform
    - Source:
* NL_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Netherlands in MW as published on ENTSO-E Transparency Platform
    - Source:
* NL_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Netherlands in MW
    - Source:
* NL_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Netherlands in MW
    - Source:
* NL_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Netherlands in MW
    - Source:


time_series_30min_singleindex.csv
---------------------------------------------------------------------------

* utc_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%SZ
    - Description: Start of timeperiod in Coordinated Universal Time
* cet_cest_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%S%z
    - Description: Start of timeperiod in Central European (Summer-) Time
* CY_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Cyprus in MW as published on ENTSO-E Transparency Platform
    - Source:
* CY_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Cyprus in MW as published on ENTSO-E Transparency Platform
    - Source:
* CY_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Cyprus in MW
    - Source:
* FR_load_actual_tso
    - Type: number
    - Description: Total load in France in MW as published by RTE
    - Source:
* FR_load_forecast_tso
    - Type: number
    - Description: Day-ahead load forecast in France in MW as published by RTE
    - Source:
* FR_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in France in MW
    - Source:
* FR_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in France in MW
    - Source:
* GB_EAW_load_actual_tso
    - Type: number
    - Description: Total load in England and Wales in MW as published by National Grid
    - Source:
* GB_GBN_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Great Britain in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_GBN_load_actual_gross_generation_tso
    - Type: number
    - Description: Gross generation incl. auto-generation by power plants, pump storage pumping, exports and transmission system losses in Great Britain in MW
    - Source:
* GB_GBN_load_actual_tso
    - Type: number
    - Description: Total load in Great Britain in MW as published by National Grid
    - Source:
* GB_GBN_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Great Britain in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_GBN_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Great Britain in MW
    - Source:
* GB_GBN_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Great Britain in MW
    - Source:
* GB_GBN_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in Great Britain in MW
    - Source:
* GB_GBN_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in Great Britain in MW
    - Source:
* GB_GBN_solar_profile
    - Type: number
    - Description: Share of solar capacity producing in Great Britain
    - Source:
* GB_GBN_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Great Britain in MW
    - Source:
* GB_GBN_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Great Britain in MW
    - Source:
* GB_GBN_wind_generation_actual_dso
    - Type: number
    - Description: Actual wind generation connected to distribution grid in Great Britain in MW
    - Source:
* GB_GBN_wind_generation_actual_tso
    - Type: number
    - Description: Actual wind generation connected to transmission grid in Great Britain in MW
    - Source:
* GB_GBN_wind_profile
    - Type: number
    - Description: Share of wind capacity producing in Great Britain
    - Source:
* GB_GBN_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in Great Britain in MW
    - Source:
* GB_GBN_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Great Britain in MW
    - Source:
* GB_GBN_wind_offshore_profile
    - Type: number
    - Description: Share of wind_offshore capacity producing in Great Britain
    - Source:
* GB_GBN_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Great Britain in MW
    - Source:
* GB_GBN_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Great Britain in MW
    - Source:
* GB_GBN_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Great Britain
    - Source:
* GB_NIR_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Northern Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_NIR_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Northern Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_NIR_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Northern Ireland in MW
    - Source:
* GB_NIR_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Northern Ireland in MW
    - Source:
* GB_NIR_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Northern Ireland in MW
    - Source:
* GB_NIR_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Northern Ireland in MW
    - Source:
* GB_NIR_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Northern Ireland
    - Source:
* GB_UKM_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in United Kingdom in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_UKM_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in United Kingdom in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_UKM_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in United Kingdom in MW
    - Source:
* GB_UKM_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in United Kingdom in MW
    - Source:
* GB_UKM_solar_profile
    - Type: number
    - Description: Share of solar capacity producing in United Kingdom
    - Source:
* GB_UKM_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in United Kingdom in MW
    - Source:
* GB_UKM_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in United Kingdom in MW
    - Source:
* GB_UKM_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in United Kingdom in MW
    - Source:
* GB_UKM_wind_offshore_profile
    - Type: number
    - Description: Share of wind_offshore capacity producing in United Kingdom
    - Source:
* GB_UKM_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in United Kingdom in MW
    - Source:
* GB_UKM_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in United Kingdom in MW
    - Source:
* GB_UKM_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in United Kingdom
    - Source:
* IE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Ireland in MW
    - Source:
* IE_sem_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ireland - (SEM) (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_sem_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ireland - (SEM) (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_sem_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Ireland - (SEM) (bidding zone) in EUR
    - Source:
* IE_sem_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Ireland - (SEM) (bidding zone) in MW
    - Source:


time_series_60min_singleindex.csv
---------------------------------------------------------------------------

* utc_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%SZ
    - Description: Start of timeperiod in Coordinated Universal Time
* cet_cest_timestamp
    - Type: datetime
    - Format: fmt:%Y-%m-%dT%H%M%S%z
    - Description: Start of timeperiod in Central European (Summer-) Time
* AL_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Albania in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* AT_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Austria in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* AT_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Austria in MW as published on ENTSO-E Transparency Platform
    - Source:
* AT_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Austria in MW as published on ENTSO-E Transparency Platform
    - Source:
* AT_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Austria in EUR
    - Source:
* AT_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Austria in MW
    - Source:
* AT_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Austria in MW
    - Source:
* BA_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Bosnia Herzegovina in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* BE_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Belgium in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* BE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Belgium in MW as published on ENTSO-E Transparency Platform
    - Source:
* BE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Belgium in MW as published on ENTSO-E Transparency Platform
    - Source:
* BE_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Belgium in MW
    - Source:
* BE_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Belgium in MW
    - Source:
* BE_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Belgium in MW
    - Source:
* BE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Belgium in MW
    - Source:
* BE_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Belgium
    - Source:
* BG_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Bulgaria in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* BG_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Bulgaria in MW as published on ENTSO-E Transparency Platform
    - Source:
* BG_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Bulgaria in MW as published on ENTSO-E Transparency Platform
    - Source:
* BG_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Bulgaria in MW
    - Source:
* BG_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Bulgaria in MW
    - Source:
* CH_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Switzerland in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* CH_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Switzerland in MW as published on ENTSO-E Transparency Platform
    - Source:
* CH_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Switzerland in MW as published on ENTSO-E Transparency Platform
    - Source:
* CH_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Switzerland in MW
    - Source:
* CH_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Switzerland in MW
    - Source:
* CH_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Switzerland in MW
    - Source:
* CH_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Switzerland in MW
    - Source:
* CH_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Switzerland in MW
    - Source:
* CS_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Serbia and Montenegro in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* CY_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Cyprus in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* CY_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Cyprus in MW as published on ENTSO-E Transparency Platform
    - Source:
* CY_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Cyprus in MW as published on ENTSO-E Transparency Platform
    - Source:
* CY_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Cyprus in MW
    - Source:
* CZ_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Czech Republic in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* CZ_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Czech Republic in MW as published on ENTSO-E Transparency Platform
    - Source:
* CZ_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Czech Republic in MW as published on ENTSO-E Transparency Platform
    - Source:
* CZ_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Czech Republic in MW
    - Source:
* CZ_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Czech Republic in MW
    - Source:
* DE_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Germany in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* DE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Germany in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Germany in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Germany in EUR
    - Source:
* DE_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Germany in MW
    - Source:
* DE_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Germany in MW
    - Source:
* DE_solar_profile
    - Type: number
    - Description: Share of solar capacity producing in Germany
    - Source:
* DE_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Germany in MW
    - Source:
* DE_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Germany in MW
    - Source:
* DE_wind_profile
    - Type: number
    - Description: Share of wind capacity producing in Germany
    - Source:
* DE_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in Germany in MW
    - Source:
* DE_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Germany in MW
    - Source:
* DE_wind_offshore_profile
    - Type: number
    - Description: Share of wind_offshore capacity producing in Germany
    - Source:
* DE_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Germany in MW
    - Source:
* DE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Germany in MW
    - Source:
* DE_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Germany
    - Source:
* DE_50hertz_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in 50Hertz (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_50hertz_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in 50Hertz (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_50hertz_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_offshore_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind_offshore generation in 50Hertz (control area) in MW
    - Source:
* DE_50hertz_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in 50Hertz (control area) in MW
    - Source:
* DE_AT_LU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in DE-AT-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_AT_LU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in DE-AT-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_AT_LU_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for DE-AT-LU (bidding zone) in EUR
    - Source:
* DE_AT_LU_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in DE-AT-LU (bidding zone) in MW
    - Source:
* DE_AT_LU_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in DE-AT-LU (bidding zone) in MW
    - Source:
* DE_AT_LU_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in DE-AT-LU (bidding zone) in MW
    - Source:
* DE_LU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in DE-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_LU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in DE-LU (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_LU_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for DE-LU (bidding zone) in EUR
    - Source:
* DE_LU_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in DE-LU (bidding zone) in MW
    - Source:
* DE_LU_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in DE-LU (bidding zone) in MW
    - Source:
* DE_LU_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in DE-LU (bidding zone) in MW
    - Source:
* DE_amprion_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Amprion (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_amprion_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Amprion (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_amprion_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Amprion (control area) in MW
    - Source:
* DE_amprion_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in Amprion (control area) in MW
    - Source:
* DE_amprion_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Amprion (control area) in MW
    - Source:
* DE_amprion_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in Amprion (control area) in MW
    - Source:
* DE_amprion_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Amprion (control area) in MW
    - Source:
* DE_tennet_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in TenneT GER (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_tennet_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in TenneT GER (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_tennet_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in TenneT GER (control area) in MW
    - Source:
* DE_tennet_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in TenneT GER (control area) in MW
    - Source:
* DE_transnetbw_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in TransnetBW (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_transnetbw_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in TransnetBW (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DE_transnetbw_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_solar_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted solar generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_wind_generation_forecast
    - Type: number
    - Description: Day-ahead forecasted wind generation in TransnetBW (control area) in MW
    - Source:
* DE_transnetbw_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in TransnetBW (control area) in MW
    - Source:
* DK_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Denmark in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* DK_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Denmark in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Denmark in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Denmark in MW
    - Source:
* DK_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Denmark in MW
    - Source:
* DK_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Denmark in MW
    - Source:
* DK_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in Denmark in MW
    - Source:
* DK_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Denmark in MW
    - Source:
* DK_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Denmark in MW
    - Source:
* DK_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Denmark in MW
    - Source:
* DK_1_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in DK1 (bidding zone) in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* DK_1_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in DK1 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_1_load_actual_net_consumption_tso
    - Type: number
    - Description: Total load excl. tansmission system losses in DK1 (bidding zone) in MW
    - Source:
* DK_1_load_actual_tso
    - Type: number
    - Description: Total load in DK1 (bidding zone) in MW as published by Energinet.dk
    - Source:
* DK_1_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in DK1 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_1_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for DK1 (bidding zone) in EUR
    - Source:
* DK_1_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in DK1 (bidding zone) in MW
    - Source:
* DK_1_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in DK1 (bidding zone) in MW
    - Source:
* DK_1_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in DK1 (bidding zone) in MW
    - Source:
* DK_1_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in DK1 (bidding zone) in MW
    - Source:
* DK_2_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in DK2 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_2_load_actual_net_consumption_tso
    - Type: number
    - Description: Total load excl. tansmission system losses in DK2 (bidding zone) in MW
    - Source:
* DK_2_load_actual_tso
    - Type: number
    - Description: Total load in DK2 (bidding zone) in MW as published by Energinet.dk
    - Source:
* DK_2_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in DK2 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_2_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for DK2 (bidding zone) in EUR
    - Source:
* DK_2_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in DK2 (bidding zone) in MW
    - Source:
* DK_2_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in DK2 (bidding zone) in MW
    - Source:
* DK_2_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in DK2 (bidding zone) in MW
    - Source:
* DK_2_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in DK2 (bidding zone) in MW
    - Source:
* DK_energinet_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Energinet (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_energinet_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Energinet (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* DK_energinet_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Energinet (control area) in MW
    - Source:
* DK_energinet_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Energinet (control area) in MW
    - Source:
* DK_energinet_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Energinet (control area) in MW
    - Source:
* EE_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Estonia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* EE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Estonia in MW as published on ENTSO-E Transparency Platform
    - Source:
* EE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Estonia in MW as published on ENTSO-E Transparency Platform
    - Source:
* EE_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Estonia in MW
    - Source:
* EE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Estonia in MW
    - Source:
* ES_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Spain in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* ES_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Spain in MW as published on ENTSO-E Transparency Platform
    - Source:
* ES_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Spain in MW as published on ENTSO-E Transparency Platform
    - Source:
* ES_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Spain in MW
    - Source:
* ES_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Spain in MW
    - Source:
* FI_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Finland in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* FI_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Finland in MW as published on ENTSO-E Transparency Platform
    - Source:
* FI_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Finland in MW as published on ENTSO-E Transparency Platform
    - Source:
* FI_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Finland in MW
    - Source:
* FR_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in France in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* FR_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in France in MW as published on ENTSO-E Transparency Platform
    - Source:
* FR_load_actual_tso
    - Type: number
    - Description: Total load in France in MW as published by own calculation based on RTE
    - Source:
* FR_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in France in MW as published on ENTSO-E Transparency Platform
    - Source:
* FR_load_forecast_tso
    - Type: number
    - Description: Day-ahead load forecast in France in MW as published by own calculation based on RTE
    - Source:
* FR_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in France in MW
    - Source:
* FR_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in France in MW
    - Source:
* GB_EAW_load_actual_tso
    - Type: number
    - Description: Total load in England and Wales in MW as published by own calculation based on National Grid
    - Source:
* GB_GBN_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Great Britain in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* GB_GBN_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Great Britain in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_GBN_load_actual_gross_generation_tso
    - Type: number
    - Description: Gross generation incl. auto-generation by power plants, pump storage pumping, exports and transmission system losses in Great Britain in MW
    - Source:
* GB_GBN_load_actual_tso
    - Type: number
    - Description: Total load in Great Britain in MW as published by own calculation based on National Grid
    - Source:
* GB_GBN_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Great Britain in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_GBN_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Great Britain in GBP
    - Source:
* GB_GBN_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Great Britain in MW
    - Source:
* GB_GBN_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Great Britain in MW
    - Source:
* GB_GBN_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in Great Britain in MW
    - Source:
* GB_GBN_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in Great Britain in MW
    - Source:
* GB_GBN_solar_profile
    - Type: number
    - Description: Share of solar capacity producing in Great Britain
    - Source:
* GB_GBN_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Great Britain in MW
    - Source:
* GB_GBN_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Great Britain in MW
    - Source:
* GB_GBN_wind_generation_actual_dso
    - Type: number
    - Description: Actual wind generation connected to distribution grid in Great Britain in MW
    - Source:
* GB_GBN_wind_generation_actual_tso
    - Type: number
    - Description: Actual wind generation connected to transmission grid in Great Britain in MW
    - Source:
* GB_GBN_wind_profile
    - Type: number
    - Description: Share of wind capacity producing in Great Britain
    - Source:
* GB_GBN_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in Great Britain in MW
    - Source:
* GB_GBN_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Great Britain in MW
    - Source:
* GB_GBN_wind_offshore_profile
    - Type: number
    - Description: Share of wind_offshore capacity producing in Great Britain
    - Source:
* GB_GBN_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Great Britain in MW
    - Source:
* GB_GBN_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Great Britain in MW
    - Source:
* GB_GBN_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Great Britain
    - Source:
* GB_NIR_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Northern Ireland in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* GB_NIR_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Northern Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_NIR_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Northern Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_NIR_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in Northern Ireland in MW
    - Source:
* GB_NIR_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in Northern Ireland in MW
    - Source:
* GB_NIR_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in Northern Ireland in MW
    - Source:
* GB_NIR_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Northern Ireland in MW
    - Source:
* GB_NIR_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in Northern Ireland
    - Source:
* GB_UKM_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in United Kingdom in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* GB_UKM_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in United Kingdom in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_UKM_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in United Kingdom in MW as published on ENTSO-E Transparency Platform
    - Source:
* GB_UKM_solar_capacity
    - Type: number
    - Description: Electrical capacity of solar in United Kingdom in MW
    - Source:
* GB_UKM_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in United Kingdom in MW
    - Source:
* GB_UKM_solar_profile
    - Type: number
    - Description: Share of solar capacity producing in United Kingdom
    - Source:
* GB_UKM_wind_capacity
    - Type: number
    - Description: Electrical capacity of wind in United Kingdom in MW
    - Source:
* GB_UKM_wind_offshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_offshore in United Kingdom in MW
    - Source:
* GB_UKM_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in United Kingdom in MW
    - Source:
* GB_UKM_wind_offshore_profile
    - Type: number
    - Description: Share of wind_offshore capacity producing in United Kingdom
    - Source:
* GB_UKM_wind_onshore_capacity
    - Type: number
    - Description: Electrical capacity of wind_onshore in United Kingdom in MW
    - Source:
* GB_UKM_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in United Kingdom in MW
    - Source:
* GB_UKM_wind_onshore_profile
    - Type: number
    - Description: Share of wind_onshore capacity producing in United Kingdom
    - Source:
* GR_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Greece in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* GR_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Greece in MW as published on ENTSO-E Transparency Platform
    - Source:
* GR_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Greece in MW as published on ENTSO-E Transparency Platform
    - Source:
* GR_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Greece in MW
    - Source:
* GR_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Greece in MW
    - Source:
* HR_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Croatia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* HR_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Croatia in MW as published on ENTSO-E Transparency Platform
    - Source:
* HR_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Croatia in MW as published on ENTSO-E Transparency Platform
    - Source:
* HU_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Hungary in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* HU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Hungary in MW as published on ENTSO-E Transparency Platform
    - Source:
* HU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Hungary in MW as published on ENTSO-E Transparency Platform
    - Source:
* HU_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Hungary in MW
    - Source:
* IE_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Ireland in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* IE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ireland in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Ireland in MW
    - Source:
* IE_sem_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ireland - (SEM) (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_sem_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ireland - (SEM) (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IE_sem_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Ireland - (SEM) (bidding zone) in EUR
    - Source:
* IE_sem_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Ireland - (SEM) (bidding zone) in MW
    - Source:
* IS_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Iceland in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* IT_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Italy in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* IT_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Italy in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Italy in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Italy in MW
    - Source:
* IT_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Italy in MW
    - Source:
* IT_BRNN_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Brindisi (bidding zone) in EUR
    - Source:
* IT_BRNN_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Brindisi (bidding zone) in MW
    - Source:
* IT_CNOR_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in IT-Centre-North (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_CNOR_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in IT-Centre-North (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_CNOR_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Centre-North (bidding zone) in EUR
    - Source:
* IT_CNOR_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Centre-North (bidding zone) in MW
    - Source:
* IT_CNOR_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in IT-Centre-North (bidding zone) in MW
    - Source:
* IT_CNOR_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in IT-Centre-North (bidding zone) in MW
    - Source:
* IT_CNOR_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Centre-North (bidding zone) in MW
    - Source:
* IT_CSUD_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in IT-Centre-South (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_CSUD_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in IT-Centre-South (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_CSUD_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Centre-South (bidding zone) in EUR
    - Source:
* IT_CSUD_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Centre-South (bidding zone) in MW
    - Source:
* IT_CSUD_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in IT-Centre-South (bidding zone) in MW
    - Source:
* IT_CSUD_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in IT-Centre-South (bidding zone) in MW
    - Source:
* IT_CSUD_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Centre-South (bidding zone) in MW
    - Source:
* IT_FOGN_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Foggia (bidding zone) in EUR
    - Source:
* IT_FOGN_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Foggia (bidding zone) in MW
    - Source:
* IT_FOGN_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Foggia (bidding zone) in MW
    - Source:
* IT_GR_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-GR (bidding zone) in EUR
    - Source:
* IT_NORD_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in IT-North (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_NORD_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in IT-North (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_NORD_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-North (bidding zone) in EUR
    - Source:
* IT_NORD_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-North (bidding zone) in MW
    - Source:
* IT_NORD_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in IT-North (bidding zone) in MW
    - Source:
* IT_NORD_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in IT-North (bidding zone) in MW
    - Source:
* IT_NORD_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-North (bidding zone) in MW
    - Source:
* IT_NORD_AT_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-North-AT (bidding zone) in EUR
    - Source:
* IT_NORD_CH_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-North-CH (bidding zone) in EUR
    - Source:
* IT_NORD_FR_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-North-FR (bidding zone) in EUR
    - Source:
* IT_NORD_SI_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-North-SI (bidding zone) in EUR
    - Source:
* IT_PRGP_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Priolo (bidding zone) in EUR
    - Source:
* IT_PRGP_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Priolo (bidding zone) in MW
    - Source:
* IT_PRGP_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Priolo (bidding zone) in MW
    - Source:
* IT_ROSN_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Rossano (bidding zone) in EUR
    - Source:
* IT_ROSN_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Rossano (bidding zone) in MW
    - Source:
* IT_ROSN_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Rossano (bidding zone) in MW
    - Source:
* IT_SACO_AC_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Italy_Saco_AC (bidding zone) in EUR
    - Source:
* IT_SACO_DC_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Italy_Sacodc (bidding zone) in EUR
    - Source:
* IT_SARD_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in IT-Sardinia (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_SARD_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in IT-Sardinia (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_SARD_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Sardinia (bidding zone) in EUR
    - Source:
* IT_SARD_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Sardinia (bidding zone) in MW
    - Source:
* IT_SARD_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in IT-Sardinia (bidding zone) in MW
    - Source:
* IT_SARD_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in IT-Sardinia (bidding zone) in MW
    - Source:
* IT_SARD_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Sardinia (bidding zone) in MW
    - Source:
* IT_SICI_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in IT-Sicily (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_SICI_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in IT-Sicily (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_SICI_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-Sicily (bidding zone) in EUR
    - Source:
* IT_SICI_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-Sicily (bidding zone) in MW
    - Source:
* IT_SICI_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in IT-Sicily (bidding zone) in MW
    - Source:
* IT_SICI_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in IT-Sicily (bidding zone) in MW
    - Source:
* IT_SICI_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-Sicily (bidding zone) in MW
    - Source:
* IT_SUD_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in IT-South (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_SUD_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in IT-South (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* IT_SUD_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for IT-South (bidding zone) in EUR
    - Source:
* IT_SUD_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in IT-South (bidding zone) in MW
    - Source:
* IT_SUD_solar_generation_actual_dso
    - Type: number
    - Description: Actual solar generation connected to distribution grid in IT-South (bidding zone) in MW
    - Source:
* IT_SUD_solar_generation_actual_tso
    - Type: number
    - Description: Actual solar generation connected to transmission grid in IT-South (bidding zone) in MW
    - Source:
* IT_SUD_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in IT-South (bidding zone) in MW
    - Source:
* LT_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Lithuania in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* LT_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Lithuania in MW as published on ENTSO-E Transparency Platform
    - Source:
* LT_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Lithuania in MW as published on ENTSO-E Transparency Platform
    - Source:
* LT_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Lithuania in MW
    - Source:
* LT_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Lithuania in MW
    - Source:
* LU_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Luxembourg in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* LU_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Luxembourg in MW as published on ENTSO-E Transparency Platform
    - Source:
* LU_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Luxembourg in MW as published on ENTSO-E Transparency Platform
    - Source:
* LV_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Latvia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* LV_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Latvia in MW as published on ENTSO-E Transparency Platform
    - Source:
* LV_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Latvia in MW as published on ENTSO-E Transparency Platform
    - Source:
* LV_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Latvia in MW
    - Source:
* ME_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Montenegro in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* ME_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Montenegro in MW as published on ENTSO-E Transparency Platform
    - Source:
* ME_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Montenegro in MW as published on ENTSO-E Transparency Platform
    - Source:
* ME_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Montenegro in MW
    - Source:
* MK_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Former Yugoslav Republic of Macedonia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* MK_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Former Yugoslav Republic of Macedonia in MW as published on ENTSO-E Transparency Platform
    - Source:
* MK_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Former Yugoslav Republic of Macedonia in MW as published on ENTSO-E Transparency Platform
    - Source:
* MK_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Former Yugoslav Republic of Macedonia in MW
    - Source:
* NL_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Netherlands in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* NL_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Netherlands in MW as published on ENTSO-E Transparency Platform
    - Source:
* NL_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Netherlands in MW as published on ENTSO-E Transparency Platform
    - Source:
* NL_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Netherlands in MW
    - Source:
* NL_wind_offshore_generation_actual
    - Type: number
    - Description: Actual wind_offshore generation in Netherlands in MW
    - Source:
* NL_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Netherlands in MW
    - Source:
* NO_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Norway in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* NO_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Norway in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Norway in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Norway in MW
    - Source:
* NO_1_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in NO1 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_1_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in NO1 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_1_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for NO1 (bidding zone) in EUR
    - Source:
* NO_1_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in NO1 (bidding zone) in MW
    - Source:
* NO_2_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in NO2 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_2_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in NO2 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_2_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for NO2 (bidding zone) in EUR
    - Source:
* NO_2_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in NO2 (bidding zone) in MW
    - Source:
* NO_3_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in NO3 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_3_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in NO3 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_3_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for NO3 (bidding zone) in EUR
    - Source:
* NO_3_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in NO3 (bidding zone) in MW
    - Source:
* NO_4_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in NO4 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_4_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in NO4 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_4_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for NO4 (bidding zone) in EUR
    - Source:
* NO_4_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in NO4 (bidding zone) in MW
    - Source:
* NO_5_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in NO5 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_5_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in NO5 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* NO_5_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for NO5 (bidding zone) in EUR
    - Source:
* NO_5_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in NO5 (bidding zone) in MW
    - Source:
* PL_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Poland in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* PL_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Poland in MW as published on ENTSO-E Transparency Platform
    - Source:
* PL_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Poland in MW as published on ENTSO-E Transparency Platform
    - Source:
* PL_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Poland in MW
    - Source:
* PT_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Portugal in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* PT_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Portugal in MW as published on ENTSO-E Transparency Platform
    - Source:
* PT_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Portugal in MW as published on ENTSO-E Transparency Platform
    - Source:
* PT_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Portugal in MW
    - Source:
* PT_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Portugal in MW
    - Source:
* RO_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Romania in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* RO_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Romania in MW as published on ENTSO-E Transparency Platform
    - Source:
* RO_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Romania in MW as published on ENTSO-E Transparency Platform
    - Source:
* RO_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Romania in MW
    - Source:
* RO_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Romania in MW
    - Source:
* RS_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Serbia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* RS_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Serbia in MW as published on ENTSO-E Transparency Platform
    - Source:
* RS_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Serbia in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Sweden in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* SE_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Sweden in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_load_actual_tso
    - Type: number
    - Description: Total load in Sweden in MW as published by Svenska Kraftnaet
    - Source:
* SE_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Sweden in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for Sweden in EUR
    - Source:
* SE_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Sweden in MW
    - Source:
* SE_wind_generation_actual
    - Type: number
    - Description: Actual wind generation in Sweden in MW
    - Source:
* SE_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Sweden in MW
    - Source:
* SE_1_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in SE1 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_1_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in SE1 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_1_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for SE1 (bidding zone) in EUR
    - Source:
* SE_1_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in SE1 (bidding zone) in MW
    - Source:
* SE_2_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in SE2 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_2_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in SE2 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_2_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for SE2 (bidding zone) in EUR
    - Source:
* SE_2_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in SE2 (bidding zone) in MW
    - Source:
* SE_3_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in SE3 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_3_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in SE3 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_3_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for SE3 (bidding zone) in EUR
    - Source:
* SE_3_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in SE3 (bidding zone) in MW
    - Source:
* SE_4_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in SE4 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_4_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in SE4 (bidding zone) in MW as published on ENTSO-E Transparency Platform
    - Source:
* SE_4_price_day_ahead
    - Type: number
    - Description: Day-ahead spot price for SE4 (bidding zone) in EUR
    - Source:
* SE_4_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in SE4 (bidding zone) in MW
    - Source:
* SI_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Slovenia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* SI_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Slovenia in MW as published on ENTSO-E Transparency Platform
    - Source:
* SI_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Slovenia in MW as published on ENTSO-E Transparency Platform
    - Source:
* SI_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Slovenia in MW
    - Source:
* SI_wind_onshore_generation_actual
    - Type: number
    - Description: Actual wind_onshore generation in Slovenia in MW
    - Source:
* SK_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Slovakia in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* SK_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Slovakia in MW as published on ENTSO-E Transparency Platform
    - Source:
* SK_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Slovakia in MW as published on ENTSO-E Transparency Platform
    - Source:
* SK_solar_generation_actual
    - Type: number
    - Description: Actual solar generation in Slovakia in MW
    - Source:
* TR_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Turkey in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* UA_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ukraine in MW as published on ENTSO-E Transparency Platform
    - Source:
* UA_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ukraine in MW as published on ENTSO-E Transparency Platform
    - Source:
* UA_east_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ukraine IPS (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* UA_east_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ukraine IPS (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* UA_west_load_actual_entsoe_power_statistics
    - Type: number
    - Description: Total load in Ukraine BEI (control area) in MW as published on ENTSO-E Data Portal/Power Statistics
    - Source:
* UA_west_load_actual_entsoe_transparency
    - Type: number
    - Description: Total load in Ukraine BEI (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:
* UA_west_load_forecast_entsoe_transparency
    - Type: number
    - Description: Day-ahead load forecast in Ukraine BEI (control area) in MW as published on ENTSO-E Transparency Platform
    - Source:


Feedback
===========================================================================

Thank you for using data provided by Open Power System Data. If you have
any question or feedback, please do not hesitate to contact us.

For this data package, contact:
Jonathan Muehlenpfordt <muehlenpfordt@neon-energie.de>

For general issues, find our team contact details on our website:
http://www.open-power-system-data.org
