#!/usr/bin/env python3

import sys, os 


def openInpcrd(file):
	with open(file) as f:
		return f.readlines()

def writeInpcrd(file, file_list):
	with open(file, 'w') as f:
		for i in file_list:
			f.write(i)

def matchBox(file1, file2):
	file1_list = openInpcrd(file1)
	file2_list = openInpcrd(file2)
	if file1_list[-1] != file2_list[-1]:
		file2_list[-1] = file1_list[-1]
		writeInpcrd(file2, file2_list)
