#!/usr/bin/env python3

import sys, os
from subprocess import call
import solvents, runPackmol, frcmod, FileReader
import leap, runParmed
from shutil import copy, copyfile

def usage():
	print('''
Flags:
	-m,  --molecule 	Declares the name of the input molecule.
				Do not include the file extention. If you 
				do, it will be removed.
				* CAN BE AN ALREADY COMPLEXED MOLECULE,
				  BUT IT IS NOT RECOMMENDED *
	-f,  --format 		Declares file format
	-s,  --solvent 		Declares the name of the solvent.
	     --reset		Deletes old frcmod, log, inpcrd, prmtop files
''')

def removeFiles():
	for i in os.listdir():
		if i.endswith(".log") or i.endswith(".frcmod") or i.endswith(".inpcrd") or i.endswith(".prmtop") or '_solvated' in i:
			print(f'Removed {i}')
			os.remove(i)

def parseLeapOutput():
	with open('leap.log') as f:
		f = f.readlines()
	for i in f:
		if "Total vdw box size:" in i and "angstroms." in i:
			i = i.split()
			box_x = float(i[4])
			box_y = float(i[5])
			box_z = float(i[6])
		elif "Added" in i and "residues." in i:
			i = i.split()
			residues_added = i[1]
	return residues_added, box_x, box_y, box_z

def leapSolvate(molecule, file_format, solvent, box_size=10, closeness=0.8, additional_paths=[]):
	from getpass import getuser
	user = getuser()
	solvent_name, off_file, frcmod_file, res_name = solvents.getSolvents(solvent=solvent)
	off_file = off_file.replace('.off', '')
	prmtop_file = 'start.prmtop' if 'start' in molecule else 'end.prmtop'
	inpcrd_file = 'start.inpcrd' if 'start' in molecule else 'end.inpcrd'
	with open('leap.in', 'w') as f:
		f.write(f"""source leaprc.protein.ff14SB
source leaprc.gaff2
addPath /home/{user}/zTeamVPScripts/solvents/
""")
		for i in additional_paths:
			f.write(additional_paths + '\n')
		f.write(f"""complex = load{file_format} {molecule}.{file_format}
loadamberparams {molecule}.frcmod
loadamberparams {frcmod_file}
loadoff {off_file}.off
solvateBox complex {off_file} {box_size} {closeness}
saveamberparm complex {prmtop_file} {inpcrd_file}
savemol2 complex {molecule}_solvated.mol2 1
quit""")
	# saveamberparm complex start.prmtop start.inpcrd ## FIXME: Not sure this is best practice
	print("Runing Leap...\n")
	# call(['tleap', '-f', 'leap.in'])
	leap.runLeap()
	# os.remove('leap.in')
	print("Leap has finished running.\n")
	return solvent_name, off_file, frcmod_file, res_name 

def trimMolecule(molecule, file_format):
	if molecule.endswith(f".{file_format}"):
		molecule, extention = molecule.split(".")
		return molecule
	else:
		return molecule

def check(molecule, file_format):
	if molecule == "":
		print(f'FATAL ERROR: Missing {file_format} name. ')
		sys.exit()

def run(molecule, file_format, solvent):
	check(molecule, file_format)
	molecule = trimMolecule(molecule, file_format)
	frcmod.makeFrcmod(molecule, file_format)
	solvent_name, off_file, frcmod_file, res_name  = leapSolvate(molecule, file_format, solvent)
	residues_added, box_x, box_y, box_z = parseLeapOutput()
	runPackmol.solvate(molecule, file_format, residues_added, solvent, box_x, box_y, box_z)

def runTwo(molecule1, molecule2, file_format, solvent, initial_residues=1):
	molecule1 = trimMolecule(molecule1, file_format)
	molecule2 = trimMolecule(molecule2, file_format)

	frcmod.makeFrcmod(molecule1, file_format)
	frcmod.makeFrcmod(molecule2, file_format)
	
	solvent, off_file, frcmod_file, res_name  = leapSolvate(molecule1, file_format, solvent)
	residues_added1, box_x1, box_y1, box_z1 = parseLeapOutput()

	# Removes leap.log so it doesn't cause problems parsing the output twice.
	try: os.remove('leap.log')
	except: pass

	solvent, off_file, frcmod_file, res_name  = leapSolvate(molecule2, file_format, solvent)
	residues_added2, box_x2, box_y2, box_z2 = parseLeapOutput()

	print(f"Residues Added 1: {residues_added1}\nResidues Added 2: {residues_added2}")

	if int(residues_added1) > int(residues_added2):
		start_residue = int(initial_residues) + int(residues_added2) + 1 
		end_residue = int(initial_residues) + int(residues_added1) + 1000
		pmd = runParmed.PMD()
		pmd.parm = 'start.prmtop' 
		pmd.coordfile = 'start.inpcrd'
		pmd.outfile = 'start.inpcrd' # overwrite the file
		pmd.setStrip(start_residue, end_residue, 'residue')
		pmd.write()
		pmd.run()
		print(pmd.output)
		# Saves prmtop file of the SMALLER prmtopfile
		copyfile('end.prmtop', 'main.prmtop')
	
	elif int(residues_added1) < int(residues_added2):
		start_residue = int(initial_residues) + int(residues_added1) + 1 
		end_residue = int(initial_residues) + int(residues_added2) + 1000

		pmd = runParmed.PMD()
		pmd.parm = 'end.prmtop' 
		pmd.coordfile = 'end.inpcrd'
		pmd.outfile = 'end.inpcrd' # overwrite the file
		pmd.setStrip(start_residue, end_residue, 'residue')
		pmd.write()
		pmd.run()
		print(pmd.output)
		# Saves prmtop file of the SMALLER prmtopfile
		copyfile('start.prmtop', 'main.prmtop')

	
	# runPackmol.solvate(molecule1, file_format, residues_added, solvent, box_x, box_y, box_z)
	# runPackmol.solvate(molecule2, file_format, residues_added, solvent, box_x, box_y, box_z)

	# mol1 = FileReader.ReadFile(f'{molecule1}_solvated.mol2')
	# mol2 = FileReader.ReadFile(f'{molecule2}_solvated.mol2')

	# for i in mol1.AtomDetails:
	# 	mol2.AtomDetails[i]["atom_type"] = mol1.AtomDetails[i]["atom_type"]
	# 	mol1.AtomDetails[i]["atom_name"] = mol2.AtomDetails[i]["atom_name"]

	# mol1.writeMol2File(f'{molecule1}_solvated.mol2')
	# mol2.writeMol2File(f'{molecule2}_solvated.mol2')
	return solvent, off_file, frcmod_file, res_name 



if __name__ == '__main__':
	ARGS = sys.argv[1:] # Removes the program name from command line args
	molecule = ""
	file_format = "mol2"
	solvent = ""

	for i in range(len(ARGS)):
		arg = ARGS[i]

		if "--reset" in ARGS:
			removeFiles()
			sys.exit()

		if arg in ['-m', '--molecule']:
			molecule = ARGS[i + 1]

		elif arg in ['-f', '--format']:
			file_format = ARGS[i + 1]

		elif arg in ['-s', '--solvent']:
			solvent = ARGS[i + 1]

		elif arg in ['-h', '--help']:
			usage()
			sys.exit()

	solvent_name, off_file, frcmod_file, res_name = run(molecule, file_format, solvent)
	