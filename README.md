# Information

Dr. David Michaelis is a professor of Organic Chemistry at Brigham Young University

Working in his lab under Jacob Parkman (PhD Candidate), I participated in studies regarding Computational Chemistry.
We used the following programs in our research (list is still being updated)
  -- AmberMD
  -- GAMESS
  -- Gaussian
  -- RED 3
  -- CP2K
  -- Chimera
  -- Avogadro
  -- Openbabel
  -- CPPTraj
  -- ...
AmberMD was our principal program for running our computational simulations and requires substantial user input. This became very time consuming, requiring us to automate the majority of our steps in this process. The vast majority of our work in terms of building input files, molecular structures, and other necessary pieces for simulation occured on our local machines, while nearly all calculations were performed using the BYU marylou supercomputer (Huge thank you to the BYU Office of Research Computing). File transfers and job scheduling (using the SLURM workload manager) were also important components of our process.

It was my responsibility to automate everything that could be automated. To do this, I created a suite of programs (particularly command line executables) using Python, BASH/Shell scripting, and Perl to allow entire simulations (ranging from 10 minutes to 3+ days) to be prepared, submitted, and analyzed using a single command line tool. These command line tools primarily served as wrappers to execute multiple unrelated programs that required user input in a way that required as little human interaction as possible.

The listed programs are written over 1 year and demonstrate learning over time. Concepts such as OOP were not used as frequently near the start of the project; however, as my knowledge increased, so did the complexity and utility of the code output.
