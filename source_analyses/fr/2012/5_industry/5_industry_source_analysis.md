# 5. Industry analysis

This analysis does not require any inputs by the user. All calculations are based on the energy balance and inputs from the metal and chemical analyses.


Issues:

- Negative final demand for woodpellets in the chemical sector, resulting in shares that are <0 and >1. Most likely caused by allocation in CHP analysis. See also [ETdataset#175](https://github.com/quintel/etdataset/issues/175).

- [SOLVED] #DIV/0 error in the non-energetic final demand share for coal as result of 0 TJ final demand for both the chemical and other industry. Add IF statement as with wood pellets.
