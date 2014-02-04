# 7. Services analysis

## Application split

The application split is calculated in the Excel file [7_services_source_analysis.xlsx](7_services_source_analysis.xlsx). Please refer to that document while continuing with this documentation.

First, it is decided how much of the final demand for electricity is used by which application. This split for final electricity demand is based on a breakdown by [European Commission_Energy Efficiency Status Report 2012.pdf](http://refman.et-model.com/publications/1844), page 109: Figure 83 "Tertiary electricity consumption breakdown in the EU-27". See Excel workbook sheet "el. breakdown".

Second, the fuel aggregation sheet of the EU services research analysis is used to decide how much of which carrier is consumed in each sector. See Excel workbook sheet "Fuel aggregation".
A couple of assumptions are made:

- All coal, wood pellets (biomass) and solar thermal energy is consumed in space heating
- 90% of all oil and gas demand are used in space heating, the remaining 10% in the 'other' application
- electricity is distributed over applications according to the breakdown derived on the "el. breakdown" sheet.

Now, the total final demands per application are known. Third, the technology split for space heating is derived:


## Technology split: Space heating

With the information from above, it is easy to derive the technology split for space heating. The final demands in space heating are converted to useful demands by applying the conversion efficiency.
In a final step, the useful demand percentages are derived.
It is assumed that the converters "Electric heat pumps with thermal storage" and "Gas-fired heat pumps" do not exist in the EU.


## Technology split: Space cooling

It is assumed that all space cooling is accomplished by conventional air-conditioning.


## Technology split: Lighting

The following technology split is assumed, without further research:

- Standard fluorescent tubes: 80.0%
- Efficient fluorescent tubes: 	20.0%
- LED tubes: 0.0%