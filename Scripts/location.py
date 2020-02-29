#!/usr/bin/env python3 

MIN = 3.38
MAX = 3.42

def usage():
	print('Yeah, yeah, yeah, I\'m working on it lol.')
	sys.exit()

def warn(message):
	print('Warning!')
	print(message)

def error(message, kill=True):
	print('Error!')
	print(message)
	if kill:
		print('Aborting Program...')
		sys.exit()

def cleanup(input_filename, tempfile_name):
	print(f'Replacing {input_filename} with {tempfile_name}')
	shutil.move(tempfile_name, input_filename)

def checkDistance(line):
	"""
	Returns 1 
	"""
	global MIN, MAX
	for distance in line:
		try: 
			if MIN < float(distance) < MAX:
				return 1
		except:
			error('Could not identify distances as floating point numbers.')
		return 0

def contactsOut(contacts, infile_name, tempfile_name=None, outfile_name=None, method='a+'):
	if outfile_name == None:
		outfile_name = infile + '-out'

	if tempfile_name == None:
		tempfile_name = infile_name + '-TEMP'

	if method in ['write', 'w', 'w+']:
		method_code = 'w'
	else:
		method_code = 'a+'

	with open(tempfile_name, 'r') as tempfile, open(outfile_name, method_code) as outfile:
		# vvvv Thats a money one-liner right there! vvvv
		tempfile_contacts = sum([int(i) for i in tempfile.readline().strip().split()])
		if tempfile_contacts == contacts:
			outfile.write(f'Contacts for {infile_name}: {contacts}\n')
			print(f'Finished parsing {infile_name}. Total contacts: {contacts}')
			cleanup(infile_name, tempfile_name)
		else:
			warn(f'The tempfile contacts {tempfile_contacts} does not match the number of contacts recorded ({contacts})!!!\nNothing will be written to {outfile_name}.')

def readAndProcess(infile_name, outfile_name=None, method='append'):
	"""
	This function will process the file in the most efficient way possible
	Testing showed this method is up to 10x faster than using vectors in C++ 
	and 2x faster than using arrays in C++, so yeah...
	"""
	contacts = 0
	line_number = 1
	tempfile_name = infile_name + '-TEMP'

	if outfile_name == None:
		outfile_name = infile_name + '-out'

	if method in ['write', 'w', 'w+']:
		method_desc = 'writing'
		method_code = 'w'
	else:
		method_desc = 'appending'
		method_code = 'a+'

	print(f'Reading {infile_name}, {method_desc} to the outfile {outfile_name}.\nTemporary Values will be stored in the file {tempfile_name}')

	with open(infile_name, 'r') as infile, open(tempfile_name, 'w') as tempfile: 
		for line in infile:
			"""
			Note: `line` indicies are as follows 
			line[0] = frame number
			line[1] ... line[-1] correspond to the atoms on the substrate
			
			Logic -- Explaining how dope this is.
			If ANY of the numbers from line[1]:line[-1] is in the range defined
			for 'contacts', this means there is a contact for the catalyst atom
			in that frame. I am only allowing ONE CONTACT PER FRAME!!! If a 
			contact is detected, the variable `contacts` will be incremented and
			a single line TSV tempfile will be written with a 1 (indicating a 
			contact) or a 0 (indicating no contact). If `contacts` does not match
			this count, an error will be sent. If it does, the tempfile will be
			renamed and will serve as a type of logfile which shows which frames 
			have contacts.
			"""
			if line_number == 1:
				# This might not be needed
				headers = line.split() 
				line_number += 1
			else:
				line = line.split() 
				result = checkDistance(line[1:])
				contacts += result
				tempfile.write(f'{"    " if line != 2 else ""}{result}')
				line_number += 1

	contactsOut(contacts, infile_name, tempfile_name=tempfile_name, outfile_name=outfile_name, method='a+')

	# with open(tempfile_name, 'r') as tempfile, open(outfile_name, method_code) as outfile:
	# 	tempfile = tempfile.readline().strip().split()

if __name__ == '__main__':
	import sys
	import os
	import shutil

	ARGS = sys.argv[1:]
	infile_name = None
	outfile_name = None
	method = None

	for i in range(len(ARGS)):
		ARG = ARGS[i]
		
		if ARG in ['-h', '--help']: 
			usage()
		
		elif ARG in ['-ma', '--max']: 
			MAX = float(ARGS[i + 1])
		  
		elif ARG in ['-mn', '--min']: 
			MIN = float(ARGS[i + 1])
		
		elif ARG in ['-i', '--infile']: 
			infile_name = ARGS[i + 1]
		
		elif ARG in ['-o', '--outfile']: 
			outfile_name = ARGS[i + 1]
		
		elif ARG in ['-m', '--method']: 
			method = ARGS[i + 1]

	if infile_name == None:
		error("No infile provided! We can't analyze nothing...")

	readAndProcess(infile_name, outfile_name=outfile_name, method=method)



