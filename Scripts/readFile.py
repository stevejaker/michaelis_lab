import sys

def readFile(fn, return_type='list'):
	return_type = str(return_type)
	outfile = []
	with open(fn,'r') as f:
		f = f.readlines()
		for l in f:
			l = l.replace('\n','')
			outfile.append(l)
	if return_type.lower() == 'list' or return_type.lower() == '1':
		return outfile
	elif return_type.lower() == 'array' or return_type.lower() == 'list of list' or return_type.lower() == '2':
		x = 0
		array = []
		for x in range(len(outfile)):
			l = outfile[x]
			l = l.split()
			if len(l) != 0:
				array.append(l)
		return array


if __name__ == '__main__':
	readFile(sys.argv[1])