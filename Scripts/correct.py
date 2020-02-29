
import sys

new_file = []
with open(sys.argv[1]) as f:
	f = f.readlines()
	for l in f:
		l = l.replace('ALN  ',"{} A".format(sys.argv[2]))
		l = l.replace('UNL A',"{} B".format(sys.argv[3]))
		l = l.replace('UNL B',"{} C".format(sys.argv[4]))
		new_file.append(l)
with open(sys.argv[1],'w') as f:
	for l in new_file:
		f.write(l)

