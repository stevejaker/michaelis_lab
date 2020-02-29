#!/usr/bin/env python3

import sys, os
from subprocess import call
from getpass import getuser
import re_type_atoms

def usage():
	pass

def FILETYPE_ERROR():
	print("FILETYPE ERROR: ONLY MOL2 FILES ARE SUPPORTED AT THIS TIME.")


def run(filename, file_type):
	if file_type != 'mol2':
		FILETYPE_ERROR()
	infile = f"{filename}.{file_type}"
	outfile = f"{filename}.pdb"
	call([	'atomtype',
			'-i', infile,
			'-o', outfile,
			'-f', file_type	])
	re_type_atoms.run(outfile, infile)
	try: os.remove("ATOMTYPE.INF")
	except: pass


if __name__ == '__main__':
	if '--help' in sys.argv or '-h' in sys.argv:
		usage()
		sys.exit()
	run()