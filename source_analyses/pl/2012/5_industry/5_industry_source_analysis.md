# 5. Industry analysis

This analysis does not require any inputs by the user. All calculations are based on the energy balance and inputs from the metal and chemical analyses.


Issues:

- Negative final demand for woodpellets. Most likely cause by allocation in CHP analysis. See also [ETdataset#175](https://github.com/quintel/etdataset/issues/175).

- [SOLVED] Own use of coal is negative. Results in a >1 and <0 parent share in the industry_transformation_generic_coal converter.
