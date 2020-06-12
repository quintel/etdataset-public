### Building demand space heating - script
The script `buildings_space_heating.py` is used to generate a demand profile (G2A profile) for the Buildings/Services sector and Agriculture sector for different weather years. Please note that this script is only used for historic weather years (1987, 1997, 2004). For recent years (2015 onwards) the profile can be downloaded directly from Gasunie Transport Services (see README in the space_heating folder).

#### How to run

The script requires data about the temperature and wind speed for every hour of the year of interest (year XXXX). For NL, this data can be downloaded from [KNMI](https://projects.knmi.nl/klimatologie/uurgegevens/selectie.cgi). Select the desired date range (1 January XXXX - 31 December XXXX), the data categories 'FH' (wind speed) and 'T' (temperature', and the desired weather station. For NL as a whole we use '260 De Bilt'.

Hit the download button and put the `.txt` file in the `data/nl/XXXX/input` folder.

To run the script, run the following in your terminal:

`python3 <path/to/buildings_space_heating.py nl XXXX`

(where XXXX is the year of interest).

E.g.: `python3 curves/demand/buildings/space_heating/script/buildings_space_heating.py nl 1987`

#### How the script works
The method used to generate the demand profiles is outlined in the Dutch Gas Bill ('gaswet'). It is used by Dutch TSOs and DSOs to predict hourly gas demand. More details can be found [here](https://refman.energytransitionmodel.com/publications/2112).

##### Parameters
In the 'input_data' folder you can find the G2A parameters file. This file contains the following parameters for each hour of the year:

* G2A_TST: a 'reference' temperature
* G2A_RER: a temperature dependent 'slope'
* G2A_TOP: a temperature independent constant

This data originates from [NEDU](https://www.nedu.nl/documenten/verbruiksprofielen/). Combined with temperature and wind speed data, these parameters can be used to generate a demand profile.

The data follows the calendar of the year 2018. It can be applied to different years (using weather data of that year) as the parameters are (largely) not specific to 2018. The parameters do take into account whether a day is a weekend day or holiday, which is of course specific to 2018. However, the impact of this is small.

##### The script
The script first reads the weather data. If year XXXX is a leap year, the last day (31 December) is removed to ensure we have 8760 data points.

For each hour, we calculate the 'average effective daily temperature' `Teff`. This is done by calculating the average daily temperature and the average daily wind speed for each day. A day runs from midnight to midnight, so each hour within the same day has the same average temperature. The effective temperature is defined as:
`average daily temperature - (average daily wind speed / 1.5)`

Secondly, the script reads the parameter file. The script calculates the 'profile fraction' for each hour of the year. It does so by combining the daily effective temperatures of year XXXX with the parameter file. For each hour, we check whether `Teff` is below the reference temperature `G2A_TST` in that hour. If that is the case, the profile fraction for that hour equals:

`G2A_RER * (G2A_TST - Teff) + G2A_TOP`

If not, the profile fraction equals:

`G2A_TOP` (temperature independent constant)

Finally, we normalise the profile to make sure that the profile fractions of each hour sum up to 1/3600.
