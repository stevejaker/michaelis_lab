#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import glob


def readFile(yay):
    new = []
    with open(yay, 'r') as f:
        f = f.readlines()
    
    for l in f:
        l = l.replace('\n', "")
        l = l.split()
        new.append(l)
    return new


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

def main():
    for filename in glob.glob('distance*.dat'):
        data = readFile(filename)
        dist, freq = getCoords(data)
        plt.plot(dist, freq)


        plt.xlabel('distance')
        plt.ylabel('frequency')

        plt.show()

        print('done')


if __name__ == '__main__':
    main()
