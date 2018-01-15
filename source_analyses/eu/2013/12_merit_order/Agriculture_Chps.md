The file `agriculture_profile.py` found at <https://github.com/quintel/modeling_experiments/blob/master/load_curves/agriculture_profile.py> is used to generate a `agriculture_chp.csv` files for all European countries and Brazil. These `agriculture_chp.csv` files provide profiles used in the Merit Order to provide the electricity production per hour for these must-run technologies. 


#### Scripts creating profile

The profile assumes that the CHPs run Monday until Friday and are off on Saturday and Sunday. From Monday until Friday the CHPs are switched on after 6 hours inactivity and run for 16 hours. The last two hours of the day they are not active. This provides a cycle during weekdays of 8 hours off followed by 16 hours on.  

The script is written and designed such that profiles can be generated according to year. This helps to avoid issues that could occur due to variations in the dates of weekdays and weekend days.

To avoid errors that occur during leap years (for example 2012), the script creates a profile for the first 8760 hours of a year. 

The total electricity output of all 8760 hours is normalized to a total of 1/3600 as explained in the `profile_generation_guidelines.md` file found at <https://github.com/quintel/merit/blob/master/profile_generation_guidelines.md>.

Furthermore, the profile assumes that the CHPs will run on 80 % of normal capacity during the summer months May until and including September.



