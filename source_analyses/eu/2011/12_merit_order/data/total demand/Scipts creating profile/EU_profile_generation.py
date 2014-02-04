from numpy import *
from pylab import *
import os

# set path
curpath = os.path.dirname(os.path.abspath(__file__))

# Clean plot window    
plt.close()
plt.figure(figsize=(15, 10), dpi=100)

# Define list of countires in the ento-e database
all_countries = ['AT','BA','BE','BG','CH','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IS','IT','LT','LU','LV','ME','MK','NI','NL','NO','PL','PT','RO','RS','SE','SI','SK']
# list of EU26 countries, Malta is missing. 
EU_countries = ['AT','BE','BG','CY','CZ','DE','EE','ES','FI','FR','DE','GB','GR','HR','IE','IT','LT','LU','LV','NL','PL','PT','RO','SE','SK','SI']


# Add all EU demand curves
output = zeros((8760))

for i in range(0, len(EU_countries)):
    
    temp = loadtxt(curpath+'/output/' + EU_countries[i] +'.csv')
    
    output += temp


# plot the average demand curve
xlabel('hour')
ylabel('hourly electricity demand (MW)')
plot(output)
show()

# Scale the average demand curve
scaled_profile = output / (sum(output) * 3600)  #the sum of a merit order profile has to equal 1/3600

# Export EU profile
savetxt(curpath+'/EU27_demand_profile.csv', scaled_profile)



##################
# Extra functions 

# compare EU and NL demand profiles 
def plot_NL_vs_EU():
    plt.close()
    plt.figure(figsize=(15, 10), dpi=100)
    NL_2011_profile = loadtxt(os.getcwd() + '/Projects/merit/load_profiles/total_demand.csv')
    plot(scaled_profile)
    plot(NL_2011_profile)
    show()

# function to plot individual countries
def plot_country(country):
    
    temp = loadtxt(curpath+'/output/' + country +'.csv')
    
    xlabel('hour')
    ylabel('hourly load (MW)')
    
    plot(temp)
    
    show()
    
def export_country_profile(country):
    
    temp = loadtxt(curpath+'/output/' + country +'.csv')
    
    # Scale the average demand curve
    scaled_profile = output / (sum(output) * 3600)  #the sum of a merit order profile has to equal 1/3600
    
    savetxt(curpath+'/'+ country+ '_demand_profile.csv', scaled_profile)
    
def export_example_profile():
    
    temp = loadtxt(curpath+'/output/GB.csv')
    temp += loadtxt(curpath+'/output/DE.csv')
    
    # Scale the average demand curve
    scaled_profile = output / (sum(output) * 3600)  #the sum of a merit order profile has to equal 1/3600
    
    savetxt(curpath+'/example_demand_profile.csv', scaled_profile)