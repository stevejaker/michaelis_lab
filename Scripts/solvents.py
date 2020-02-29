#!/usr/bin/env python3

def getSolvents(solvent=""):
	# Options for solvent:
	#	'None' -- Requests User Input
	from getpass import getuser
	user = getuser()
	solvent_dct = {}
	x = 1
	try:
		with open(f'/home/{user}/zTeamVPScripts/solvents/solvent_list') as f:
			f = f.readlines()
	except:
		with open(f'/zhome/{user}/zTeamVPScripts/solvents/solvent_list') as f:
			f = f.readlines()

	for i in f:
		i = i.replace('\n', '')
		i = i.split()
		if i != "":
			solvent_name = i[0]
			off_file 	 = i[1]
			frcmod_file  = i[2]
			res_name	 = i[3]
			if solvent_name != "" and solvent_name.lower() == solvent.lower():
				return solvent_name, off_file, frcmod_file, res_name
			else:
				solvent_dct[x] = {
					"solvent_name": solvent_name,
					"frcmod_file": frcmod_file,
					"off_file": off_file,
					"res_name": res_name
				}
			x += 1
	displaySolvents(solvent_dct)
	return getUI(solvent_dct)

def displaySolvents(solvent_dct):
	# NOT DISPLAYING RESIDUE NAME
	print(' {:-<85} '.format('-'))
	print("|{:^6}|{:^25}|{:^25}|{:^25}|".format('ID', 'Solvent Name', 'Off File', 'Frcmod File'))
	print(' {:-<85} '.format('-'))
	for i in solvent_dct:
		d = solvent_dct[i]
		print("|{:^6}|{:^25}|{:^25}|{:^25}|".format(i, d['solvent_name'], d['off_file'], d['frcmod_file']))
	print(' {:-<85} '.format('-'))

def getUI(solvent_dct, solvent=0):
	if solvent == 0:
		solvent = int(input("Select a solvent ID >> "))
		if solvent in solvent_dct:
			solvent_name	= solvent_dct[solvent]['solvent_name']
			off_file 		= solvent_dct[solvent]['off_file']
			frcmod_file	 	= solvent_dct[solvent]['frcmod_file']
			res_name		= solvent_dct[solvent]['res_name']
		else:
			print(f"Selection {solvent} not recognized.")
			getUI(solvent_dct)
	return solvent_name, off_file, frcmod_file, res_name

if __name__ == '__main__':
	solvent_name, off_file, frcmod_file, res_name = getSolvents()
	