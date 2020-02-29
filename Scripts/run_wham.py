#!/usr/bin/env python 

import os, sys
from getpass import getuser
import bashcall

user = getuser()
WORKDIR = os.getcwd()
WHAMPATH = f'/zhome/{user}/wham/wham'
INPUT_FILE = 'ums_input'
ARGS = sys.argv[1:]
number_of_datafiles = 0
temperature = 0
min_distance = -9999
max_distance = 9999

def usage():
	print('''
Usage:
	python run_wham.py [options]

Options:
	-h,  --help 			Shows this message
	-n,  --number 			Declares number of datafiles
	-T,  --temperature 		Declares reaction Temperature
	-m,  --min 				Sets Minimum Distance Value
	-M,  --max 				Sets Maximum Distance Value
''')

def checkInputFile():
	global INPUT_FILE
	min_distance = 9999.0
	max_distance = -9999.0
	with open(INPUT_FILE) as f:
		f = f.readlines()
	for i in f:
		i = i.split()
		if float(i[0]) < float(min_distance):
			min_distance = float(i[0])
		if float(i[0]) > float(max_distance):
			max_distance = float(i[0])
	
	return len(f), min_distance, max_distance

# def readProdFile():
# 	with open()

# def autoRun():
# 	number_of_datafiles, min_distance, max_distance = checkInputFile()
# 	temperature = readProdFile()
# 	manualRun(number_of_datafiles, min_distance, max_distance, temperature)


def manualRun(number_of_datafiles, min_distance, max_distance, temperature, GETDATA=False):
	if number_of_datafiles == 0 or min_distance == -9999 or max_distance == 9999 or GETDATA == True:
		number_of_datafiles, min_distance, max_distance = checkInputFile()
	
	wham_input = f'{min_distance} {max_distance} {number_of_datafiles} 0.01 {temperature} 0 summary.dat result.dat'
	print(f'\nThe Wham input is :\n{wham_input}\n')

	bashcall.lstCall([f'{WHAMPATH} {wham_input}',
		"cat result.dat | awk '{print$1,$2}' > pmf.dat",
		"sed -i '/inf/d' pmf.dat",
		'xmgrace pmf.dat',
		'echo "Done"'])


if __name__ == '__main__':
	for i in range(len(ARGS)):
		ARG = ARGS[i]

		if ARG in ['-h', '--help']:
			usage()
			sys.exit()

		elif ARG in ['-n', '--number']:
			number_of_datafiles = ARGS[i + 1]

		elif ARG in ['-T', '--temperature']:
			temperature = ARGS[i + 1]

		elif ARG in ['-m', '--min']:
			min_distance = ARGS[i + 1]

		elif ARG in ['-M', '--max']:
			max_distance = ARGS[i + 1]


	if number_of_datafiles == 0 or temperature == 0:
		# autoRun()
		print('ERROR')
		sys.exit()
	else:
		manualRun(number_of_datafiles, min_distance, max_distance, temperature)