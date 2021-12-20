## POTENCIA

The potencia script elegantly downloads neccesary files from the study from
https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/POTEnCIA, extracts ETM data
for all designated countries, and merges this data into csv files. The downloaded
files are automatically removed in the end.

Make sure to have `pandas` and `openpyxl` installed to use this script.

At the top of the script you can alter some parameters:
- **POTENCIA_YEAR** The year of the Potencia study. This year is used to build the url. Default 2018.
- **ANALYSIS_YEAR** The analysis year you want to extract from the data. E.g. 2019 will have the script output 2019 data for all countries.
- **COUNTRY_CODES** The countries you want to add to the output csvs. Make sure these countries are available in the potencia study.
- **TAB_KEYS** The files and tabs of the Potencia study you want to extract. You can add extra tabs to the existing `TAB_KEYS`, and these will show up in your output without any further action needed. If you want to add a whole new file to the extraction, you should add new `TAB_KEYS`, a `SHORT`, a conversion of the short to the folder where this file lives (in `det_yearly_file` around line 45), and a new little extraction block at the bottom of the script (you can copy the one for RESIDENCES or TERTIARY for example) for your new file.

The output will be a csv file for every tab key you specified at the top of the script.
Each csv contains the requested countries as columns, and the rows will equal the
ones from the original Potencia tab.
