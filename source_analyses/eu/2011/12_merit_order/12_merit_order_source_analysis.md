## Merit order profile source analysis

### Contents of "12_merit_order"

##### Data

The data folder contains raw data that was downloaded for the purpose of creating EU profiles. Each of these Excel files contains the original data. Sometimes, it is necessary to manipulate this data, for one of the following reasons: 

- data was missing
- different sources treat daylight savings time changes differently
- data was provided with 15 or 30 min intervals (instead of 60 min)

Data was found for 

- wind
  - 2 German, and a Austrian power curve
- solar
  - 2 German, and a Spanish power curve
- total demand
  - ENTSO-E provides a complete set of demand curves for 26 EU countries

The remaining profiles could not be created for the EU, because of a lack of data. Instead, we use the NL profiles in the EU merit order calculation. 

##### wind_solar_hydro analysis.xlsx

This Excel file generates profiles, which have to be saved (exported) as csv files (windows formatted) and stored in the profile folder. 

##### Profiles

This folder contains 9 profiles, fit for the ETM merit order calculation. These profiles have been copied directly to the merit order repository. 
There also is a readme, summarising how the profiles are created. 

### Documentation

Merit order profiles are used by the ETM when the Merit order module is turned on ("has_merit_order = true" in eu.ad). Please also refer our [documentation](http://github.com/quintel/documentation/blob/master/general/merit_order.md) for further documentation. Here, we briefly outline what merit order profiles are used for and how to create them.

Merit order profiles are used by ETEngine in order to calculate the supply and demand of electricity on an hourly resolution. For every hour of the year, the hourly demand of electricity is matched with a certain amount of volatile electricity (wind/solar), must-run technology (CHPs) and dispatchable power plants (coal, gas plants etc.). 
The merit order module needs to 'know' how much electricity can be produced in a certain hour and how large the demand is. This is accomplished with the help of merit order profiles. A profile represents the generation characteristics of electricity producers (wind (inland, coastal, offshore), solar, hydro river, CHPs in agriculture, industry and residences/services). Depending on how many units of a power producer are installed, the corresponding merit order profile is scaled up, so that it reflects the production of that technology. Similarly, the demand profile is scaled according to the electricity demand in a given ETM scenario. 

ETEngine knows the total annual electricity production of certain converters (MJ). By multiplying total energy production (MJ) with a scaled profile (1/s), an hourly load curve in MW can be derived: 

```
L(i) = profile(i) * P
```
with: 
; L: Load or demand in MW
; i: hour
; P: total production in MJ


#### How to create profiles

##### Common pitfalls

1. A merit order profile needs to consist of exactly 8760 hours. The ETM does not consider gap years with 366 days (in such a case, the ETM neglects the last day of a gap year). 
* When compiling merit order profiles, make sure that they reflect the weekend/weekday pattern of the given year. Certain profiles are sensitive to weekend/weekdays, e.g. residential heat demand is higher on the weekend. A countries electricity demand is generally lower on the weekend. Therefore, it might not be possible to simply copy a profile from a different year and recycle it. Always look up the day that a year started on, e.g. a Monday. Then make sure that all profiles are 'synced' and start on a 'Monday'. 
* Also, be aware that profiles tend to be sensitive to the weather conditions, especially temperatures. Cold winters cause a higher electricity demand and a higher demand for space heating (CHP). Electricity demand may react to a high air conditioning demand in summer (depends on your country). Agricultural CHPs have a lower heat demand when outside temperatures rise. Keep in mind that these conditions also change from year to year (beware when recycling old profiles!). 
* The change from daylight savings (winter/summer time) may also cause trouble: You might think: one hour is not significant, as merit order considers 8760 hours. However, 'overlooking' an hour in March will cause the entire summer to be shifted by one hour, meaning that changes in demand/production will be offset by one hour for about half the year. This is especially relevant for the demand profile and solar PV. 
* When creating a profile, do not average too many or too little power curves. When you average the power output of too many measurement sites, you will likely end up with a very flat profile, which may not represent the nature of the particular technology (especially wind/solar). When you average too little or very similar power curves, your profile may become extremely peaky. Perform some sanity checks: For example: Is it likely that all wind turbines though out the country are 'on' at the same time? 
 
##### Research Data
A profile should be based on actual measurement data. For volatile participants, this is usually the energy carrier that is exploited by the converter, e.g. wind speeds, light intensities, water flow. 
If possible, data from different locations (but the same year) should be combined. The wind profiles that we use in the ETM are based on about 4 measurement curves. Combining more curves leads to more smooth and less peaked profiles. A smoother profile will also be characterised by more full load hours. 

##### Convert primary energy to electric output
For each data curve, calculate the electricity output of a converter. This is done by applying conversion laws and efficiencies  (including for example, cut-in, cut-out speeds in case of wind, or peak-power in case of solar cells). 
Let's assume that you have four hourly measurement curves, e.g. wind speeds or solar irradiation measurements). After the conversion to from wind speed to turbine power output, you should have four hourly power curves. 

##### Average power output
Now, the electricity output can be averaged. (We average over distributed power generation output, not over distributed wind speeds). 

##### Normalisation
All merit order profiles need to me normalised: As ETEngine will scale the profiles according to the installed capacity and availability of the respective technology, the profile itself needs to be normalised to 1/3600 (this figure is used to enable an easy transition between Joule and Wh). 
Normalisation ensures that the participant will produce the correct amount of MWh/year in merit order. Double-check that the final profile actually fulfils the constraint `SUM(profile) * 3600 = 1`

##### Save as Windows-CSV
If the profile should be readable for the et-engine, it has to be saved in a CSV file that has windows-style newline commands. In Excel, you need to save the profile as "Windows Comma Separated (.csv)". 

##### A profile should not cause a conflict in installed capacities 

Profiles are used to convert an annual energy production to an hourly load in the merit order calculation: 

```
L(i) = profile(i) * P             < 1 >
```
with: 
; L: Load or demand in MW
; i: hour
; P: total production in MJ

It should never happen that merit order calculates an hourly electricity production capacity that exceeds the installed capacity. In other words: If wind turbines with a nameplate capacity of 3 GW are installed, it should not happen that  merit order will run them at 5 GW in certain hours of the year. In technical terms, this means: 

The load curve L(i) [MW] can never exceed the installed capacity (spec. capacity * number of units):

	L(i) =< spec_capacity * #_units             < 2 >

Combining the two equations, yields:

	profile(i) * P =< spec_capacity * #_units             < 3 >

In the merit order module, total annual production is defined as 

	P [MJ] = spec_capacity [MW] * #_units * availability [%] * full_load_hours [h] * 3600 s/h             < 4 >

Substituting P in < 3 >: 

	profile(i) * full load hours * availability * 3600 <= 1

If `MAX(profile(i) ) * full load hours * availability * 3600 exceeds 1, merit order will calculate with exaggerated capacities for certain hours of the year. 

Please test if your profiles fulfil the above constraint. It may also be interesting to see for how many hours of the year `profile(i) * full load hours * availability * 3600 = 1` is fulfilled. This is equivalent to the number of hours that a technology is running at full capacity. Is that number realistic? How often does it happen that *all* wind turbines are running at nameplate capacity throughout the country?