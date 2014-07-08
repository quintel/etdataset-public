# 7. Services analysis


## Application splits

The application split and technology shares are calculated in the [7_services_source_analysis.xlsx](7_services_source_analysis.xlsx). 

On the 'Electricity' sheet it is decided how much of the final demand for electricity is used by which application. This split for final electricity demand is based on a breakdown by [Fleiter et al. (2010) Electricity demand in the European services sector: A detailed bottom-up estimate by sector and by end-use](https://www.google.nl/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCAQFjAA&url=http%3A%2F%2Fwww.isi.fraunhofer.de%2Fisi-wAssets%2Fdocs%2Fe%2Fde%2Fpublikationen%2FIEECB__10_No50_Final_2.pdf&ei=YhqxU-jzFoHSOff7gYgB&usg=AFQjCNHFhhsCr383s_KlO6h5r0Npk6qOEg&bvm=bv.69837884,d.ZWU), figure 8: 'Share of energy service in total electricity demand by country'.

The 'Fuel aggregation' sheet is used to decide how much of which carrier is consumed for each application. A couple of assumptions are made:

- All coal, wood pellets (biomass) and solar thermal energy is consumed in space heating.
- 90% of all oil and gas demand are used in space heating, the remaining 10% in the other applications.
- Electricity is distributed over applications according to the breakdown derived on the 'Electricity' sheet.


## Technology shares

Now, the total final demands per application are known. Third, the technology split for space heating is derived:


## Space heating

With the information from above, it is easy to derive the technology split for space heating. The final demands in space heating are converted to useful demands by applying the conversion efficiency. In a final step, the useful demand percentages are derived. It is assumed that the converters "Electric heat pumps with thermal storage" and "Gas-fired heat pumps" do not exist in the EU.


## Space cooling

It is assumed that all space cooling is accomplished by conventional air-conditioning.


## Lighting

The following technology split is assumed, without further research:

| Technology                  | Share |
| :-------------------------- | ----: |
| Standard fluorescent tubes  | 80.0% |
| Efficient fluorescent tubes | 20.0% |
| LED tubes                   |  0.0% |


## Debts

- The technology split for lighting requires more research.
- Demand for other carriers is appr. 700 TJ. This energy use is not accounted for in the ETM.
