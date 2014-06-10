# 2. Power and heat plant analysis

The dashboard assumption for the first attempt were obtained from the DE 2011 dataset.

The following changes are made:
- Percentage wind turbines offshore is set to 0% because there is no offshore wind yet. According http://www.thewindpower.net/country_maps_en_27_poland.php all wind farms are still 'planned'.
- Shares of coastal and inland turbines are optimized to match installed capacity. According http://www.thewindpower.net/country_en_27_poland.php the installed capacity was 2,497 by the end of 2012.


Potential sources:

- PAIZ (-) Energy Sector in Poland
  * Installed capacity: 37.4 GW
  * Electricity generation in Poland by source (Figure 2): 88% coal, 3% gas, 3% biomass, 2% hydro, 2% wind and geothermal, 2% oil.
  * Electricity from renewable sources (Table 4); generated energy by the end of September 2012: 124 MW biogas plants, 559 MW biomass plants, 1,251 MW PV plants, 2341 MW wind plants, 958 MW hydro plants
  * Thermal energy 462.5 PJ, from which 343 PJ sold. Mainly produced from hard coal (79%). Installed capacity of licenced heat producers was 59.2 GW, from which 58.1 GW generating capacity.
- GUS (2013) Energy Statistics 2011-2012
  * Heat generation in heat-only boilers in public thermal plants, public heat plants and non-public heat plants (p. 81-83)
  * Transformation in run-of-river hydro plants (p. 72), pumped-storage hydro plants (p. 72), wind plants (p. 84), biomass and wastes plants (p. 85), solar PV plants (p. 85)
  * Heat output vs sector and input for autoproducing heat plants (p. 228)


Issues:

- Assumptions for power plants are generally not relevant because the electricity production from most powerplants is zero.
- Main activity heat plants are important in Poland and requires therefore more attention.
- (Hydro) Production shares of hydro plants need to be researched
- (Wind) Production shares of wind turbines need to be researched.
- (Main activity heat plants) In general, the calculated fuel inputs for main activity heat plants are highter than the reported fuel inputs.
- (FLH) Full load hours need to be researched based on installed capacities.

- [SOLVED] There is no main activity electricity production reported on the energy balance, exept for hydro and wind. It seems that everything is covered by main activity CHP plants. Zero values result in #DIV/0 errors for the electricity production by coal plants in the analysis.