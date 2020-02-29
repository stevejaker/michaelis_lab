#!/usr/bin/env python3

from subprocess import call
import os, sys


def runLeap():
	try: os.remove('leap.log')
	except: pass
	call(['tleap', '-f', 'leap.in'])
	checkForErrors()

def checkForErrors():
	with open('leap.log') as f:
		f = f.readlines()
	for i in f:
		if "Exiting LEaP: Errors = 0" in i:
			print("\nLEaP Finished Running with 0 errors!\n")
		elif "Exiting LEaP: Errors = " in i:
			i = i.split()
			print(f'\nLEaP Finished running with {i[4]} errors.\nAborting program. See leap.log for more details\n')
			sys.exit()
	
if __name__ == '__main__':
	runLeap()
