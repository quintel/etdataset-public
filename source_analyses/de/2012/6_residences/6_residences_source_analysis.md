# 6. Residences analysis

The dashboard assumptions for the first attempt were obtained from the DE 2011 dataset.


## Application split

The final demand for space heating, hot water, lighting, cooking and appliances are estimated roughly based on the Odyssee 2011 data. The 2011 values are scaled to the final demand in 2012 taken from the IEA energy balance. The "Energieverbrauch der privaten Haushalte" table from [DESTATIS](https://www.destatis.de/DE/ZahlenFakten/GesamtwirtschaftUmwelt/Umwelt/UmweltoekonomischeGesamtrechnungen/EnergieRohstoffeEmissionen/Tabellen/EnergieverbrauchHaushalte.html) might be useful to validate the application split.


## Space heating

The technology split for space heating are based on Ecofys data. The percentages are adjusted manually to match the IEA energy demand. 

| Technology                    | Calc. share | Final share |
| :---------------------------- | ----------: | ----------: |
| Condensing combi boiler       |       14.0% |       13.7% |
| Solar thermal panels          |        0.0% |        1.3% |
| Gas-fired heat pump (ground)  |        0.0% |        0.0% |
| Gas-fired micro CHP           |        0.0% |        0.0% |
| District heating              |       10.0% |        9.2% |
| Electricity-driven heat pump  |        0.0% |        0.0% |
| Woodpellets (biomass) heaters |       14.0% |       14.6% |
| Electric heaters (resistance) |        3.0% |        1.5% |
| Gas-fired heaters             |       31.0% |       30.2% |
| Oil-fired heaters             |       28.0% |       27.8% |
| Coal-fired heaters            |        0.0% |        1.7% |
| Electric heat pump add-on     |        0.0% |        0.0% |


## Hot water

The technology split for hot water are based on Ecofys data. The percentages are adjusted manually to match the IEA energy demand. 

| Technology                    | Calc. share | Final share |
| :---------------------------- | ----------: | ----------: |
| Condensing combi boiler       |       12.0% |       12.6% |
| Solar thermal panels          |        0.0% |        1.3% |
| Gas-fired heat pump (ground)  |        0.0% |        0.0% |
| Gas-fired micro CHP           |        0.0% |        0.0% |
| District heating              |        4.4% |        4.6% |
| Electricity-driven heat pump  |        0.3% |        0.3% |
| Woodpellets (biomass) heaters |        3.4% |        3.7% |
| Electric heaters (resistance) |       29.6% |       24.2% |
| Gas-fired heaters             |       30.5% |       32.1% |
| Oil-fired heaters             |       19.9% |       20.9% |
| Coal-fired heaters            |        0.0% |        0.3% |
| Electric heat pump add-on     |        0.0% |        0.0% |


## Debts

- Technology splits for space cooling, lighting, cooking and appliances need to be researched.
- Split between old en new houses need to be researched.f