#3. Primary Production Analysis (all countries)

This document describes how the initial values for all regasification related shares were found. 

##Regasification data

The GIE (Gas Infrastructure Europe) is an organisation that collects and publishes data about every European country's LNG inventory and send-out (of regasified LNG) on a daily basis. Note: these numbers are only for countries which have LNG import terminals, and they are a country's totals (so not the values of individual terminals). For every year, the daily send-out was summed over to find the total NG send-out (as a result of regasification). This was then multiplied with the density of natural gas (from natural_gas.carrier) and its specific energy to give the total energy of the regasified of LNG. 

No bio LNG regasification data was found; not only is regasification a less viable route for bio lng than using it in transport directly, but also is bio lng production happening on a small scale as of now. Therefore, it is assumed to be zero.

##Shares

Then the total energy of the regasified lng is divided by the primary_energy_supply (of natural gas) to give the initial ratio of NG/regasified LNG in the national gas grid. A similar procedure is used for bio lng, more information on which can be found in the network_gas_analysis sheet.