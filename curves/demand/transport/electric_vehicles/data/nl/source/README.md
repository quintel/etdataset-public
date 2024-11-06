In the ETM 5 electric vehicle load curves are used:
* `electric_vehicle_profile_1.csv` : Charging at public places
* `electric_vehicle_profile_2.csv` : Charging at home
* `electric_vehicle_profile_3.csv` : Fast charging
* `electric_vehicle_profile_4.csv` : Charging at work
* `electric_vehicle_profile_5.csv` : Custom profile.

The load curves 1,2, and 4 are generated using the [ELaad profile generator](https://platform.elaad.io/analyse/low-voltage-charging-profiles/).
1000 runs for each of the three categories have been generared, and aggregated to 1 profile for each category.


The electric vehicle load curves 3 and 5 in the ETM are based on the Movares report ["Laadstrategie Elektrisch Wegvervoer"](https://refman.energytransitionmodel.com/publications/2055), which distinguishes three types of charging strategies: charging everywhere, charging at home and fast charging. The file `20170509_Movares_original_data.xlsx` can be converted into three input csv files. We have used the fast charging profile for our fast charging profile in the ETM, and we have used the charging everywhere profile as placeholder for our custom profile.



