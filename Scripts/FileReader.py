#!/usr/bin/env python3

import os, sys

class ReadFile():
	def __init__(self, file):
		self.InputType = None
		self.MoleculeName = "*****"
		self.MoleculeType = 'SMALL'
		self.MoleculeChargeType = 'User Charges'
		self.Filename = file
		self.AtomNum = 0
		self.BondNum = 0
		self.AtomDetails = {}
		self.BondDetails = {
		"bonds":[]
		}
		self.TotalCharge = 0
		idx = file.rfind('.')
		self.InputType = file[idx + 1 :].lower()
		if self.InputType == 'mol2':
			self.readMol2(file)
		elif self.InputType == 'pdb':
			self.readPDB(file)
		# readMolecule(self, file)

	def readMol2(self, file):
		with open(file, 'r') as f:
			F = f.read()
			self.checkMol2Format(F) # Runs check before proceeding
			f = F.split('\n')
		for i in range(len(f)):
			line = f[i]
			line = line.replace('\n','')
			if '@<TRIPOS>MOLECULE' in line:
				self.readMol2Molecule(f, i + 1)
			elif '@<TRIPOS>ATOM' in line:
				self.readMol2Atoms(f, i + 1)
			elif '@<TRIPOS>BOND' in line:
				self.readMol2Bonds(f, i + 1)

	def checkMol2Format(self, file):
		if '@<TRIPOS>MOLECULE' not in file:
			self.fileError('Format', 'reading', '@<TRIPOS>MOLECULE NOT IN FILE!')
		elif '@<TRIPOS>ATOM' not in file:
			self.fileError('Format', 'reading', '@<TRIPOS>ATOM NOT IN FILE!')
		elif '@<TRIPOS>BOND' not in file:
			self.fileError('Format', 'reading', '@<TRIPOS>BOND NOT IN FILE!')
		else:
			pass
			# print('\nSybyl Mol2 Format is Correct. Continuing reading file...\n')

	def readMol2Molecule(self, file, i):
		self.MoleculeName = file[i].replace('\n', '')
		control_info = file[i + 1].replace('\n', '')
		control_info = control_info.split()
		self.AtomNum = int(control_info[0])
		self.BondNum = int(control_info[1])
		# The remaining parts of control_info are rarely used and essentially pointless
		# Hence, they are not included in the ReadMol2 Object
		self.MoleculeType = file[i + 2].replace('\n', '')
		self.MoleculeChargeType = file[i + 3].replace('\n', '')

	def readMol2Atoms(self, file, i):
		for i in range(i, i + self.AtomNum):
			initial_line = file[i]
			line = initial_line.split()
			try: atom_number = int(line[0])
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Number\nLINE: {initial_line}')
			try: atom_name = line[1]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Name\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: x_coord = line[2]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify X Coordinate\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: y_coord = line[3]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Y Coordinate\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: z_coord = line[4]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Z Coordinate\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: atom_type = line[5]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Type\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: residue_num = int(line[6])
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Residue Number\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: residue_name = line[7]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Residue Name\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: atom_charge = line[8]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Charge\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			self.AtomDetails[atom_number] = {
				"atom_number": atom_number,
				"atom_name": atom_name,
				"x_coord": x_coord,
				"y_coord": y_coord,
				"z_coord": z_coord,
				"atom_type": atom_type,
				"residue_num": residue_num,
				"residue_name": residue_name[:3],
				"atom_charge": atom_charge,
				"bonded_to": []
			}

	def readMol2Bonds(self, file, i):
		for i in range(i, i + self.BondNum):
			initial_line = file[i]
			line = initial_line.split()
			try: bond_number = int(line[0])
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Bond Number\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: atom1 = int(line[1])
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom #1 in Bond {bond_number}\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: atom2 = int(line[2])
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom #2 in Bond {bond_number}\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			try: bond_type = line[3]
			except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Type in Bond {bond_number}\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
			self.BondDetails[bond_number] = {
				"bond_number": bond_number,
				"atom1": atom1,
				"atom2": atom2,
				"bond_type": bond_type,
			}
			if atom1 not in self.AtomDetails[atom2]['bonded_to']:
				self.AtomDetails[atom2]['bonded_to'].append(atom1)
			if atom2 not in self.AtomDetails[atom1]['bonded_to']:
				self.AtomDetails[atom1]['bonded_to'].append(atom2)

	def writeMol2File(self, output_filename):
		with open(output_filename, 'w') as f:
			f.write(f'''@<TRIPOS>MOLECULE
{self.MoleculeName}
{self.AtomNum} {self.BondNum} 0 0 0
{self.MoleculeType}
{self.MoleculeChargeType}

@<TRIPOS>ATOM
''')
			for i in range(1, self.AtomNum + 1):
				l = self.AtomDetails[i]
				line = "{:>3} {:<4}{:>12}{:>12}{:>12} {:<6}{:<3} {:<4}{:>10}\n".format(
				l['atom_number'], l['atom_name'], l['x_coord'],
				l['y_coord'], l['z_coord'], l['atom_type'],
				l['residue_num'], l['residue_name'], l['atom_charge'])
				f.write(line)

			f.write('\n@<TRIPOS>BOND\n')
			for i in range(1, self.BondNum + 1):
				l = self.BondDetails[i]
				line = "{:<3} {:<3} {:<3} {:<3}\n".format(
				l['bond_number'], l['atom1'],
				l['atom2'], l['bond_type'])
				f.write(line)

	def readPDB(self, file):
		with open(file, 'r') as f:
			F = f.read()
			f = F.split('\n')
			f.remove('')
		for i in range(len(f)):
			line = f[i]
			line = line.replace('\n','')
			line = line.split()
			if 'COMPND' in line[0]:
				del line[0]
				self.MoleculeName = " ".join(line)
			elif 'ATOM' in line[0]:
				self.readPDBAtoms(line)
			# FIXME -- This section is quite buggy...
			elif 'CONECT' in line[0]:
				self.readPDBConnectivity(line)
			elif 'MASTER' in line[0]:
				self.AtomNum = int(line[9])
				self.BondNum = int(line[11])
		self.readPDBBonds()

	def readPDBConnectivity(self, line):
		# Supports up to 6 bonds!
		atom1 = int(line[1])
		atom2 = int(line[2])
		try: atom3 = int(line[3])
		except: atom3 = 0
		try: atom4 = int(line[4])
		except: atom4 = 0
		try: atom5 = int(line[5])
		except: atom5 = 0
		try:atom6 = int(line[6])
		except: atom6 = 0
		del line[0] # removes header
		del line[0] # removes atom 1
		self.AtomDetails[atom1]['bonded_to'] = line # translates remaining part of the list into bonded_to
		if checkPDBAtoms(atom1, atom2):
			self.BondDetails['bonds'].append((atom1, atom2))
		elif checkPDBAtoms(atom1, atom3):
			self.BondDetails['bonds'].append((atom1, atom3))
		elif checkPDBAtoms(atom1, atom4):
			self.BondDetails['bonds'].append((atom1, atom4))
		elif checkPDBAtoms(atom1, atom5):
			self.BondDetails['bonds'].append((atom1, atom5))
		elif checkPDBAtoms(atom1, atom6):
			self.BondDetails['bonds'].append((atom1, atom6))

	def checkPDBAtoms(self, atom1, atom2):
		# Returns true if the bond is not recorded AND if both bond atoms are nonzero
		if atom1 != 0 and atom2 !=0 and (atom1, atom2) not in self.BondDetails['bonds'] and (atom2, atom1) not in self.BondDetails['bonds']:
			return True
		else:
			return False

	def readPDBAtoms(self, line):
		try: atom_number = int(line[1])
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Number\nLINE: {initial_line}')
		try: atom_name = line[2]
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Name\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		try: residue_name = line[3]
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Residue Name\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		try: residue_num = int(line[5])
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Residue Number\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		try: x_coord = line[6]
		except: self.fileError('Format', 'reading', f'Couldn\'t identify X Coordinate\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		try: y_coord = line[7]
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Y Coordinate\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		try: z_coord = line[8]
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Z Coordinate\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		try: atom_type = line[11][0]
		except: self.fileError('Format', 'reading', f'Couldn\'t identify Atom Type\nLINE: {initial_line}') # FIXME -- ADD ERROR MSG
		atom_charge = "0.0000" # PDB files don't contain charge, so we need to add a zero charge if it is converted to mol2
		self.AtomDetails[atom_number] = {
			"atom_number": atom_number,
			"atom_name": atom_name,
			"x_coord": x_coord,
			"y_coord": y_coord,
			"z_coord": z_coord,
			"atom_type": atom_type,
			"residue_num": residue_num,
			"residue_name": residue_name[:3],
			"atom_charge": atom_charge,
			"bonded_to": []
		}

	def readPDBBonds(self):
		# Writes connectivity that is readable for mol2 files
		for i in range(len(self.BondDetails['bonds'])):
			bond_number = i + 1
			atom1 = self.BondDetails['bonds'][0]
			atom2 = self.BondDetails['bonds'][1]
			self.BondDetails[bond_number] = {
				"bond_number": bond_number,
				"atom1": atom1,
				"atom2": atom2,
				"bond_type": 1,
			}

	def writePDBFile(self, output_filename):
		with open(output_filename, 'w') as f:
			f.write(f"COMPND\t{self.MoleculeName}\n")
			f.write(f"AUTHOR\tGENERATED BY TEAMVP\n")

			for i in range(1, self.AtomNum + 1):
				l = self.AtomDetails[i]
				f.write('ATOM{:>7} {:<4} {:<3} A{:>4}    {:>8}{:>8}{:>8} 1.00 0.00          {:>2}\n'.format(
				l['atom_number'], l['atom_name'], l['residue_name'],
				l['residue_num'], l['x_coord'], l['y_coord'],
				l['z_coord'], l['atom_type'][0].upper()))

			for i in range(1, self.AtomNum + 1):
				f.write('CONECT{:>5}'.format(i))
				for bond in self.AtomDetails[i]['bonded_to']:
					f.write('{:>5}'.format(bond))
				f.write('\n')
			## ENDING -- Probably need to format better....
			f.write(f"MASTER        0    0    0    0    0    0    0    0   {self.BondNum}    0   {self.BondNum}    0\n")
			f.write("END\n")

	def fileError(self, error_type, error_action, error_message):
		print(f'{error_type} error was occurred when {error_action} your {self.InputType} file.')
		print(f'ERROR MESSAGE: {error_message}')
		sys.exit()

	def write(self, filename, filetype='mol2'):
		if filetype.lower() == 'mol2':
			self.writeMol2File(filename)
		elif filetype.lower() == 'pdb':
			self.writePDBFile(filename)
		else:
			print("Cannot Identify Filetype")