import os
import subprocess
import math
import sys
import  csv


"""Een tabel met voor elk gen in jullie dataset : De ID, de naam, lengte/sequentie, eiwit(ten) gecodeerd op het gen.
    Een tabel met voor elk eiwit in jullie dataset: De accession code, de naam,
     lengte/aminozuursequentie. Informatie over splicing varianten.
Annotatie van functie en pathway."""""

input_seq = 'seq_a3.fa'
proteome = "uniprot-proteome%3AUP000002279.fasta"
ncbi_koppel_db = "GCF_000002275.2_Ornithorhynchus_anatinus_5.0.1_rna.fna"
protenome_ncbi = 'GCF_000002275.2_Ornithorhynchus_anatinus_5.0.1_protein.faa'
outpute_name = 'ncbi_protien_info.txt'
output_folder = 'sequence_info'

def sort_info(output_folder):
    """hier alle funtie vppr eht soorteren en zo . dua om tabellen te maken en alle info uit de bestandent te halen.
    """
    subprocess.check_call('bash bash_info_seq.sh '+ output_folder, shell=True)

def info_protien_en_meer(protien_list):
    """ hier word info van ncbi met bash gekregen. hierna
    word allles in een betand gegooit. hier kan dus alles per seq uit gehaald worden.
    """
    for protien_info in protien_list:
        name = protien_info[1][1]
        lis.append(name)
        seq_name = str(protien_info[0])


        All_seq_info = []
        All_seq_info.append(protien_info)
        subprocess.call('bash getinfoandid.sh '+name + ' ' + output_folder+ ' '+ seq_name, shell=True,  stderr=None)
        with open(seq_name+".txt", 'r') as main_file:
            All_seq_info.append(main_file.readlines())
            All_seq_info.append('\n')
        with open(seq_name + "_gene.txt", 'r') as gene_file:
            All_seq_info.append(gene_file.readlines())
            All_seq_info.append('\n')
        with open(seq_name + "_mRNA.txt", 'r') as mRNA_file:
            All_seq_info.append(mRNA_file.readlines())
            All_seq_info.append('\n')
        with open(output_folder + '/'+ seq_name+'.txt', 'w+') as output_file:
            for info in All_seq_info:
                output_file.write(''.join(str(i) for i in info))
                output_file.write('\n')
        subprocess.call('rm '+ seq_name+'.txt '+ seq_name+'_gene.txt '+ seq_name+'_mRNA.txt html.txt', shell= True)



def return_full_seq(name, protenome_ncbi):
    """

    :param name:
    :param protenome_ncbi:
    :return:
    """
    all_protiens = []
    hit_protien_info = str(subprocess.check_output('egrep ' + name + ' ' + protenome_ncbi + '  -n', shell=True), 'utf8')
    with open(protenome_ncbi, 'r') as protien_seq:
        all_protiens += (protien_seq.readlines())
        # print(all_protiens)

        gen_seq_and_info = all_protiens[int(hit_protien_info.split(':')[0]) - 1]
        for lines in range(int(hit_protien_info.split(':')[0]), len(all_protiens)):
            if all_protiens[lines][0] != '>':
                gen_seq_and_info += all_protiens[lines]
            else:
                return gen_seq_and_info


def make_dic_information_gene(hits_list, protenome_ncbi):
    """Dict layout : key = name seq.| full hit, naam ncbi protien, leng, volle serquentie, info van ncbi wget stuff

    :param hits_list:
    :return:
    """
    gene_dict = []
    for hit in hits_list:
        gene_dict.append([hit.split('\t')[0], [hit, hit.split('\t')[1], 'nan',
                                               return_full_seq(hit.split('\t')[1], protenome_ncbi)]])
    return gene_dict


def fasta_file_to_list(file):
    """ Loopt door een faste bestand door en maakt hier een lijst van.
    door dat een fasta niet alles wat je wilt op een lijn staat id er een if els nodig.
    Wanneer line begint met '>'  is dit de info van het fasta bestand. Deze line word dan
    toegevoegd aan een tijdelijke string.
    Dan gaat de loop veder door de lijst van het bestand tot er iets anders tegen komt dat
     niet met '>'begint. nu word de tijdelijke string toegevoegd aan een lijst met alle serquenteies en word de var leeggemaakt.
    wanner er door het hele bestand gelopen is word de lijst met fasta terug gegeven.

    :param file: Bestand : een bestand in fasta formaat waar serquenties in staan.
    :return: lijst: Hier zitten alle serquenties in met de naam.
    """
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


def blast_db_ncbi(input, db):
    """

    :param input:
    :param db:
    :return:
    """
    seq_list = fasta_file_to_list(input)
    best_hits = []
    for seq in seq_list:
        tmp_seq_file = open('seq_tmp_file.fa', 'w+')
        tmp_seq_file.write(seq)
        best_hits.append(str(
            subprocess.check_output(["blastall -d " + db + " -i seq_tmp_file.fa -p blastx -m8 | head -n1"],
                                    shell=True), 'utf8'))
        # print(str(
        #     subprocess.check_output(["blastall -d " + db + " -i seq_tmp_file.fa -p blastx -m8 | head -n4"],
        #                             shell=True), 'utf8'))
    best_hits.pop(0)
    return best_hits


def make_db(File):
    """
    :param File:
    :return:
    """
    os.system("formatdb -i " + File + "  -p T")
    print(subprocess.check_output('ls', shell=True))


def system_input():
    """Deze funcite vangt alle variable op van de terminal als python hier in gedraaid word.
    Dit gebruert mer sys.arg. deze variabler zijn dan strings.


    :return: input_seq : serquentie van de dataset.
             protenome_ncbi: het bestand met het protenome van uit ncbi.
    """
    input_seq = sys.argv[0]
    protenome_ncbi = sys.argv[1]
    output_folder = sys.argv[2]
    return input_seq, protenome_ncbi, output_folder


def main():
    #input_seq, protenome_ncbi, output_folder = system_input()
    make_db(protenome_ncbi)
    best_ncbi_hits = blast_db_ncbi(input_seq, protenome_ncbi)
    gene_dictionary = make_dic_information_gene(best_ncbi_hits, protenome_ncbi)
    info_protien_en_meer(gene_dictionary)
    sort_info(output_folder)


main()
