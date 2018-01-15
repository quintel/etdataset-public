from numpy import *
from pylab import *
import os

# define countries, according to the abbreviations used in the ENTSO-E CSVs
countries = ['AT','BA','BE','BG','CH','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IS','IT','LT','LU','LV','ME','MK','NI','NL','NO','PL','PT','RO','RS','SE','SI','SK']
# set path
curpath = os.path.dirname(os.path.abspath(__file__))

##########
# FOR LOOP
##########

for l in range(0,len(countries)):

    output = list()

    # open the 12 CSV files in the input folder and extract data for coutnry 'l'
    for i in range(1,13):
    
        f = open(curpath + '/input/' + str(i) +'.csv')

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
    
    output.pop(7305)# Oct 31 is n.a.
                    # Oct 30 contains the extra hour, and is therefore not 'n.a.'
    output.pop(7255)# Oct 29 is n.a.
    output.pop(7230)# Oct 28 is n.a.
    output.pop(7205)# Oct 27 is n.a.
    output.pop(7180)# Oct 26 is n.a.
    output.pop(7155)# Oct 25 is n.a.
    output.pop(7130)# Oct 24 is n.a.
    output.pop(7105)# Oct 23 is n.a.
    output.pop(7080)# Oct 22 is n.a.
    output.pop(7055)# Oct 21 is n.a.
    output.pop(7030)# Oct 20 is n.a.
    output.pop(7005)# Oct 19 is n.a.
    output.pop(6980)# Oct 18 is n.a.
    output.pop(6955)# Oct 17 is n.a.
    output.pop(6930)# Oct 16 is n.a.
    output.pop(6905)# Oct 15 is n.a.
    output.pop(6880)# Oct 14 is n.a.
    output.pop(6855)# Oct 13 is n.a.
    output.pop(6830)# Oct 12 is n.a.
    output.pop(6805)# Oct 11 is n.a.
    output.pop(6780)# Oct 10 is n.a.
    output.pop(6755)# Oct 9 is n.a.
    output.pop(6730)# Oct 8 is n.a.
    output.pop(6705)# Oct 7 is n.a.
    output.pop(6680)# Oct 6 is n.a.
    output.pop(6655)# Oct 5 is n.a.
    output.pop(6630)# Oct 4 is n.a.
    output.pop(6605)# Oct 3 is n.a.
    output.pop(6580)# Oct 2 is n.a.
    output.pop(6555)# Oct 1 is n.a.
 
    output.pop(2042)# daylight saving switch in March (one hour 'does not exist')

    # Exporting 'country.csv' file
    savetxt(curpath+ '/output/' + countries[l]+'.csv', output, fmt="%d", delimiter =',')

    print countries[l] , '  ', len(output)