#!/usr/bin/env python3

import os, sys

def usage():
	print("""
Usage:
	runCppTraj.py [options]

Options:
	-h,  --help 			Shows this message	
""")


def main(trajdir, MPI, OMP, cores, file="cpptraj.in"):
	import bashcall
	import subprocess
	if MPI:
		bashcall.listCall(["module purge",
			#"export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE",
			"module load gcc/7 openmpi python/3.6 amber/18",
			"echo \"Cpptraj run started at `date`\"",
			f"mpirun -np {cores} cpptraj.MPI -i {file}",
			"echo \"Cpptraj run ended at `date`\"",
			])
	elif OMP:
		bashcall.listCall(["module purge",
			#"export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE",
			"module load gcc/7 openmpi python/3.6 amber/18",
			"echo \"Run started at `date`\"",
			f"mpirun -np {cores} cpptraj.MPI -i {file}",
			"echo \"Run ended at `date`\"",
			])
	else:
		subprocess.call([f"{trajdir}cpptraj", "-i", file])


