# Sources wind weather years 1987 

### Onshore/coastal data
The onshore data is downloaded from the [KNMI KNMY database](https://knmy.readthedocs.io/en/latest/) using `process_wind_speed_data.py`.
We use station 240: Schiphol.

### Offshore data
The offshore data is downloaded from [KNMI - Uurgegevens van Noordzee stations](https://www.knmi.nl/nederland-nu/klimatologie/uurgegevens_Noordzee).
We use Station 320 - Lichteiland Goeree as this station has the best data availability for the weather years. File: `uurgeg_320_1981-1990.txt`.

### Offshore data 1987
Weatherstation 320 does not have a complete dataset for 1987. Therefor we used data from the [KNMI datacenter](https://data.knmi.nl/datasets/KNW-CSV-TS/1.0?bbox=51.9,3.8,51.8,3.7&dtend=1987-12-31T22:59Z&q=knw&dtstart=1986-12-31T23:00Z).
