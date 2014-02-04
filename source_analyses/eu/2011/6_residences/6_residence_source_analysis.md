# 6. Residence analysis

Most of the cells in the residence analysis dashboard are adjusted to match the IEA energy flows (optimising checks). There is no proper source analysis because of a lack of research data.

1. Application split:
The breakdown is based on a report published by [Enerdata: Energy Efficiency Trends in Buildings in the EU.pdf](http://refman.et-model.com/publications/1841). They report that 2/3 of all final demand in residences is used for space heating (in 2009). 1/6 is consumed in the preparation of hot water.
In the end, the application split is adjusted manually to match IEA statistics.
* Technology split: Space heating: Percentages are adjusted manually until the IEA energy demands are matched. Further research and validation is needed.
* Technology split: Hot water: Percentages are adjusted manually until the IEA energy demands are matched. The hot water split should complement the space heating split. Further research and validation is needed.
* Technology split: Space cooling: All space cooling is accomplished by conventional air conditioning.
* Technology split: Cooking: This split has been taken directly from the NL dataset. Further research and validation is needed.
* Technology split: Appliances: This split has been taken directly from the NL dataset. Further research and validation is needed. Maybe the document [CECED_200604_report on Energy Consumption of Domestic Appliances in EU Households.pdf](http://refman.et-model.com/publications/1843) is helpful for improving this technology split.
* The "Heater characterization (solar thermal, el. add-on)" is taken from the NL dataset. Further research is required.
* The "Old / New Houses Split" is taken directly from the NL dataset. Further research is required. ***Note: All of these entries have to be consistent with their corresponding keys in the country.ad file!***

Other suggested sources:

- [Enerdata_201103_Odyssee European Energy Efficiency trends – Household energy consumption.pdf](http://refman.et-model.com/publications/1842)
- [European Commission_Energy Efficiency Status Report 2012.pdf](http://refman.et-model.com/publications/1844)