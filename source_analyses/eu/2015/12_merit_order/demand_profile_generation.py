from numpy import *
from pylab import *
import os

# set path
curpath = os.path.dirname(os.path.abspath(__file__))

# Define list of countires in the ento-e database
all_countries = ['AT','BA','BE','BG','CH','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IS','IT','LT','LU','LV','ME','MK','NI','NL','NO','PL','PT','RO','RS','SE','SI','SK']
# list of EU26 countries, Malta is missing. 
EU_countries = ['AT','BE','BG','CY','CZ','DE','EE','ES','FI','FR','DE','GB','GR','HR','IE','IT','LT','LU','LV','NL','PL','PT','RO','SE','SK','SI']


# Export the scaled profile for all countries

for i in range(0, len(all_countries)):

    output = loadtxt(curpath+'/data/demand_curves/' + all_countries[i] +'_demand_curve.csv')
    
    # Scale the average demand curve
    scaled_profile = output / (sum(output) * 3600)  #the sum of a merit order profile has to equal 1/3600
    
    savetxt(curpath+'/demand_profiles/'+ all_countries[i] + '_demand_profile.csv', scaled_profile)


# Add all EU demand curves and export the scaled profile
output = zeros((8760))

for i in range(0, len(EU_countries)):
    
    temp = loadtxt(curpath+'/data/demand_curves/' + EU_countries[i] +'_demand_curve.csv')
    
    output += temp

# Scale the average demand curve
scaled_profile = output / (sum(output) * 3600)  #the sum of a merit order profile has to equal 1/3600

# Export EU profile
savetxt(curpath+'/demand_profiles/EU27_demand_profile.csv', scaled_profile)



# Export the example demand profile
    
temp = loadtxt(curpath+'/data/demand_curves/GB_demand_curve.csv')
temp += loadtxt(curpath+'/data/demand_curves/DE_demand_curve.csv')
    
# Scale the average demand curve
scaled_profile = output / (sum(output) * 3600)  #the sum of a merit order profile has to equal 1/3600
    
savetxt(curpath+'/demand_profiles/example_demand_profile.csv', scaled_profile)