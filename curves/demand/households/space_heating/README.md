### Heat demand curves

The heat demand curves are based on ECN data. For raw data see file "warmtevraagprofielen.xlsx". These curves relate the year 1987.

We use the relationship between irradiance and temperature data and the heat demand curves to generate heat demand curves for other years.

The files `insulation_data.py` and `insulaton_classes.py` reproduce the ECN curves from irradiation and temperature data. The file `fitting.py` shows a comparison between the ECN curve for 1987 and the constructed curve. 

The relationship between irradiation and temperature data and the heat demand curves determined from the 1987 data can also be used to construct heat demand curves for other years and countries. The file `heat_demand_profile_generator.py` enables you to do so. This file is extracts input data (irradiation and temperature) from the country and year defined and gives heat demand curves as output. 