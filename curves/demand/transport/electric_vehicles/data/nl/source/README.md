The electric vehicle load curves in the ETM are based on the Movares report ["Laadstrategie Elektrisch Wegvervoer"](https://refman.energytransitionmodel.com/publications/2055), which distinguishes three types of charging strategies: 1) charging everywhere, 2) charging at home, and 3) fast charging. The file `20170509_Movares_original_data.xlsx` can be converted into three input csv files:

* `profile_1.csv`
* `profile_2.csv`
* `profile_3.csv`

Besides the Movares report, we have also used a study by ELaad and Jedlix (["Impact of Smart Charging on EVs Charging Behaviour Assessed from Real Charging Events](https://www.livinglabsmartcharging.nl/nl/praktijk/slim-laden-voorkomt-overbelasting1-energienetwerk)) as an additional source. The file `ELaad_Jedlix_chart_data_v1.xlsx` distinguished two strategies: 4) smart charging, and 5) regular charging. These profiles (`profile_4` and `profile_5`) represent an average day and do not distinguish week or weekend days. Hence, these profiles should be saved to the year specific input folders, both as `hourly_week_profile_[number]` and `hourly_weekend_profile_[number]`.
