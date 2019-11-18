## Generating solar production curves and full load hours (FLH) values for weather years

The solar load curves which are based on data provided by the [Open Power System Data platform](https://data.open-power-system-data.org) are not available for the weather years (1987, 1997, 2004). That is why we use measured irradiation data and convert that to production.

### Script to process irradiation data
The file `process_irradiation_data.py [country] [year]` collects hourly KNMI irradiation data for a specific year and weather station. Since this feature is only available for the Netherlands, specifying `nl` as a country collects data from the weather station 260 (De Bilt). The hourly irradiation data is converted to a normalized solar curve. As with all load profiles, we normalize the load profiles to 1/3600. This results in the following output csv files:

* `solar_pv.csv`

### Source of irradiation data

**Irradiation data**: The irradiation data is downloaded from the KNMI database using the [KNMY library](https://knmy.readthedocs.io/en/latest/). We use weather station 260: De Bilt.


### Determining the full load hours

The full load hours for the weather years (1987, 1994, 2004) are scaled based on the yearly total irradiation using our default `nl` (2015) dataset as a reference year. 

For our default `nl` dataset the full load hours for solar PV are calculated based on the average horizontal and optimal yearly global irradiation and a performance ratio (of 83%). This key figure is used for other datasets (e.g., 2016 and 2017) of the Netherlands as well. According to the [KNMI](https://www.knmi.nl/nederland-nu/klimatologie/maand-en-seizoensoverzichten/2015/jaar), 2015 was a very sunny year (1894 sun hours compared to an average of 1639 sun hours), implying that a number of 867 full load hours is probably too low. To determine the full load hours for the weather years (1987, 1997, 2004) the reference number of full load hours for 2015 was scaled up based on the number of yearly sun hours, resulting in 1894 / 1639 * 867 = 1002 full load hours (check `Q_2015_STN260_analysis.xlsx` for the analysis). This value, as well as the total yearly irradiation, was used to determine the full load hours for the weather years:

full load hours (year) = full load hours (2015) / total irradiation (2015) * total irradiation (year)