#!/usr/bin/env python3

import numpy as np
import glob
import math
import os

def readFile(yay):
    new = []
    with open(yay, 'r') as f:
        f = f.readlines()
    
    for l in f:
        l = l.replace('\n', "")
        l = l.split()
        new.append(l)
    return new

def convert(energy):
    energy = (energy*2*(math.pi/180)**2)
    return round(energy, 5)

def average(data):
    sum = 0
    for i in range(len(data)):
        sum = sum + float(data[i][1])
    avg = sum/len(data)
    return round(avg, 2)

def getCoords(data):
    list_dist = []
    list_freq = []
    betterData = np.zeros(len(data))
    for i in range(len(data)):
        betterData[i] = float(data[i][1])
    
    betterData.sort()
    
    for i in range(len(betterData)):
        if i == 0:
            #print('no')
            list_dist.append(betterData[i]) 
            list_freq.append(1)
            continue
    
        for j in range(len(list_dist)):
            if i == 0: print('crap')
            if betterData[i] == list_dist[j]:
                #print('yah')
                list_freq[j] = list_freq[j] + 1    
        else:
            list_dist.append(betterData[i])
            list_freq.append(1)

    distance = np.array(list_dist)
    frequency = np.array(list_freq)

    return distance, frequency

def getMost(data, there):
    high = -999
    idx = -999
    for i in range(len(data)):
        if data[i] > high:
            high = data[i]
            idx = i
    return there[idx]

def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

try:
    os.remove("summary.dat")
except:
    pass

#inp = input('Please input the data force file, including the extension.   ')
inp = 'force_logfile'
if inp == 'h' or inp == 'H' or inp == 'Help' or inp == 'help':
    print('How to use this:')
    print('Put this script in the directory that has all the data you want formatted.')
    print('Run the script from konsole by typing \'python format.py\'.  You will be prompted for an energy input.')
    #print('Input the energy and press enter.')
elif inp == 'HeLp' or inp == 'hElP':
    print('Jokes on you, sarcastic little twit')

try:
    fdata = readFile(inp)
except:
    print('Could not find input file.')

names = []
nums = []
highFreqs = []
energies = []

for i in range(len(fdata)):
    names.append(fdata[i][0])
    try:
        data = readFile(fdata[i][0])
    except:
        print('Could not find file ' + fdata[i][0] + ', skipping and continuing.')
        names.remove(fdata[i][0])
        continue
    try:
        num = average(data)
        energies.append(convert(float(fdata[i][1])))
    except:
        print(fdata[i][0] + ' is empty.')
        os.remove(fdata[i][0])
        names.remove(fdata[i][0])
        names.remove(convert(float(fdata[i][1])))
    nums.append(num)

    #dist, freq = getCoords(data)
    #highFreq = getMost(freq, dist)
    #highFreq = truncate(highFreq,2)
    #highFreqs.append(highFreq)

f = open('summary.dat', 'w+') 
for i in range(len(names)):
    f.write(str(names[i]) + '    ' + str(nums[i]) + '    ' + str(energies[i]))
    f.write('\n')
f.close()

print('done')
