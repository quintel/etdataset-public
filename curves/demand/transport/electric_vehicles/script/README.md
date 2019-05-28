The original Movares data is given for weekdays and weekend days on a 15-minute basis for 1 day, which can be found in the input csv files:

* `profile_1.csv`
* `profile_2.csv`
* `profile_3.csv`

This original data is turned into two separate files for weekdays and weekend days and the resolution is changed to hourly by running `20170509_15minutes_to_hours.py [country] [year]`, where the country and year must be specified. For example, if the load curves for the Netherlands, 2013 dataset should be generated, `20170509_15minutes_to_hours.py nl 2013` must be run.

In turn, these week and weekend day profiles are stitched together to form an annual profile by running `20170509_daily_to_annual.py [country] [year]`, resulting in 3 output csv files:

* `electric_vehicle_profile_1.csv`
* `electric_vehicle_profile_2.csv`
* `electric_vehicle_profile_3.csv`

Running the script also results in profiles based on the ELaad data:

* `electric_vehicle_profile_4.csv`
* `electric_vehicle_profile_5.csv`

Currently, the year specific nl load curves are used for all other datasets.
