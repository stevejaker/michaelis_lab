#!/usr/bin/env python3

import os, sys
from shutil import copy, copytree, rmtree
from getpass import getuser
from subprocess import call, check_output

WORKDIR = os.getcwd()   # Pulls Current Work Directory
USER = getuser()     # Pulls Username
ARGS = sys.argv[1:]  # Takes input arg vector and removes the program name
#
# INSERT DEFAULT VARIABLES HERE
#

def usage():
	print("""
Usage:
	runAntechamber.py [options]

Options:
	-h,  --help 			Shows this message	
""")

def runAC(infile, outfile, file_type, net_charge, charge_type):
	call(['antechamber',
		'-i', infile,
		'-fi', file_type,
		'-o', outfile,
		'-fo', file_type,
		'-pf', 'y',
		'-nc', net_charge,
		'-c', charge_type
		])

if __name__ == '__main__':
	print("Cannot run this command from the command line... Yet...")
	sys.exit()
	for i in range(len(ARGS)):
		ARG = ARGS[i]
		if ARG in ['-h', '--help']:
			usage()
			sys.exit()
	runAC(infile, outfile, file_type, net_charge, charge_type)

