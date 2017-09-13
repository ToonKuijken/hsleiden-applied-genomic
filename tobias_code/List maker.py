# -*- coding: utf-8 -*-
from astropy.table import Table

def maak_tabel(lijst_eiwitnamen, lijst_eiwitcodes):
    t = Table([lijst_eiwitcodes,lijst_eiwitnamen], names=('Eiwitcodes',\
          'Eiwitnamen'))
    return(t)

def maak_lijsten():
    lijst_eiwitnamen = []
    lijst_eiwitcodes = []
    eiwitnamen = open('Eiwitnamen', 'r')
    eiwitcodes = open('XP', 'r')
    for i in eiwitnamen:
        i = i.rstrip()
        lijst_eiwitnamen.append(i)
    for i in eiwitcodes:
        i = i.rstrip()
        lijst_eiwitcodes.append(i)
    return lijst_eiwitnamen, lijst_eiwitcodes
    
def main():
    eiwitnamen, eiwitcodes = maak_lijsten()
    tabel = maak_tabel(eiwitnamen, eiwitcodes)
    print(tabel)
main()

#cat ncbi_protien_info.txt | egrep '>XP' | sort | uniq | awk '{ print $1, substr($0, index($0,$3))}' > Eiwitcode_plus_naam