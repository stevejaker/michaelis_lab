#!/usr/bin/env python3

def usage():
	print("""
Usage:
	runtraj.py [options]

Options:
	-h,  --help 			Shows this message	
""")

# def main():
# 	pass

class LocationStudy():
	def __init__(self, array_pieces, mpi=True, mpi_type='MPI', cores=16, pieces=None, mem=6, mem_type='G',
				nodes=1, test=False, user=None, days='00', hrs='01', mins='00',
				script_name='runtraj'):
		# SBATCH Information
		self.mem = mem
		self.mem_type = mem_type
		self.nodes = nodes
		self.cores = cores
		self.test = test
		self.user = user
		self.days = days
		self.hrs = hrs
		self.mins = mins
		self.array_pieces = array_pieces


		# MPI Information
		self.mpi = mpi
		if self.mpi:
			if mpi_type.lower() == 'omp':
				self.mpi_type = "MPI.OMP"
			else:
				self.mpi_type = "MPI"

		# self.substrate_molecules = substrate_molecules
		self.pieces = pieces

		# Control Information
		self.script_name = script_name

	def getTrajInfo(self):
		"""
		Sets up if we are running MPI, which type of MPI and how many types of substrate we are running.
		"""
		if self.mpi:
			if self.pieces == 1:
				return 'mpirun -np 16 cpptraj.{0} -i cpptraj_C${1}_S.in'.format(self.mpi_type, "{SLURM_ARRAY_TASK_ID}")
			else:
				return '\n'.join(['mpirun -np 16 cpptraj.{0} -i cpptraj_C${1}_S{2}.in'.format(self.mpi_type, "{SLURM_ARRAY_TASK_ID}", i) for i in range(1, self.pieces + 1)])
		else:
			if self.pieces == 1:
				return 'cpptraj -i cpptraj_C${SLURM_ARRAY_TASK_ID}_S.in'
			else:
				return '\n'.join(['cpptraj -i cpptraj_C${0}_S{1}.in'.format("{SLURM_ARRAY_TASK_ID}", i) for i in range(1, self.pieces + 1)])

	def getPyInfo(self):
		if self.pieces == 1:
			return "location.py -i distance_C_${SLURM_ARRAY_TASK_ID}_S_all.dat"
		else:
			return "\n".join(["location.py -i distance_C_${0}_S{1}_all.dat".format("{SLURM_ARRAY_TASK_ID}", i) for i in range(1, self.pieces + 1)])


	def write(self):
		SLURM_ARRAY_TASK_ID = "{SLURM_ARRAY_TASK_ID}"
		with open(self.script_name, 'w') as f:
			f.write(f"""#!/bin/bash

#SBATCH --time={self.days}-{self.hrs}:{self.mins}         # time (DD-HH:MM)
#SBATCH --nodes={self.nodes} --ntasks-per-node={self.cores}
#SBATCH --mem-per-cpu={self.mem}{self.mem_type}   # memory per CPU core
#SBATCH --mail-user={self.user}@byu.edu   # email address
#SBATCH --mail-type=FAIL
#SBATCH --requeue
#SBATCH --array=1-{self.array_pieces}%1 # LIMITS TO ONE JOB AT A TIME TO PREVENT OVERFLOW. LIKE LEGIT 2 FREAKING PETABYTES OF DATA COULD BE WRITTEN HERE...
{'#SBATCH --qos=test' if self.test else ''}

. /etc/profile

# Because this function is so much freaking easier lol
loadamber 

echo "Running cpptraj.MPI for Catalyst atom ${SLURM_ARRAY_TASK_ID}"

{self.getTrajInfo()}

echo "Finished running cpptraj"

echo "
Running location.py
"

{self.getPyInfo()}

echo "
DONE!
"
""")



if __name__ == '__main__':
	import sys, os
	for i in range(len(ARGS)):
		ARG = ARGS[i]
		if ARG in ['-h', '--help']:
			usage()
			sys.exit()
		elif ARG in ['option1', 'option2']:
			variable = ARGS[i + 1]
		# Insert Other Options Here
	main()

