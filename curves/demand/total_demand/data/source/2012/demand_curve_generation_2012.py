from numpy import *
from pylab import *
import os

# The ENTSO-E 'Load and consumption data' summarizes the hourly load values per month for all countries in a single file. In order to use this data in the ETM,
# this script is used to re-order the data in a single list of 8760 hourly load values for each country.

# define countries, according to the abbreviations used in the ENTSO-E CSVs
countries = ['AT','BA','BE','BG','CH','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IS','IT','LT','LU','LV','ME','MK','NI','NL','NO','PL','PT','RO','RS','SE','SI','SK']
# set path
curpath = os.path.dirname(os.path.abspath(__file__))

##########
# FOR LOOP
##########

for l in range(0,len(countries)):

    output = list()

    # open the 12 CSV files in the input folder and extract data for country 'l'
    for i in range(1,13):
    
        f = open(curpath + '/data/ENTSO-E/' + str(i) +'-2012.csv')

        lines = f.readlines()

        for j in range(10,len(lines)):
    
            lines[j] = lines[j].strip('\r\n')
            temp = lines[j].split(',')
    
            if temp[0] == countries[l]:
            
                for k in range(2, len(temp)):# replace all "n.a. (not applicable entries) with 0
                
                    if temp[k] == 'n.a.':
                        output.append(0)
                    else:
                        output.append(float(temp[k]))
    
        f.close()
        #print len(output)

    # remove false datapoints due to the way that is dealt with daylight saving time. We pop the last positions first, in order to not mess up the order (counting) of datapoints. 
    # note, that we actually replaced all 'n.a." with "0.0" above - only positions will be popped that contain a 'n.a.' in the original data
    # the pattern of popped data points seems a bit random at first sight. ENTSO-E data contains an extra column in October, to report two hours (daylight savgins switch). This extra column only contains a number on Oct-30, on all other days, it is 'n.a.'. 
    # NOTE: the days at which we switch from daylight saving time and back vary per year; the list below needs to be updated each year!
    
    output.pop(7329)# Oct 31 is n.a.
    output.pop(7304)# Oct 30 is n.a.
    output.pop(7279)# Oct 29 is n.a.
                    # Oct 28 contains the extra hour, and is therefore not 'n.a.'
    output.pop(7229)# Oct 27 is n.a.
    output.pop(7204)# Oct 26 is n.a.
    output.pop(7179)# Oct 25 is n.a.
    output.pop(7154)# Oct 24 is n.a.
    output.pop(7129)# Oct 23 is n.a.
    output.pop(7104)# Oct 22 is n.a.
    output.pop(7079)# Oct 21 is n.a.
    output.pop(7054)# Oct 20 is n.a.
    output.pop(7029)# Oct 19 is n.a.
    output.pop(7004)# Oct 18 is n.a.
    output.pop(6979)# Oct 17 is n.a.
    output.pop(6954)# Oct 16 is n.a.
    output.pop(6929)# Oct 15 is n.a.
    output.pop(6904)# Oct 14 is n.a.
    output.pop(6879)# Oct 13 is n.a.
    output.pop(6854)# Oct 12 is n.a.
    output.pop(6829)# Oct 11 is n.a.
    output.pop(6804)# Oct 10 is n.a.
    output.pop(6779)# Oct 9 is n.a.
    output.pop(6754)# Oct 8 is n.a.
    output.pop(6729)# Oct 7 is n.a.
    output.pop(6704)# Oct 6 is n.a.
    output.pop(6679)# Oct 5 is n.a.
    output.pop(6654)# Oct 4 is n.a.
    output.pop(6629)# Oct 3 is n.a.
    output.pop(6604)# Oct 2 is n.a.
    output.pop(6579)# Oct 1 is n.a.
 
    output.pop(2018)# daylight saving switch in March (one hour 'does not exist')
    
    # 2012 was a leap year. Since the ETM cannot deal with this, we removed the 24 data points for 29 February
    
    output.pop(1439)
    output.pop(1438)
    output.pop(1437)
    output.pop(1436)
    output.pop(1435)
    output.pop(1434)
    output.pop(1433)
    output.pop(1432)
    output.pop(1431)
    output.pop(1430)
    output.pop(1429)
    output.pop(1428)
    output.pop(1427)
    output.pop(1426)
    output.pop(1425)
    output.pop(1424)
    output.pop(1423)
    output.pop(1422)
    output.pop(1421)
    output.pop(1420)
    output.pop(1419)
    output.pop(1418)
    output.pop(1417)
    output.pop(1416)

    # Exporting 'country.csv' file
    savetxt(curpath + '/data/demand_curves/' + countries[l] + '_demand_curve.csv', output, fmt="%d", delimiter =',')

    print countries[l] , '  ', len(output)