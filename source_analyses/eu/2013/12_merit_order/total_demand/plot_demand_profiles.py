from pylab import *

import os

# set path
curpath = os.path.dirname(os.path.abspath(__file__))

# This script can be used to plot hourly demand profiles. To do so, run this script, then use the function plot_demand_profiles
# Syntax plot_demand_profiles(['country_1','country_2', ..., 'country_n'])

# Hourly demand profiles are available for the following countries
# 'AT' (Austria)
# 'BA' (Bosnia and Herzegovina)
# 'BE' (Belgium)
# 'BG' (Bulgaria)
# 'CH' (Switzerland)
# 'CY' (Cyprus)
# 'CZ' (Czech)
# 'DE' (Germany)
# 'DK' (Denmark)
# 'EE' (Estonia)
# 'ES' (Spain)
# 'FI' (Finland)
# 'FR' (France)
# 'GB' (Great Britain)
# 'GR' (Greece)
# 'HR' (Croatia)
# 'HU' (Hungary)
# 'IE' (Ireland)
# 'IS' (Iceland)
# 'IT' (Italy)
# 'LT' (Lithuania)
# 'LU' (Luxemburg)
# 'LV' (Latvia)
# 'ME' (Montenegro)
# 'MK' (Macedonia)
# 'NI' (Northern Ireland?)
# 'NL' (Netherlands)
# 'NO' (Norway)
# 'PL' (Poland)
# 'PT' (Portugal)
# 'RO' (Romania)
# 'RS' (Serbia)
# 'SE' (Sweden)
# 'SI' (Slovenia)
# 'SK' (Slovakia)
# 'EU27' (EU-27)
# 'example' (example country for ETM)


# Clean plot window    
plt.close()
plt.figure(figsize=(15, 10), dpi=100)


# function to plot individual countries
def plot_demand_profiles(countries):
    
    for i in range(0, len(countries)):
    
        temp = loadtxt(curpath +'/demand_profiles/' + countries[i] +'_demand_profile.csv')
    
        plot(temp, label=countries[i])
    
    xlabel('hour')
    ylabel('hourly load (MW)')
    
    ylim(0,0.6e-7)
    
    legend()
            
    show()