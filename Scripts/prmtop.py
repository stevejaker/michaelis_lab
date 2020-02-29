#!/usr/bin/env python3

import os, sys
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
	prmtop.py [options]

Options:
	-h,  --help 			Shows this message	
""")

def trimEnd(line, trim_char=" "):
	"""
	Removes undesired characters from the end of a string
	(Default: space)
	"""
	if line == '':
		return line
	elif line[-1] == trim_char:
		return trimEnd(line[:-1])
	else:
		return line

def main(prmtop):
	residue_information = {}
	res_labels = []
	res_atom_numbers = []
	with open(prmtop, 'r') as f:
		file = f.readlines()
	for i in range(len(file)):
		line = file[i].replace('\n', '')
		# print(line)
		if '%FLAG POINTERS' in line:
			num_atoms = file[i + 2].split()[0]
		elif '%FLAG RESIDUE_LABEL' in line:
			# if "%FORMAT(20a4)" not in trimEnd(file[i + 1].replace('\n', '')):
			i += 2
			line = trimEnd(file[i].replace('\n', ''))
			while '%FLAG' not in line:
				idx = 0
				for x in range(20):
					piece = line[idx:idx + 4].strip()
					if piece != "":
						res_labels.append(piece)
					idx += 4	
				i += 1
				line = trimEnd(file[i].replace('\n', ''))
		elif '%FLAG RESIDUE_POINTER' in line:
			# if "%FORMAT(10I8)" not in trimEnd(file[i + 1].replace('\n', '')):
			i += 2
			line = trimEnd(file[i].replace('\n', ''))
			while '%FLAG' not in line:
				idx = 0
				for x in range(10):
					piece = line[idx:idx + 8].strip()
					if piece != "":
						res_atom_numbers.append(piece)
					idx += 8	
				i += 1
				line = trimEnd(file[i].replace('\n', ''))
			res_atom_numbers.append(num_atoms)
	x = 0
	for i, res in enumerate(res_labels):
		if i == len(res_atom_numbers) + 1: break
		# if i >= len(res_labels):
		residue_information[x] = {
			"name": res,
			"starting_atom": res_atom_numbers[i],
			"ending_atom": res_atom_numbers[i + 1]
		}
		# else:
		# 	residue_information[x] = {
		# 		"name": res,
		# 		"starting_atom": res_atom_numbers[i],
		# 		"ending_atom": num_atoms
		# 	}
		x += 1
	return residue_information, res_labels, res_atom_numbers



if __name__ == '__main__':
	for i in range(len(ARGS)):
		ARG = ARGS[i]
		if ARG in ['-h', '--help']:
			usage()
			sys.exit()

		elif ARG in ['-p', '--prmtop']:
			prmtop = ARGS[i + 1]
		
	residue_information, res_labels, res_atom_numbers = main(prmtop)

