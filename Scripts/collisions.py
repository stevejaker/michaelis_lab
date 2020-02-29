#!/usr/bin/env python3

import numpy as np
import glob
import math
import os, sys
import error_handler
from shutil import copytree, copy
from getpass import getuser

workdir = os.getcwd()
user = getuser()
ARGS = sys.argv[1:]
FILENAME = 'distance.dat'
LOWER = 3.38
UPPER = 3.42

def usage():
    print('''
Usage:
    collisions.py [options]

Options:
    -h,  --help             Shows this message
    -f,  --file             Declares filename
    -u,  --upper            Declares Upper Limit (Float)
    -l,  --lower            Declares Lower Limit (Float)
''')

def readFile(yay):
    new = []
    with open(yay, 'r') as f:
        f = f.readlines()
    
    for l in f:
        l = l.replace('\n', "")
        l = l.split()
        new.append(l)
    for i in range(8):
        new.pop(0)
    return new

def countcollisions(data, lower, upper):
    numcollisions = 0
    full_data = []
    
    for i in range(len(data)):
        if float(data[i][1]) <= upper and float(data[i][1]) >= lower:
            numcollisions = numcollisions + 1
            full_data.append(data[i])
    return numcollisions, full_data
    
def writeFile(collisions, txt_outfile):
    f = open(txt_outfile, 'w+')
    f.write('There are ' + str(collisions) + ' collisions')
    f.close()
    return ""

def writeFullData(full_data, full_data_outfile):
    with open(full_data_outfile,'w') as f:
        f.write("Frame\t\t\tDistance\n")
        for i in full_data:
            f.write(f"{i[0]}\t\t\t{i[1]}\n")

def run(filename=FILENAME, upper=UPPER, lower=LOWER):
    global workdir
    txt_outfile = filename.replace('.dat', '.txt')
    full_data_outfile = filename.replace('.dat', '_full_data.txt')
    data = readFile(filename)
    numcollisions, full_data = countcollisions(data, lower, upper)
    writeFile(numcollisions, txt_outfile)
    writeFullData(full_data, full_data_outfile)
    try: os.mkdir('collisions')
    except: pass
    copy(f'{workdir}/{filename}', f'{workdir}/collisions/{filename}')
    copy(f'{workdir}/{txt_outfile}', f'{workdir}/collisions/{txt_outfile}')
    copy(f'{workdir}/{full_data_outfile}', f'{workdir}/collisions/{full_data_outfile}')
    print('done')
    return numcollisions


if __name__ == '__main__':
    for i in range(len(ARGS)):
        arg = ARGS[i]
        if arg in ['-h', '--help']:
            usage()
            sys.exit()
        elif arg in ['-f', '--file']:
            FILENAME = ARGS[i + 1]
        elif arg in ['-u', '--upper']:
            try: UPPER = float(ARGS[i + 1])
            except: error_handler.throwError("Type Error", 1, f"{arg}: {ARGS[i + 1]} Not of Type: Float")
        elif arg in ['-l', '--lower']:
            try: LOWER = float(ARGS[i + 1])
            except: error_handler.throwError("Type Error", 1, f"{arg}: {ARGS[i + 1]} Not of Type: Float")
    numcollisions = run(FILENAME, UPPER, LOWER)

