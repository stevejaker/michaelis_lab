#!/usr/bin/env python3

import time
import os, sys
import error_handler as EH

def getRuntime():
	return int(time.time() // 1)

def elapsed(start_time, prefix="\n", help=False):
	total_seconds = getRuntime() - int(start_time)

	years = total_seconds // 31535965
	remaining_time = total_seconds % 31535965

	months = remaining_time // 2628000
	remaining_time = total_seconds % 2628000

	weeks = remaining_time // 604800
	remaining_time = total_seconds % 604800

	days = remaining_time // 86400
	remaining_time = total_seconds % 86400
	
	hours = remaining_time // 3600
	remaining_time = remaining_time % 3600
	
	minutes = remaining_time // 60
	
	seconds = remaining_time % 60
	
	if years != 0:
		print(f"{prefix}Runtime: {years} Years {months} Months {weeks} Weeks {days} Days {hours} Hours {minutes} Minutes {seconds} Seconds\n")
	elif months != 0:
		print(f"{prefix}Runtime: {months} Months {weeks} Weeks {days} Days {hours} Hours {minutes} Minutes {seconds} Seconds\n")
	elif weeks != 0:
		print(f"{prefix}Runtime: {weeks} Weeks {days} Days {hours} Hours {minutes} Minutes {seconds} Seconds\n")
	elif days != 0:
		print(f"{prefix}Runtime: {days} Days {hours} Hours {minutes} Minutes {seconds} Seconds\n")
	elif hours != 0:
		print(f"{prefix}Runtime: {hours} Hours {minutes} Minutes {seconds} Seconds\n")
	elif minutes != 0:
		print(f"{prefix}Runtime: {minutes} Minutes {seconds} Seconds\n")
	else:
		print(f"{prefix}Runtime: {seconds} Seconds\n")


if __name__ == '__main__':
	ARGS = sys.argv[1:]
	prefix = None
	if len(ARGS) == 0:
		print(getRuntime())
		sys.exit()
	for i in range(len(ARGS)):
		ARG = ARGS[i]
		if ARG in ['-t', '--time']:
			try: start_time = int(ARGS[i + 1])
			except ValueError: EH.throwError("ValueError!", 1, f"Argument: {ARGS[i + 1]} not of type STRING")
			except IndexError: EH.throwError("IndexError!", 2, "COULD NOT FIND INPUT TIME!")
			if start_time < 0:
				EH.throwError("IdiotError!", 2, "Time can't be negative you idiot")
		elif ARG in ['-p', '--prefix']:
			prefix = ARGS[i + 1]
			if prefix[-1] not in [' ', '\t', '\n']:
				prefix = prefix + " "
	# try:
	if prefix is not None:
		elapsed(start_time, prefix=prefix)
	else:
		elapsed(start_time)
	# except:
	# 	print("ERROR")
		