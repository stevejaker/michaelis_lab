import sys


def addCharge(glist,b_dct):
    new = []
    x = 0
    while x < len(glist):
        g = glist[x]
        if len(g) == 10:
            del g[-1]
        if len(g) == 9:
            g[5] = b_dct["{}{}".format(g[1].strip(),g[7].strip())]
        else:
            pass
        x+=1
        new.append(g)
    return new

def makeList(f):
    x = 0
    out = []
    while x < len(f):
        l = f[x]
        l = l.split( )
        if len(l) != 0:
            out.append(l)
        x += 1
    return out

def readPDBFile(fn):
    out = []
    with open(fn,'r') as f:
        f = f.readlines()
        for l in f:
            l = l.replace('\n','')
            l = l[0:17] + "  " + l[17:]
            out.append(l)
    return out


def readFile(fn):
    out = []
    with open(fn,'r') as f:
        f = f.readlines()
        for l in f:
            l = l.replace('\n','')
            out.append(l)
    return out

def makeDCT(lst):
    dct = {}
    for l in lst:
        if l[0].strip() == "ATOM" or l[0].strip() == "HETATM":
            dct["{}{}".format(l[2].strip(),l[3].strip())] = str(l[9].strip())
    return dct

def writeFile(f,fn):
    with open(fn,'w') as a:
        for l in f:
            if len(l) == 9:
                x = '%7s%6s%11s%11s%11s  %-9s%s%8s%11s'% (l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8])
                a.write(x)
                a.write('\n')
            elif len(l) == 4:
                x = '%5s%5s%5s%5s' % (l[0],l[1],l[2],l[3])
                a.write(x)
                a.write('\n')
            elif len(l) == 4:
                x = '%s%4s%4s%4s%4s' % (l[0],l[1],l[2],l[3],l[4])
                a.write(x)
                a.write('\n')
            else:
                a.write('   '.join(l))
                a.write('\n')

def run(file1, file2):
    writeFile(addCharge(makeList(readFile(file1)),makeDCT(makeList(readPDBFile(file2)))),output)

if __name__ == '__main__':

    try:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        name,ext = file1.split('.')
        output = "atom_type.mol2"
    except:
        print('\n\n-----------')
        print('-  ERROR  -')
        print('-----------\n')
    run(file1, file2)    
    print('\nFinished.\nNew File saved as: {}\n'.format(output))
