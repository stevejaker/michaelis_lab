#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --time=00:00:01
#SBATCH --mem-per-cpu=1M
#SBATCH --array=1-3%1 

if [[ "${SLURM_ARRAY_TASK_ID}" -eq "1" ]]; then
	# If this is ARRAY_TASK_ID 1, sander1, we pass our Arguments here so we can run leap corectly

	runamber $SLURM_ARRAY_TASK_ID $@


else
	# If it is not ARRAY_TASK_ID 1, just run the next job in the line
	runamber $SLURM_ARRAY_TASK_ID
fi


