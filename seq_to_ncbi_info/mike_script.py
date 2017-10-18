"""script voor mike ze tabellen"""
import subprocess

## globals
TOFILE = True


def open_en_split(file):
    inhoud = []
    with open(file, 'r') as files:
        for i in files.readlines():
           inhoud.append(i.split('\t'))
    return inhoud

def clean_make_lists(data):
    new_list = []
    for lijnen in data:
        lijnen.remove('\n')
        for i in  lijnen[1:len(lijnen)]:
            listt = i.split(' ')
            if listt[0][0:3] == "oaa":
                new_list.append([lijnen[0],listt[0], ''.join(i+ ' ' for i in listt[1: len(listt)])])
            else:
                new_list.append([lijnen[0],listt[1],''.join(i+ ' ' for i in listt[2: len(listt)])])
    return new_list


def main():
    inhoud_bestand = open_en_split('pathway_table.txt')
    clean_path = clean_make_lists(inhoud_bestand)
   # new = set(clean_path)

    if TOFILE == True:
        with open('clean_pathways.txt', 'w+') as file:
            for lines in clean_path:
                for i in lines:
                    file.write(i)
                    file.write('\t')
                file.write('\n')
        subprocess.call('cat clean_pathways.txt |sort | uniq>clean_pathway.txt; rm clean_pathways.txt' ,shell=True)

        print('done')
    else:
        print(clean_path)
        print('done')
main()