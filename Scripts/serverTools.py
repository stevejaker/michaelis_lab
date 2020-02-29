import sys, os
from subprocess import check_output, call
from getpass import getuser

def submit():
	inp = input('Would you like to submit this job on the supercomputer? (Default: No)\n[ Yes | No | Sync ] >> ')
	if inp.lower() in ['sync'] :
		return 'sync'
	elif inp.lower() in ['y', 'yes']:
		return 'submit'
	else:
		return 'no'

def syncDir():
	user= getuser()
	server_login = f"{user}@ssh.rc.byu.edu" 
	workdir = os.getcwd()
	new_dir = workdir.replace('/home/', '/zhome/')
	new_dir = new_dir.replace('/storage/','/compute/') # This might be unnecessary
	# end = new_dir.rfind('/')
	sync_dir = new_dir[:new_dir.rfind('/')] # removes slash
	try:
		# Make New Directory
		call([
			'ssh', server_login,
			'mkdir', '-p', new_dir
			])
		# Sync Directory
		call([
			'rsync', '-raz', '--update', '--progress',
			workdir, f"{server_login}:{sync_dir}"
			])
		print('\nSync Complete\n')
	except:
		print('ERROR: Something went wrong when attempting to sync with your server! Aborting!')
		sys.exit()
	return new_dir

def runJob(new_dir, run_script):
	user= getuser()
	server_login = f"{user}@ssh.rc.byu.edu" 
	try:
		call([
			'ssh', server_login,
			'cd', f'{new_dir};',
			'sbatch', run_script
			])
	except:
		print(f'ERROR: Something went wrong when attempting to run your job: {run_script}! Aborting!')
		sys.exit()