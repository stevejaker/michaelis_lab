#!/usr/bin/env python3

import sys, os
from subprocess import call
from getpass import getuser
import FileReader
# import atomType

def run():
	with open('packmol.sh', 'w') as f:
		f.write('#!/bin/bash\n\n')
		f.write('packmol < packmol.inp')
	call(['bash', 'packmol.sh'])
	os.remove('packmol.sh')

def convertToMol2(molecule):
	call(["obabel", "packmol.pdb", "pdb", "-o", "mol2", "-O", f'{molecule}_solvated.mol2'])
	mol = FileReader.ReadFile(f'{molecule}_solvated.mol2')
	mol.writeMol2File(f'{molecule}_solvated.mol2')
	# atomType.run(molecule, 'mol2')

def solvate(molecule, file_format, residues_added, solvent, box_x, box_y, box_z):
	user = getuser()
	# FILE MUST BE A PDB
	if file_format.lower() != "pdb":
		mol = FileReader.ReadFile(f"{molecule}.{file_format}")
		mol.writePDBFile(f"{molecule}.pdb")
	with open('packmol.inp', 'w') as f:
		f.write(f"""tolerance 1.5

filetype pdb

output packmol.pdb

structure {molecule}.pdb
  number 1 
  fixed 0. 0. 0. 0. 0. 0.
  centerofmass
end structure

structure /home/{user}/zTeamVPScripts/solvents/{solvent}.pdb 
  number {residues_added}
  inside box {round(box_x / -2.0)}. {round(box_y / -2.0)}. {round(box_z / -2.0)}. {round(box_x /  2.0)}. {round(box_y /  2.0)}. {round(box_z /  2.0)}.
  radius 1.5
end structure
""")
	run()
	convertToMol2(molecule)


def multiSubs():
	print(f"""

tolerance 1.5

filetype pdb

output 2_subs.pdb

structure $PEP.pdb
  number 1 
  fixed 0. 0. 0. 0. 0. 0.
  centerofmass
end structure

structure $SUB1.pdb 
  number $sub1
  inside box ${box_neg}. ${box_neg}. ${box_neg}. ${box_pos}. ${box_pos}. ${box_pos}.
  radius 1.5
end structure

structure $SUB2.pdb 
  number $sub2
  inside box ${box_neg}. ${box_neg}. ${box_neg}. ${box_pos}. ${box_pos}. ${box_pos}. 
  radius 1.5
end structure
" > input.inp

packmol < input.inp""")
	print('Not Functional')
	# run()