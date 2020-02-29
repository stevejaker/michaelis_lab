#!/usr/bin/env python3

from subprocess import call

def makeFrcmod(molecule, file_format):
	print(f'Running parmchk2 for {molecule}.{file_format}...\n')
	call([	'parmchk2',
			'-i', f"{molecule}.{file_format}",
			'-f', file_format, 
	 		'-o', f"{molecule}.frcmod" ]) 
	print('Parmchk2 has finished running.\n')


if __name__ == '__main__':
	for i in range(len(sys.argv)):
		arg = sys.argv[i]
		if i in '-i':
			molecule, file_format = sys.argv[i + 1].split('.')
			makeFrcmod(molecule, file_format)
