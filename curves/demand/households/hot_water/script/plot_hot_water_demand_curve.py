import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import os
from pylab import *

time_steps = 8760

file_name_1 = "hot water profile 1 households, 7 days.csv"
file_name_2 = "hot water profile 10 households, 7 days.csv"
file_name_3 = "hot water profile 100 households, 7 days.csv"
file_name_4 = "hot water profile 1000 households, 7 days.csv"
# file_name_5 = "hot water profiles 10000 households, 7 days.csv"
# file_name_6 = "hot water profiles 100000 households, 7 days.csv"
file_name_7 = "hot water hot water distribution.csv"

profile_1 = genfromtxt(file_name_1, delimiter=',')
profile_2 = genfromtxt(file_name_2, delimiter=',')
profile_3 = genfromtxt(file_name_3, delimiter=',')
profile_4 = genfromtxt(file_name_4, delimiter=',')
#profile_5 = genfromtxt(file_name_5, delimiter=',')
#profile_6 = genfromtxt(file_name_6, delimiter=',')
profile_7 = genfromtxt(file_name_7, delimiter=',')


plt.close()
plt.figure(figsize=(19, 7))

mini = 0
maxi = 24 * 7

subplot(2,3,1)
plt.plot(profile_1[mini:maxi],linewidth=1.0,)  
title("1 households")
plt.xlabel('time (hours)')
plt.ylabel('probability')
ylim(0,4e-7)

subplot(2,3,2)
plt.plot(profile_2[mini:maxi],linewidth=1.0,)  
title("10 households")
plt.xlabel('time (hours)')
plt.ylabel('probability')
ylim(0,4e-7)

subplot(2,3,3)
plt.plot(profile_3[mini:maxi],linewidth=1.0,)  
title("100 households")
plt.xlabel('time (hours)')
plt.ylabel('probability')
ylim(0,4e-7)

subplot(2,3,4)
plt.plot(profile_4[mini:maxi],linewidth=1.0,)  
title("1000 households")
plt.xlabel('time (hours)')
plt.ylabel('probability')
ylim(0,4e-7)

# subplot(2,3,5)
# plt.plot(profile_2[mini:maxi],linewidth=1.0,)  
# title("10000 households")
# plt.xlabel('time (hours)')
# plt.ylabel('probability')
# ylim(0,4e-7)

subplot(2,3,5)
plt.plot(profile_7[mini:maxi],linewidth=1.0,)  
title("Distribution function")
plt.xlabel('time (hours)')
plt.ylabel('probability')
ylim(0,4e-7)




#plt.legend()
plt.show()