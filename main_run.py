import os
import subprocess
import math
import sys
# gloabals

input_seq = 'seq_a3.fa'
proteome = "uniprot-proteome%3AUP000002279.fasta"

def save_data_and_gene_info(hits, protenome_file, seq):
    for hit in hits:

        hit_name = hit.split('|')[1]
        hit_len = int(hit.split('\t')[3])
        print(hit_len, hit_len/60, math.floor(hit_len/60))
        hit_protien_info = str(subprocess.check_output('egrep '+hit_name+' '+protenome_file + '  -n'+  str(int(math.floor((hit_len/60)+2))), shell=True), 'utf8' )
        #print(hit_protien_info)
        #print(hit_name,hit_len)



def runblast(list_of_seq):
    num = 0
    best_hits = []
    for seq in list_of_seq:
        tmp_seq_file = open('seq_tmp_file.fa', 'w+')
        tmp_seq_file.write(seq)
        #best_hits.append(os.system("blastall -d "+proteome+" -i seq_tmp_file.fa -p blastx -m8 | head -n1"))
        best_hits.append(str(subprocess.check_output(["blastall -d "+proteome+" -i seq_tmp_file.fa -p blastx -m8 | head -n1"], shell=True),'utf8'))
        num +=1
    best_hits.pop(0)
    return best_hits


def open_seq_to_list(file):
    list_of_seq = []
    with open(input_seq, 'r') as file:
        tmp_string = ''

        for i in file.readlines():
            if i[0] == '>':
                tmp_string += i
            else:
                tmp_string += i
                list_of_seq.append(tmp_string)
                tmp_string = ''
    return list_of_seq


def setup_map(protoonomefile):
    # make db
    os.system("formatdb -i "+ proteome+"  -p T")

    print(subprocess.check_output('ls', shell=True))


def main():
   # setup_map(None)
    list_of_seq = open_seq_to_list(None)
    best_hit_per_seq = runblast(list_of_seq)
    print('test')
    for i in best_hit_per_seq:
        print(i)

    save_data_and_gene_info(best_hit_per_seq, proteome, input_seq)

    #print(best_hit_per_seq)
main()


#data = str(subprocess.check_output("ifconfig| tail -n2 | head -n1|sed -e 's/(/ /g'|  awk {'print $2,$3 \"|\" $6,$7'}", shell=True), 'utf8').strip('\n').split('|')
