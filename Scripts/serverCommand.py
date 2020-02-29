#!/usr/bin/env python3

import os, sys
from shutil import copy, copytree, rmtree
from getpass import getuser
from subprocess import call, check_output

WORKDIR = os.getcwd()   # Pulls Current Work Directory
USER = getuser()     # Pulls Username
ARGS = sys.argv[1:]  # Takes input arg vector and removes the program name
SERVER_LOGIN = f"{USER}@ssh.rc.byu.edu"
#
# INSERT DEFAULT VARIABLES HERE
#


def usage():
	print("""
Usage:
	serverCommand.py [options]

Options:
	-h,  --help 			Shows this message	
""")

def runCommands(command_list):
	global SERVER_LOGIN
	# Triggers Login to the Server
	commands = ['ssh', SERVER_LOGIN]
	
	# Adds commands to the list
	for cmd in command_list:
		commands.append(cmd)

	# Actually Executes the Commands
	call(commands)


def run(cmd):
	command_list = cmd.split()
	runCommands(command_list)


if __name__ == '__main__':
	for i in range(len(ARGS)):
		ARG = ARGS[i]
		if ARG in ['-h', '--help']:
			usage()
			sys.exit()
		elif ARG in ['option1', 'option2']:
			variable = ARGS[i + 1]
		# Insert Other Options Here
	run()

