#!/usr/bin/env python3

import sys, os
try: import FileReader
except:
	print("\nCANNOT IMPORT FileReader.py. MAKE SURE IT IS INSTALLED AND IN YOUR PYTHONPATH\n")
	sys.exit()

def usage():
	print("""
I'm too lazy to make a usage menu right now.
""")

def getAtoms(filename):
	try:
	 	with open(filename) as f:
	 		atom1 = f.readline().strip()
	 		atom2 = f.readline().strip()
	 		atom3 = f.readline().strip()
	 	return atom1.replace('\n',''), atom2.replace('\n',''), atom2.replace('\n','')
	except: 
		print(f'Could not open {filename}')
		sys.exit()
 	

def getAtomIndex(complex_file, atom1, atom2, substrates):
	catalyst_contact_list= []
	substrate1_contact_list = []
	substrate2_contact_list = []
	for i in complex_file.AtomDetails:
		if complex_file.AtomDetails[i]['atom_name'] == atom1 and complex_file.AtomDetails[i]['residue_num'] == 1:
			atom_number = str(complex_file.AtomDetails[i]['atom_number'])
			if atom_number not in catalyst_contact_list:
				catalyst_contact_list.append(atom_number)
		elif complex_file.AtomDetails[i]['atom_name'] == atom2 and complex_file.AtomDetails[i]['residue_num'] != 1 and complex_file.AtomDetails[i]['residue_num'] <= substrates + 1:
			atom_number = str(complex_file.AtomDetails[i]['atom_number'])
			if atom_number not in substrate1_contact_list:
				substrate1_contact_list.append(atom_number)
		elif complex_file.AtomDetails[i]['atom_name'] == atom2 and complex_file.AtomDetails[i]['residue_num'] != 1 and complex_file.AtomDetails[i]['residue_num'] > substrates:
			atom_number = str(complex_file.AtomDetails[i]['atom_number'])
			if atom_number not in substrate2_contact_list:
				substrate2_contact_list.append(atom_number)
	return catalyst_contact_list, substrate1_contact_list, substrate2_contact_list

def getContactAtom(atom1, element1, atom2, element2, atom3, element3):
	return f"{element1}{atom1}", f"{element2}{atom2}", f"{element3}{atom3}"

def run(substrates, carbon_locations_file="carbon_locations.txt", ATOM_NAME='C', use_old=False, run_multiple=False):
	if run_multiple:
			atom1, atom2, atom3 = getAtoms(carbon_locations_file)
			if use_old:
				atom1, atom2, atom3 = getContactAtom(atom1, ATOM_NAME, atom2, ATOM_NAME, atom3, ATOM_NAME)

				complex_file = FileReader.ReadFile('complex.mol2')
				catalyst_contact_list, substrate1_contact_list, substrate2_contact_list = getAtomIndex(complex_file, atom1, atom2, substrates)
	else:
		with open(carbon_locations_file, 'r') as f:
			catalyst_contact_list  = [f.readline().strip().replace('\n','')]
			substrate_contact_list = [f.readline().strip().replace('\n','')]
		return catalyst_contact_list, substrate_contact_list, []

	return catalyst_contact_list, substrate1_contact_list, substrate2_contact_list
	

if __name__ == '__main__':
	carbon_locations_file = 'carbon_locations.txt'
	substrates = 100
	ADD_ATOM_NAME = True

	ARGS = sys.argv[1:]

	for i in range(len(ARGS)):
		arg = ARGS[i]
		
		if arg in ['-h', '--help']:
			usage()
			sys.exit()

		elif arg in ['-f', '--file']:
			carbon_locations_file = ARGS[i + 1]

		elif arg in ['-s', '--substrates']:
			substrates = int(ARGS[i + 1])

		elif arg in ['-d']:
			ADD_ATOM_NAME = False
			

	atom1, atom2, atom3 = getAtoms(carbon_locations_file)
	if ADD_ATOM_NAME:
		atom1, atom2, atom3 = getContactAtom(atom1, ATOM_NAME, atom2, ATOM_NAME, atom3, ATOM_NAME)

	complex_file = FileReader.ReadFile('complex.mol2')
	catalyst_contact_list, substrate1_contact_list, substrate2_contact_list = getAtomIndex(complex_file, atom1, atom2, substrates)

	print()
	print(f"Catalyst Contact Points: {', '.join(catalyst_contact_list)}")
	print()
	print(f"Substrate 1 Contact Points: {', '.join(substrate1_contact_list)}")
	print()
	print(f"Substrate 2 Contact Points: {', '.join(substrate2_contact_list)}")
	print()

	