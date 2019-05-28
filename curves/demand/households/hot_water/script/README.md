### Hot water demand households

The script `probability_distribution_hot_water` is used to generate an aggregated domestic hot water curve. The script is based in
great part on Realistic Domestic Hot-Water Profiles in Different Time Scales, [Jordan (2001)](https://refman.energytransitionmodel.com/publications/2065). See folder "source".

Input is year and country. This input is used to determine the start day of the year and the output folder.

Output is hourly data which sums to 1/3600.

Details about parameters and references to the study can be found in the comments.