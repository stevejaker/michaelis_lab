#!/user/bin/env python

import sys, os

def throwError(error, error_code, message):
	print()
	print(f'ERROR {error_code}: {error}')
	print(message)
	print()
	sys.exit()

def giveWarning(warning, message):
	print()
	print('WARNING!')
	print(message)
	print()