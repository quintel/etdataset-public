# 2. Power and heat plant analysis

The dashboard assumption for the first attempt were obtained from the NL 2011 dataset.

The Power and heat plant analysis is filled based on the Platts data. See [uk_2012_installed_capacities.xlsm](../2_power_and_heat_plant/uk_2012_installed_capacities.xlsm).

The following changes are made:


## Coal and lignite

Platts only reports electricity production by coal plants using steam turbines. The electricity production is therefore divided over the Supercritical and Ultra supercritical power. This is done to to match the calculated fuel input with the energy balance. The electricity production shares are:

| Technology | Production share | Comment |
| :--- | ---: | :-- |
| Ultra supercritical co-firing | 9.4% | Based on energy balance |
| Ultra supercritical | 23.3% | Optimized |
| Supercritical | 67.3% | Optimized |

The full load hours (FLH) are set on the average FLH calculated based on the total electricity production and total installed capacity: 5,370 h.


## Gas

An initial split of the electricity production is based on the default FLH and the installed capacities reported by Platts for the Turbine, Combined cycle, Engine and Ultra supercritical. With the default FLH and the intial share, the calculated fuel input was too low. The share of the Ulta supercritical (lower efficiency) is therefore increased and the Combined cycle (high efficiency) is decreased. Increase of the production with Ultra supercritical resulted in an increase in installed capacity. The FLH of the Ultra supercritical are therefore increased to 2000 h to ensure a installed capacity that matches the Platts data.

| Technology | Capacity | Default FLH | Initial share | Final share | Final FLH |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Turbine | 916 | 700 | 0.4% | 0.4% | 700 |
| Combined cycle | 29,036 | 4200| 99.0% | 66.9% | 4200 |
| Engine | 362 | 700 | 0.2% | 0.2% | 700 |
| Ultra supercritical | 816 | 700 | 0.5% | 32.5% | 1750 |


## Nuclear

Since there are no 3rd generation nuclear plants yet, the production by 2nd generation nuclear plants is set to 100%. The electricity production is matched with the installed capacity reported by Platts by setting the FLH to 6,521 h.


## Hydro

The share between hydro river and hydro mountain are estimated based on the installed capacities researched by Ecofys. The full load hours (FLH) are subsequently calculated using the installed capacities and the electricity production.

| Technology | Installed capacity (MW) | Share | FLH (h) |
| :--- | ---: | ---: | ---: |
| River | 141 | 5.4% | 2,023 |
| Mountain | 1,545 | 94.6% | 3,236 |

See [hydro_source_analysis.xlsx](../../../eu/2012/2_power_and_heat_plant/hydro_source_analysis.xlsx).


## Oil products

The FLH of oil plants (Oil supercritical and Diesel engine) are set to the average FLH based on total electricity production from the energy balance and the total installed capacity from Platts: 235 h.


## Issues

- (Hydro) Production shares and FLH of hydro river and hydro mountains need to be researched.
- (Solar) FLH of solar need to be researched.
- (Wind) FLH of wind turbines need to be researched.