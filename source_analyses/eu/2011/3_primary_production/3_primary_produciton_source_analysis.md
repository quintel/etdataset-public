# 3. Primary production

## Time curves for Coal, Lignite, Natural gas, Crude oil, Uranium oxide and Bio-residues

Tine curves are forecasted (extrapolated from historic data) in the Python script [projecting_timecurves_2000_2050](projecting_timecurves_2000_2050) (use, for example, Enthought Canopy to run/edit the script).

The script contains historic data of carrier production for the years 2000 - 2010. These data points are obtained from Eurostat (see Eurostat tables in Sources/Eurostat tables). The data points for 2011 are obtained from the energy balance.

Based on these data points, the annual production is extrapolated with a linear fitting until 2050.

Running the script will generate the file [extrapolation_production_trends.csv](extrapolation_production_trends.csv) in the same directory that the script is located in.

The extrapolated curves are then copied and pasted manually into the Excel file [timecurves_source_analysis.xlsx](timecurves_source_analysis.xlsx). This file contains the historic trend and the forecast (it also points to the sources of the research data).

The resulting time curves are used in the "3_primary_production_analysis.xlsx" research analysis.


## Other dashboard input

The Dashboard of "3_primary_production_analysis.xlsx" research analysis also contains he following input:

* Domestic production in 2011: Bio-oil: a dummy value was filled in, lack of research data
* Maximum domestic production in 2011
  * Biogenic waste: a dummy value was filled in, lack of research data
  * Non-biogenic waste: a dummy value is filled in, lack of research data
* The "Wood pellet production" is estimated without proper research:
  - Percentage of wood converted to wood pellets: 95.0%
  - Percentage of wood converted to torrified biomass pellets: 5.0%

