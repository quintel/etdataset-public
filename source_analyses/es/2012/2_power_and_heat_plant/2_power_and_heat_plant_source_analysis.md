# 2. Power and heat plant analysis

The dashboard assumption for the first attempt were obtained from the DE 2011 dataset. 


The following changes were made:

- The shares of coal plants, gas plants and nuclear plants were optimized to reduce the error in fuel input. Generally shifting toward lower efficiency technologies compared to the NL 2011 dataset.


Issues:

- Dashboard assumptions should be researched based on an overview of installed capacities to validate the technology share and full load hours.
- (Solar) It seems that conversion of solar thermal to electricity is not correctly covered by the PP&HP analysis. See https://github.com/quintel/etdataset/issues/495.
