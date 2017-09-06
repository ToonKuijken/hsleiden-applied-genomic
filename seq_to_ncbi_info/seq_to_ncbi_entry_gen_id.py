import os
import subprocess
import math
import sys
import  csv


"""Een tabel met voor elk gen in jullie dataset : De ID, de naam, lengte/sequentie, eiwit(ten) gecodeerd op het gen.
    Een tabel met voor elk eiwit in jullie dataset: De accession code, de naam,
     lengte/aminozuursequentie. Informatie over splicing varianten.
Annotatie van functie en pathway."""""

#input_seq = 'seq_a3.fa'
#proteome = "uniprot-proteome%3AUP000002279.fasta"
#ncbi_koppel_db = "GCF_000002275.2_Ornithorhynchus_anatinus_5.0.1_rna.fna"
#protenome_ncbi = 'db_files_ncbi/GCF_000002275.2_Ornithorhynchus_anatinus_5.0.1_protein.faa'
#outpute_name = 'ncbi_protien_info.txt'
#output_folder = 'sequence_info'

def info_protien_en_meer(protien_list, output_folder):
    """
    """
    for protien_info in protien_list:
        name = protien_info[1][1]
        All_seq_info = []
        All_seq_info.append(protien_info)
        print('bash getinfoandid.sh '+name + ' ' + output_folder)
        subprocess.call('bash getinfoandid.sh '+name + ' ' + output_folder, shell=True)
        with open(name+".txt", 'r') as main_file:
            All_seq_info.append(str(main_file.readlines()))
            pass
        with open(name + "_gene.txt", 'r') as gene_file:
            All_seq_info.append(str(gene_file.readlines()))

        with open(name + "_mRNA.txt", 'r') as mRNA_file:
            All_seq_info.append(str(mRNA_file.readlines()))

        with open(output_folder + '/'+ name+'.txt', 'w+') as output_file:
            for info in All_seq_info:
                print(info)
                output_file.write(''.join(str(i) for i in info))
                output_file.write('/n')
        subprocess.call('rm '+ name+'.txt '+ name+'_gene.txt '+ name+'_mRNA.txt ', shell= True)


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


def fasta_file_to_list(input_seq):
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


def blast_db_ncbi(input_file, db):
    """

    :param input:
    :param db:
    :return:
    """
    seq_list = fasta_file_to_list(input_file)
    best_hits = []
    for seq in seq_list:
        tmp_seq_file = open('seq_tmp_file.fa', 'w+')
        tmp_seq_file.write(seq)
        best_hits.append(str(
            subprocess.check_output(["blastall -d " + db + " -i seq_tmp_file.fa -p blastx -m8 | head -n1"],
                                    shell=True), 'utf8'))
    best_hits.pop(0)
    return best_hits


def make_db(File):
    """Deze funtie maakt een database van een bestand dat je mee geeft.
    Door subprocess.check_output()kan er in bash een command worden gegeven en gekeken wat de uitkomst is voor debugging opties.

    :param File: Een betand met
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
    input_seq = sys.argv[1]
    protenome_ncbi = sys.argv[2]
    output_folder = sys.argv[3]
    return input_seq, protenome_ncbi, output_folder


def main():
    """De main functie die alle stappen uitvoerd.
    Eerst worden de argumenten van de terminal opgevangen.
    Daarna word er een db gemaatk van het protenoom file.
    """
    input_seq, protenome_ncbi, output_folder = system_input()
    make_db(protenome_ncbi)
    best_ncbi_hits = blast_db_ncbi(input_seq, protenome_ncbi)
    gene_dictionary = make_dic_information_gene(best_ncbi_hits, protenome_ncbi)
    info_protien_en_meer(gene_dictionary, output_folder)
    #with open(outpute_name, 'w+') as output:
     #   for key in gene_dictionary:
      #      print(key)
       #     output.write(
        #        'Orginial seq:' + key[0] + '\nHit:' + key[1][0] + 'ncbi id:' + key[1][1] + '\n' + key[1][3] + '\n')


main()
