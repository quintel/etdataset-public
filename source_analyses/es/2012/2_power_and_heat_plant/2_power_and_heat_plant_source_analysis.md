# 2. Power and heat plant analysis

The dashboard assumption for the first attempt were obtained from the DE 2011 dataset. 


The following changes were made:

- The shares of coal plants, gas plants and nuclear plants were optimized to reduce the error in fuel input. Generally shifting toward lower efficiency technologies compared to the NL 2011 dataset.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--------- | ----------------------: | ----: | ------: |
| River      |                   1,664 |  6.7% |     831 |
| Mountain   |                  14,421 | 93.3% |   1,329 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Debts

- Dashboard assumptions should be researched based on an overview of installed capacities to validate the technology share and full load hours.
- (Solar) It seems that conversion of solar thermal to electricity is not correctly covered by the PP&HP analysis. See [ETdataset#495](https://github.com/quintel/etdataset/issues/495).
