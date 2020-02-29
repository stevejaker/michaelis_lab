#!/usr/bin/env python3

import os, sys
from shutil import copy, copytree, rmtree
from getpass import getuser
from subprocess import call, check_output

WORKDIR = os.getcwd()   # Pulls Current Work Directory
USER = getuser()     	# Pulls Username
ARGS = sys.argv[1:]  	# Takes input arg vector and removes the program name


def usage():
	print("""
Usage:
	runParmed.py [options]

Options:
	-h,  --help 			Shows this message	
	-p,  --parm
	-c,  --coordfile
	-ss, --strip_start
	-se, --strip_end'
	-st, --strip_type
""")

class PMD():
	def __init__(self):
		# Initialize some crap
		self.parm = None
		self.coordfile = None
		self.strip_mask = None
		self.outfile = None
		self.output = None
		self.file_written = False
		self.parmed_input = "parm.in"

	def run(self):
		# If the file does not exist, write it
		if self.parmed_input not in os.listdir() and self.file_written != True:
			self.write()
		o = check_output(["parmed",
			"--overwrite", 			# sets to overwrite
			"--no-splash", 			# Turns off the stupid image displayed
			"--input", "parm.in"	# Sets the Input File
			])
		self.output = o.decode('utf-8')

	def write(self):
		with open(self.parmed_input, 'w') as f:
			if self.parm is not None:
				f.write(f"parm {self.parm}\n")
			if self.coordfile is not None:
				f.write(f"loadCoordinates {self.coordfile}\n")
			if self.strip_mask is not None:
				f.write(f"strip {self.strip_mask}\n")
			if self.outfile is not None:
				f.write(f"writeCoordinates {self.outfile}\n")
			self.file_written = True

	def setStrip(self, start=1, end=1, striptype='atom'):
		if striptype.lower() in ['atm', 'atom']:
			self.strip_mask = f'@{start}-{end}' if end > start else f'@{start}'
		elif striptype.lower() in ['residue', 'res']:
			self.strip_mask = f':{start}-{end}' if end > start else f':{start}'
		# elif striptype.lower() in ['']:
		# 	self.strip_type = '@'



if __name__ == '__main__':
	pmd = PMD()
	for i in range(len(ARGS)):
		ARG = ARGS[i]
		if ARG in ['-h', '--help']:
			usage()
			sys.exit()
		elif ARG in ['-p', '--parm']:
			self.parm = ARGS[i + 1]
		elif ARG in ['-c', '--coordfile']:
			self.coordfile = ARGS[i + 1]
		elif ARG in ['-ss', '--strip_start']:
			start = ARGS[i + 1]
		elif ARG in ['-se', '--strip_end']:
			end = ARGS[i + 1]
		elif ARG in ['-st', '--strip_type']:
			striptype = ARGS[i + 1]
	
	pmd.setStrip()
	pmd.run()
