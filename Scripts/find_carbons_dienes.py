#!/usr/bin/env python3

"""
VERSION 1.0
LAST UPDATED: 7/18/2019
"""
import operator

def init(filename):#Initializes the process, by reading the file. Returns the 4 carbons of interest
    with open(filename,'r') as f:
        f = f.readlines()
    pl,sl = process(f)
    if len(sl) > len(pl):
        twoSubs(pl,sl)
    else:
        try:
            pc1 = pl[0][1][1:]
            print(pc1)
            pc2 = pl[1][1][1:]
            print(pc2)
        except:
            pc1 = "Error:01"
            pc2 = "Error:01"
            print("ERROR: Couldn't Locate Peptide Carbons.")
        try:
            sc1 = sl[0][1:]
            sc2 = sl[1][1:]
            print(sc1)
            print(sc2)
        except:
            sc1 = "Error:02"
            sc2 = "Error:02"
            print("ERROR: Couldn't Locate Substrate Carbons.")
        with open('carbon_locations.txt','w') as f:
            for l in [pc1,pc2,sc1,sc2]:
                f.write(l)
                f.write('\n')
            
        
def twoSubs(pl,sl):
    try:
        pc1 = pl[0][1][1:]
        pc2 = pl[1][1][1:]
        print(pc1)
        print(pc2)
    except:
        pc1 = "Error:01"
        pc2 = "Error:01"
        print("ERROR: Couldn't Locate Peptide Carbons.")
    try:
        sc1 = sl[0][0][1:]
        print(sc1)
        sc2 = sl[0][1][1:]
        print(sc2)
        sc3 = sl[1][0][1:]
        print(sc3)
        sc4 = sl[1][1][1:]
        print(sc4)
        
    except:
        sc1 = "Error:02"
        sc2 = "Error:02"
        sc3 = "Error:02"
        sc4 = "Error:02"
        print("ERROR: Couldn't Locate Substrate Carbons.")
    with open('carbon_locations_standard_sub.txt','w') as f:
        for l in [pc1,pc2,sc1,sc2]:
            f.write(l)
            f.write('\n')
    with open('carbon_locations_cyclopentadiene.txt','w') as f:
        for l in [pc1,pc2,sc3,sc4]:
            f.write(l)
            f.write('\n')
       
    
def process(f): #Main processing function. Returns the list of the 4 carbons of nterested.
    new_file = []
    for l in f:
        l = l.replace('\n','')
        new_file.append(l)
    a = f[2]
    det = a.split( )
    split1 = int(det[0]) + 6
    al,num = cutFile(new_file,split1,6,0,1,5) #get col 5
    split2 = split1 + int(det[1]) + 1
    bl,num = cutFile(new_file,split2,num,1,2,1)
    split3 = split2 + int(det[2]) + 1
    ml,num = cutFile(new_file,split3,num,1,2,1)
    mv1,mv2,mv3 = getMolecules(ml)
    sl = 0
    if mv3[1] < 10:
        peptide,substrate,p_atoms,s_atoms = getPeptideAndSubstrate(al,mv1,mv2,bl)
        sl = checkBondsS(findAlkenes(s_atoms),substrate,s_atoms)
        return checkBondsP(findAlkenes(p_atoms),peptide,p_atoms), sl
    else:
        peptide,substrate,p_atoms,s_atoms = getPeptideAndSubstrate(al,mv1,mv2,bl)
        sl1 = checkBondsS(findAlkenes(s_atoms),substrate,s_atoms)
        peptide,substrate,p_atoms,s_atoms = getPeptideAndSubstrate(al,mv1,mv3,bl)
        sl2 = checkBondsS(findAlkenes(s_atoms),substrate,s_atoms)
        sl = [sl1,sl2,0]
        return checkBondsP(findAlkenes(p_atoms),peptide,p_atoms), sl
    
    
    
    """peptide,substrate,p_atoms,s_atoms = getPeptideAndSubstrate(al,mv1,mv2,bl)
    return checkBondsP(findAlkenes(p_atoms),peptide,p_atoms), checkBondsS(findAlkenes(s_atoms),substrate,s_atoms)"""

def checkBondsP(pl,b,p_tot):#PEPTIDE
    for x in pl:
        atom_num = x[0]
        atom_name = x[1]
        for l in b:
            remove = False
            a1 = l[0]
            a2 = l[1]
            if a1 == atom_num:
                #print('Atom {} is bonded to Atom {}'.format(atom_name,a2))
                remove,an = getAtom(a2,p_tot)
                if remove == 'nitrogen':
                    pl.remove(l)
            elif a2 == atom_num:
                #print('Atom {} is bonded to Atom {}'.format(a1,atom_name))
                remove,an = getAtom(a1,p_tot)
                if remove == 'nitrogen':
                    pl.remove(x)
    return pl

def checkBondsS(pl,b,p_tot): #SUBSTRATE
    bd = {}
    nl = []
    for x in pl:
        atom_num = x[0]
        atom_name = x[1]
        bd[atom_name] = []
        for l in b:
            remove = False
            a1 = l[0]
            a2 = l[1]
            if a1 == atom_num:
                remove,an = getAtom(a2,p_tot)
                f = bd[atom_name]
                f.append(an)
                bd[atom_name] = f
            elif a2 == atom_num:
                remove,an = getAtom(a1,p_tot)
                f = bd[atom_name]
                f.append(an)
                bd[atom_name] = f
    #print(bd)
    for x in pl:
        atom_num = x[0]
        atom_name = x[1]
        bonds = bd[atom_name]
        if bonds.count('H') == 2:
            #print("{} is a Terminal Alkene".format(atom_name))
            nl.append(atom_name)
        elif bonds.count('N') > 0:
            # nl.append(atom_name)
            pass
        elif x[2] == 'c2':
            nl.append(atom_name)
    #print(nl)
    return nl



                
def getAtom(a,pl):
    atom_list = []
    for l in pl:
        atom_num = l[0]
        atom_name = l[1]
        if atom_num == a:
            if atom_name[0:1] == "N":
                #print("Atom {} (aka {}) is a/an {} atom".format(a,atom_name,atom_name[0:1]))
                #print("ATOM REMOVED\n")
                return 'nitrogen',atom_name
            atom_list = atom_name[0:1]
            #print("Atom {} (aka {}) is a/an {} atom\n".format(a,atom_name,atom_name[0:1]))
    return False, atom_list
            
def findAlkenes(f):
    nl = []
    for l in f:
        if l[2] =='ce':
            nl.append(l)
        elif l[2] =='c2':
            nl.append(l)
        elif l[2] =='cf':
            nl.append(l)
            
    return nl
    
def getPeptideAndSubstrate(f,a,b,bl):
    peptide = findBonds((f[a[0]-1:a[1]]),bl)
    substrate = findBonds((f[b[0]-1:b[1]+b[0]-1]),bl)    
    return peptide,substrate,(f[a[0]-1:a[1]]),(f[b[0]-1:b[1]+b[0]-1])

def findBonds(f,bl):
    nl = []
    fl =[] 
    for l in f:
        nl.append(l[0])
    for l in bl:
        if l[0] in nl:
            fl.append([l[0],l[1]])
    return fl
    
def getMolecules(ml):
    nl = []
    x = 1
    for l in ml:
        atoms = int(l[1]) - x
        if atoms != 0:
            if atoms not in nl:
                nl.append([x,atoms])
        x = int(l[1])
        if len(nl) < 2:
            nl.append([atoms,0])
    mv1 = max(nl, key=operator.itemgetter(1))
    nl.remove(mv1)
    mv2 = max(nl, key=operator.itemgetter(1))
    nl.remove(mv2)
    mv3 = max(nl, key=operator.itemgetter(1))
    return mv1,mv2,mv3
        
def cutFile(f,split,num,d,e,g):#Cuts file into sections. Returns a list of atoms, bonds, or molecules
    nl = []
    if g==d:
        while num < split:
            try:
                l = f[num]
                l = l.split( )
                nl.append([l[d],l[e],l[g]])
            except:
                pass
            num += 1
    else:
        while num < split:
            try:
                l = f[num]
                l = l.split( )
                nl.append([l[d],l[e],l[g]])
            except:
                pass
            num += 1
    return nl,num




if __name__ == '__main__':
    test = '/home/sjaker12/forcefieldsWork/20ns_1/20ns_1/'
    init('complex1.mol2')
