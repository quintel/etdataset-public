# created by Joris Berkhout

from pylab import *
from scipy.optimize import curve_fit
import os
# set path
curpath = os.path.dirname(os.path.abspath(__file__))

# Year range for which data is available (Eurostat or IEA)
years = arange(2000,2012,1)

# Year range for extrapolating data
years_ex = arange(2000,2051,1)

# The following data are taken from "timecurves_source_analysis.xlsx"
coal = array([4379922.21,
4348011.56,
4305882.10,
4267248.00,
4120956.57,
4006596.36,
3919664.50,
3800821.99,
3635778.94,
3399512.63,
3350721.40,
3151629.00])/1e6

lignite = array([4536680.28,
4503627.54,
4459990.25,
4419973.44,
4268446.22,
4149993.03,
4059949.87,
3936853.97,
3765904.00,
3521181.69,
3470644.22,
3858091.00])/1e6

gas = array([8702344.54,
8729727.52,
8551528.80,
8366002.83,
8510370.59,
7899905.99,
7512022.31,
7001585.14,
7038640.09,
6408161.63,
6539675.30,
5867098.00])/1e6

oil = array([7233754.29,
6748983.43,
6939282.58,
6516311.84,
6056286.15,
5557321.36,
5084483.45,
5018580.07,
4689314.39,
4401667.49,
4076337.59,
3524038.00])/1e6

uranium = array([10209622.67,
10579083.55,
10700129.72,
10761301.79,
10898174.82,
10782194.92,
10697743.13,
10107836.70,
10128729.83,
9662214.29,
9904892.81,
9899121.00])/1e6

bio = array([2476108.06,
2516470.74,
2590748.12,
2834933.96,
3045121.36,
3232112.78,
3482579.12,
3822354.17,
4020148.05,
4213419.97,
4722307.95,
4674794.00])/1e6

total = array([37538432.05,
37425904.34,
37547561.57,
37165771.86,
36899355.71,
35628124.44,
34756442.38,
33688032.04,
33278515.30,
31606157.69,
32064579.27,
30974771.00])/1e6

# Define a list of carriers
carriers = [coal, lignite, gas, oil, uranium, bio, total]

# Define a linear function for fitting purposes
def func(x, a, b):
    return a + b * x

# Plot
close()

# Create an output array for writing out the extrapolated data
output_array = np.zeros((len(years_ex),7))
output_array[:,0] = years_ex/1e6

colors = ['bD', 'gD', 'rD', 'cD', 'mD', 'yD', 'kD']
colors2 = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-']
labels = ['coal', 'lignite', 'natural gas', 'crude oil', 'uranium oxide', 'bio-residues', 'total']

for i in range(0,6):
    
    popt, pcov = curve_fit(func, years, carriers[i])
    y_fit = func(years_ex, popt[0], popt[1])

    plot(years, carriers[i], colors[i])
    plot(years_ex, y_fit, colors2[i], label=labels[i])
    
    output_array[:,i+1] = y_fit
    
# Plot Energy report data points; these points are not used in the fit, but only plotted for reference
years2 = [2005,2020]

coal2 = array([4072256.67, 2699412.56])/1e6
lignite2 = array([4218003.33, 2796024.94])/1e6
gas2 = array([7854640.00, 5495437.50])/1e6
oil2 = array([5556740.00, 2145837.50])/1e6
uranium2 = array([10727460.00, 9535892.50])/1e6
bio2 = array([3211310.00, 5954856.08])/1e6
total2 = array([35640410.00, 28627461.08])/1e6

plot(years2, coal2, 'bo')
plot(years2, lignite2, 'go')
plot(years2, gas2, 'ro')
plot(years2, oil2, 'co')
plot(years2, uranium2, 'mo')
plot(years2, bio2, 'yo')
#plot(years2, total2, 'ko')
    
# Replace negative numbers by 0
output_array = output_array.clip(0)  
    
# Write out the resulting array
with open(curpath+ '/extrapolation_production_trends_from_python_script.csv', 'wb') as f:
  f.write('year,coal,lignite,natural gas,crude oil,uranium oxide,bio-residues\n')
  np.savetxt(f, output_array*1e6, fmt="%f", delimiter =',')    

title("Primary energy production per carrier for EU-27")

xlabel("year")
ylabel("Primary energy production (EJ)")

xlim(1995, 2055)
ylim(0,12)

legend()

show()