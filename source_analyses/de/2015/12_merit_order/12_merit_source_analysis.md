# Merit order load profiles

Hourly load profiles are used in the merit order module to determine the availability of volatile electricity sources and the run profiles of must-run technologies. The sources of these load profiles as well as the load profiles themselves are stored in ETDataset. These load profiles are then copied to `etsource/datasets/de/load_profiles`.

Both wind and solar pv profiles are based on data provided by the Open Power System Data platform (https://data.open-power-system-data.org/). The specific data used in this analysis has been downloaded from https://data.open-power-system-data.org/time_series/, choosing the 60 minutes resolution and filtering for only the 2015 data for Germany. According to the website, the underlying data for solar pv and wind profiles are the measured generation curves as provided by the four German TSO's. 

## Wind load profiles

The 2015 data does not make the split between onshore and offshore production, the 2016 data does. In order to guarantee consistency between profiles for different technologies, we have chosen to use the 2015 data and use the same profile for wind offshore, wind coastal and wind onshore. These profiles are corrected to make sure that they match the full load hours as determined in the Power and heat plant analysis. As with all load profiles, we normalize the load profiles to 1/3600.

## Solar pv load profiles

The solar pv profile can be directly read from the 2015 data. The resulting full load hours are used to set the limits of the corresponding full load hours slider.
