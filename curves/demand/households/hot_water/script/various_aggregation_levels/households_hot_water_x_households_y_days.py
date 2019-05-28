# -*- coding: utf-8 -*-
"""
Created on Apr 29 2015
Modified on Jul 29 2016  
Modified on May 013 2019

@author: joris.berkhout@quintel.com, chael.kruip@quintel.com, dorine.vandervlies@quintel.com
"""

#==============================================================================
# This script is used to generate typical time profiles for domestic hot water
# (DHW) demand. These profiles are generated for a period of one year and time
# resolution of 15 minutes. The script is based in great part on the study 
# `Realistic Domestic Hot-Water Profiles in Different Time Scales` by Jordan
# (2001). Within this study the DHW demand is divided in four categories or
# types of events:
#
# type A: short load (washing hands, washing food)
# type B: medium load (doing the dishes, hot water for cleaning)
# type C: bath
# type D: shower
#
# Jordan (2001) defines probability curves for each type of events: these
# curves specify the probability of such an event to occur at every 15 minute
# time step. Combined with a typical volume per type of event and a typical
# number of occurences per day, these probability curves are used to generate
# random DHW demand profiles. We have refined the method described in the study
# in three ways:
#
# 1. we have adapted the volumes and occurences to the Dutch situation as derived
#    from other sources
#    
#    | type | volume per event | daily occurence per person |
#    | ---- | ---------------- | -------------------------- |
#    | A    | 1                | 5                          |
#    | B    | 9                | 1                          |
#    | C    | 120              | 0.143 *                    |
#    | D    | 50               | 1                          |
#
#    * once a week provided that the household has a bath, which we assume is true
#      for 1 in every 7 households
# 2. we have added the option to include events of type C (bath) in the DHW
#    demand profile or not; these events represent relatively high hot water
#    demands resulting in 'spiky' profiles which are not representative for most
#    households as only 1 in 7 owns a bath 
# 3. we have made it possible to adapt the profiles to represent households
#    with different numbers of people in it; some events happen more often when
#    this number of people increases (e.g. showers), other events increase in volume
#    (e.g. doing the dishes).
# 
# In addition we make the following two assumptions:
# 
# 1. we assume that all events occur entirely within a single timestep.
# 2. we assume that all types of events require water at the same temperature;
#    this means that the DHW demand in kWh is proportional to the DWH in liters.
#    The script returns a normalized DWH demand profile that is scaled when used
#    in ETMoses or ETModel. 
#
# The script returns randomly generated, normalized DHW demand profiles named
# 'DHW_demand_profile_<n>p_<b>_<i>.csv'
# where <n> is the number of persons in the household, <b> is bath or no_bath
# and <i> is the number of the profile. In order to make sure that the same
# profile can be recreated, <i> is also used as a random seed while
# generating the profile.
# The script also returns a aggregated profile which takes into account the
# average number of people per household and the fact that only 1 in around 7
# households has a bath.
#==============================================================================

import numpy as np
import pylab as plt
from numpy import zeros

plt.close()

# Input
number_of_days = 7
number_of_households = 1000

first_of_jan = 1 #  2013: Tuesday (2) 2014: Wednesday (3) 2015: Thursday (4), 2016: Friday (5), 2017: Sunday (7), 2018: Monday (1)

# Global variables

# year, days, hours, quarters
days_per_year = 365
hours_per_day = 24
quarters_per_hour = 4
quarters_per_year = days_per_year * hours_per_day * quarters_per_hour
quarters_per_day = quarters_per_hour * hours_per_day

length_simulation = (number_of_days * hours_per_day * quarters_per_hour)


# volumes per type of event
volume_A_person = 1
volume_B_person = 9
volume_C_person = 120
volume_D_person = 50

# daily occurence per type of event
occ_A_person = 10
occ_B_person = 1
occ_C_person = 0.143
occ_D_person = 1

# number of households with x persons in 2015 (https://statline.cbs.nl/Statweb/publication/?DM=SLNL&PA=37975&D1=21,23-26&D2=0&D3=20-23&HDR=T&STB=G1,G2&VW=T)
person_1 = 2867797.0
person_2 = 2512123.0
person_3 = 923286.0
person_4 = 961010.0
person_5 = 400982.0
total_households = person_1 + person_2 + person_3 + person_4 + person_5

prob_1_person = person_1 / total_households
prob_2_person = person_2 / total_households
prob_3_person = person_3 / total_households
prob_4_person = person_4 / total_households
prob_5_person = person_5 / total_households

# All profiles are generated with a time resolution of 15 minutes

quarters = np.arange(0,length_simulation,1)

# The code below is used to reconstruct the probability functions for each type of event;
# this is our best effort to reproduce the curves used in Jordan (2001)

def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

# The probability per year follows a cosine function with an amplitude of 10%.
# This probability function is the same for a types of events

top_of_sine_days = 45.
prob_year_ABCD = 0.5 + 0.05 * np.cos((quarters/quarters_per_year + (top_of_sine_days/days_per_year*quarters_per_day))*2*np.pi) 

# All types of events have an increasing probability of happening in the weekend
# Type C (bath) follows its own probability
# Numbers from figure 1.5 in Jordan
# Using two subsequent weeks to easily pick one week sequence that fits with 1st of January

prob_week_ABD_jordan = np.array([0.95, 0.95, 0.95, 0.95, 0.98, 1.09, 1.13, 0.95, 0.95, 0.95, 0.95, 0.98, 1.09, 1.13])
prob_week_C_jordan = np.array([0.50, 0.50, 0.50, 0.50, 0.80, 1.90, 2.30, 0.50, 0.50, 0.50, 0.50, 0.80, 1.90, 2.30])

prob_week_ABD = np.zeros(7)
prob_week_C = np.zeros(7)

# Determine sequence of days in the year from 1st of January
for i in range(0,7):
    prob_week_ABD[i] = prob_week_ABD_jordan[(first_of_jan -1 + i)]
    prob_week_C[i] = prob_week_C_jordan[(first_of_jan - 1 + i)]

# Each type of event follows its own probablity function during the week. I have
# recreated the probability functions shown in Figure 1.6 of Jordan (2001) below.

# Type A and B
prob_day_AB = np.zeros(96)

for i in range(5*4, 23*4):
    prob_day_AB[i] = 1/18.

# Type C
prob_day_C = np.zeros(96)

for j in range(7*4, 23*4):
    
    prob_day_C[j] = gauss_function(j, 0.06, 15*4., 20.)
    
for k in range(17*4, 21*4):
    
    prob_day_C[j] = gauss_function(k, 0.22, 19*4., 5)

# Type D
prob_day_D = np.zeros(96)

for k in range(5*4, 9*4):

    prob_day_D[k] = gauss_function(k, 0.25, 7*4., 4.)
    
for k in range(9*4, 18*4):
    
    prob_day_D[k] = 0.02
    
for k in range(18*4, 21*4):
    
    prob_day_D[k] = gauss_function(k, 0.085, 19.5*4., 4.)
    
for k in range(21*4, 23*4):
    
    prob_day_D[k] = 0.02


# The probability for an event to happen is prob_year * prob_week * prob_day
# The following function can be used to construct the probability function for 
# an entire year with time steps of 15 minutes

def annual_probability_curve(prob_day, prob_week, prob_year):
    
    annual_probability = np.zeros(length_simulation)   
    
    for i in range(0,length_simulation):
                
        day_of_week = ( i / 96 ) % 7
        hour_of_day = i % 96
        
        annual_probability[i] = prob_year[i] * prob_week[day_of_week] * prob_day[hour_of_day]
        
    # return the normalized probability function
    return annual_probability / sum(annual_probability)     
            
# Create the probabilities
prob_year_A = annual_probability_curve(prob_day_AB, prob_week_ABD, prob_year_ABCD)
prob_year_B = annual_probability_curve(prob_day_AB, prob_week_ABD, prob_year_ABCD)
prob_year_C = annual_probability_curve(prob_day_C, prob_week_C, prob_year_ABCD)
prob_year_D = annual_probability_curve(prob_day_D, prob_week_ABD, prob_year_ABCD)
 
# Create individual DHW demand profile
def individual_DHW_profile(n, b, i):

    # Scale 
    occ_A_household = occ_A_person * n
    occ_B_household = occ_B_person
    occ_C_household = occ_C_person * n
    occ_D_household = occ_D_person * n
    volume_A_household = volume_A_person
    volume_B_household = volume_B_person * n
    volume_C_household = volume_C_person
    volume_D_household = volume_D_person

    # Create empty patterns
    pattern_A = np.zeros(len(prob_year_A))
    pattern_B = np.zeros(len(prob_year_B))
    pattern_C = np.zeros(len(prob_year_C))
    pattern_D = np.zeros(len(prob_year_D))

 #   np.random.seed(i)

    for j in range(0, length_simulation):
        # construct the random pattern for each type of event by taking onto account
        # their probability, the number of events per day and the volume per event    
        pattern_A[j] = volume_A_household * np.random.choice((0,1),p=[1-prob_year_A[j]*occ_A_household*number_of_days, prob_year_A[j]*occ_A_household*number_of_days])
        pattern_B[j] = volume_B_household * np.random.choice((0,1),p=[1-prob_year_B[j]*occ_B_household*number_of_days, prob_year_B[j]*occ_B_household*number_of_days])
        pattern_C[j] = volume_C_household * np.random.choice((0,1),p=[1-prob_year_C[j]*occ_C_household*number_of_days, prob_year_C[j]*occ_C_household*number_of_days])
        pattern_D[j] = volume_D_household * np.random.choice((0,1),p=[1-prob_year_D[j]*occ_D_household*number_of_days, prob_year_D[j]*occ_D_household*number_of_days])

    pattern = pattern_A + pattern_B + b * pattern_C + pattern_D

    return pattern / sum(pattern)

#new_profile = zeros([35040,1])
summed_profile = np.zeros(len(prob_year_A))

for i in range(0, number_of_households):
    n = int(np.random.choice([1,2,3,4,5], 1, p=[prob_1_person, prob_2_person, prob_3_person, prob_4_person, prob_5_person]))
    b = int(np.random.choice([0,1], 1, p=[0.6, 0.4]))
    x = 3
    # n = 3
    # b = 0
    #print("n = " + str(n) + " b = " + str(b))
    new_profile = individual_DHW_profile(n, b, x)

    for j in range(0, len(new_profile)):
    	summed_profile[j] = new_profile[j] + summed_profile[j]


summed_profile = summed_profile
hourly_profile = summed_profile.reshape(-1, 4).sum(axis=1)
hourly_profile = hourly_profile / sum(hourly_profile) / 3600. / days_per_year * number_of_days
print(sum(hourly_profile))

np.savetxt("hot water profile " + str(number_of_households) + " households, " + str(number_of_days) + " days.csv", hourly_profile, fmt='%.3e', delimiter=',')
#np.savetxt("new_profile.csv", new_profile, fmt='%.3e', delimiter=',')
plt.figure(1)
#plt.xlim(0, 96)
#plt.ylim(0, max(max(prob_day_AB / sum(prob_day_AB)), max(prob_day_C) / sum(prob_day_C), max(prob_day_D) / sum(prob_day_D)) * 1.1)

plt.title("probability throughout the day " + str(number_of_households) + " households")
plt.xlabel("time (hours)")
plt.ylabel("probability")

plt.plot(hourly_profile)  
plt.show()


print("done!")