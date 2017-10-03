# Imports
import os
import subprocess
import importlib
import sys

"""Support check """
spam_loader = importlib.find_loader('bioservices')
if spam_loader is not None:
    import bioservices

    print('installed')
    FULL_SUPPORT = True
else:
    FULL_SUPPORT = False


# mag dit ?


# haal weg


def pathway_info(gene_name, seq_name, output_folder):
    """ Deze functie maakt gebruik van de bioservices modulen.

   Als deze geïnstalleerd is worden alle gegevens van het gen uit de KEGG database opgehaald.

   Dit wordt door middel van Bash naar het bestand van de sequentie geschreven.

   :param gene_name: naam van het gen

   :param seq_name: de naam van de originele sequentie

   """
    # is module installed ??
    if FULL_SUPPORT is True:
        name = gene_name
        keggapi = bioservices.KEGG()
        gene_info = keggapi.get('oaa:' + name)
        subprocess.call("echo  '" + str(gene_info) + '\n' + "'>>" + output_folder + "/" +
                        seq_name + ".txt", shell=True)
    else:
        pass


def sort_information(output_folder):
    """Dit is de functie voor het sorteren van alle gegevens uit de bestanden, hier worden dus alle tabellen gemaakt.

   22-9-2017: Er worden nu 3 bestanden aangemaakt: een debug/ alles bestand met alle huidige info, een bestand met een lijst van gencodes en -namen en een bestand met een lijst van eiwitcodes en -namen.

   """

    subprocess.call('bash bash_info_seq.sh ' + output_folder, shell=True)
    subprocess.call("cat info_seq.txt | awk '{ print $3 ,  substr($0,"
                    " index($0,$4))}' > 'eiwitcodes.txt'", shell=True)
    subprocess.call("bash list_of_genes.sh " + output_folder, shell=True)


def compress_files(cf_data_list, cf_folder, cf_seq):
    """


    :param cf_data_list:
    :param cf_folder:
    :param cf_seq:
    :return: None
    """
    with open(cf_folder + '/' + cf_seq + '.txt', 'w+') as output_file:
        for info in cf_data_list:
            output_file.write(''.join(str(i) for i in info))
            output_file.write('\n')
    subprocess.call('rm ' + cf_seq + '.txt ' + cf_seq + '_gene.txt ' +
                    cf_seq + '_mRNA.txt ', shell=True)


def get_online_info(goi_eiwit_lijst, goi_output_folder):
    """In deze functie wordt informatie van de NCBI database verkregen door middel van Bash.

   Vervolgens wordt alles per sequentie in een bestand geplaatst en kan er dus per sequentie informatie uit

   gehaald worden. Er wordt door de lijst met informatie die er is heen

   gelopen om zo de naam er uit te halen. Daarna wordt er in het Bash

   script getinfoandid.sh met wget informatie verkregen en vervolgens wordt dit in 3 bestanden gezet.

   Deze bestanden worden dan weer geopend en om alle informatie in een

   lijst te zetten. De lijst wordt meegegeven aan de functie compress_files()

   . Tenslotte wordt er met de functie pathway_info de informatie

   opgehaald uit KEGG.

   """

    for protien_info in goi_eiwit_lijst:
        name = protien_info[1][1]
        seq_name = str(protien_info[0])
        All_seq_info = []
        All_seq_info.append(protien_info)
        run = subprocess.check_output('bash getinfoandid.sh ' + name + ' ' +
                                      goi_output_folder + ' ' + seq_name,
                                      shell=True, stderr=None)
        with open(seq_name + ".txt", 'r') as main_file, \
                open(seq_name + "_gene.txt", 'r') as gene_file, open(
                    seq_name + "_mRNA.txt", 'r') as mRNA_file:
            All_seq_info.append(main_file.readlines())
            All_seq_info.append('\n')
            All_seq_info.append(gene_file.readlines())
            All_seq_info.append('\n')
            All_seq_info.append(mRNA_file.readlines())
            All_seq_info.append('\n')

        compress_files(All_seq_info, goi_output_folder, seq_name)
        pathway_info(str(subprocess.check_output("cat " + goi_output_folder + '/' +
                                                 seq_name + ".txt | grep '\<Gene-track_geneid\>' |tr '<'"
                                                            " '  ' |tr '>' ' ' | awk '{print $2}'",
                                                 shell=True), 'utf8'), seq_name, goi_output_folder)


def return_full_seq(rfs_naam, rfs_protenome_ncbi):
    """Deze functie haalt de hele sequentie uit het bestand rfs_protenome_ncbi.txt waar het

   protenoom instaat. Eerst wordt er gebruikmakend van Bash de index van het eiwit

   opgehaald. Daarna wordt het bestand geopend en wordt

   er vanaf de index van het gen heen gelopen tot

   dat er een nieuwe sequentie gevonden wordt, dit kan omdat bekend is dat elke

   sequentie begint met > in FASTA formaat. Wanneer een regel begint met >

   wordt de sequentie gereturned.

   :param rfs_naam: string: De naam van het eiwit wat gevonden is en

   de sequentie die nodig is.

   :param rfs_protenome_ncbi: bestand: FASTA bestand met proteoom erin.

   :return: str: sequentie van het eiwit wat gevraagd wordt.

   """
    all_protiens = []
    hit_protien_info = str(subprocess.check_output('egrep ' + rfs_naam + ' ' +
                                                   rfs_protenome_ncbi + '  -n',
                                                   shell=True), 'utf8')
    with open(rfs_protenome_ncbi, 'r') as protien_seq:
        all_protiens += (protien_seq.readlines())
        gen_seq_and_info = all_protiens[int(hit_protien_info
                                            .split(':')[0]) - 1]
        for lines in range(int(hit_protien_info.split(':')[0]),
                           len(all_protiens)):
            if all_protiens[lines][0] != '>':
                gen_seq_and_info += all_protiens[lines]
            else:
                return gen_seq_and_info


def make_dic_information_gene(hits_list, protenome_ncbi):   #TODO
    """Dict layout : key = name seq.| full hit, naam ncbi protien,

   leng, volle sequentie, informatie van ncbi wget stuff

   :param hits_list:

   :return:

   """
    gene_dict = []
    for hit in hits_list:
        gene_dict.append([hit.split('\t')[0],
                          [hit, hit.split('\t')[1], 'nan',
                           return_full_seq(hit.split('\t')[1],
                                           protenome_ncbi)]])
    return gene_dict


def fasta_file_to_list(ffl_file):
    """Loopt door een FASTA bestand heen en maakt hier een lijst van.

   Doordat een FASTA bestand alles achter elkaar neerzet is er een if/els statement nodig.

   Wanneer de regel begint met '>' verwijst dit naar het FASTA formaat. Deze regel wordt dan

   toegevoegd aan een tijdelijke string.

   Dan gaat de loop verder door de lijst van het bestand en elke keer als hij iets anders tegen komt dat

   niet met '>' begint wordt dit aan de tijdelijke string toegevoegd. Vervolgens wordt dit weer toegevoegd aan een lijst met alle sequenties en wordt de variabele leeggemaakt.

   Wanneer er door het hele bestand gelopen is wordt de lijst met gesorteerde FASTA gegevens terug gegeven.

   :param ffl_file: Bestand : een bestand in FASTA formaat waar sequenties in staan.

   :return: lijst: Hier zitten alle sequenties in met de bijbehorende naam.

   """
    ffl_list_of_seq = []
    with open(ffl_file, 'r') as ffl_local_file:
        temp_string = ''
        for i in ffl_local_file.readlines():
            if i[0] == '>':
                temp_string += i
            else:
                temp_string += i
                ffl_list_of_seq.append(temp_string)
                temp_string = ''
    return ffl_list_of_seq


def blast_db_ncbi(bdn_input, bdn_db):
    """Hier worden alle sequenties geBLAST tegen de gemaakte database.

   eerst word er met de funftie fasta_file_to_list() en lijst met

   sequenties gemaakt in fasta formaat. Door deze lisjt word dan heen

   gelopen en steeds een betand gemaakt met de serquentie er in.

   wanneer. met dit bestand word dan geblast met subpocess.

   check_output(). dan word de beste hit met head -n1 gepakt. de

   output word dan gestring in utf8 formaat. hierna word het aan een

   lijst toegevoegd en word de lijst terug gegeven aan de main functie

   .

   :param Betand : bdn_input: Het bestand met de sequenties die

   geblast worden.

   :param Bestand: bdn_db:De naam van het fasta bestan waar een db van

   is gemaakt.

   :return:

   """
    bdn_seq_list = fasta_file_to_list(bdn_input)
    bdn_best_hits = []
    for seq in bdn_seq_list:
        temp_seq_file = open('seq_tmp_file.fa', 'w+')
        temp_seq_file.write(seq)
        bdn_best_hits.append(str(
            subprocess.check_output(
                ["blastall -d " + bdn_db + " -i seq_tmp_file.fa -p blastx"
                                           " -m8 | head -n1"]
                , shell=True), 'utf8'))
    bdn_best_hits.pop(0)
    return bdn_best_hits


def make_db(md_file):
    """De functie make_db maakt een database bestand van een meegegeven bestand door middel van Bash.
   Dit gebreurd via os.System(). De functie heeft verder geen return of output.
   :param md_file: een proteoom bestand in FASTA formaat.
   """

    os.system("formatdb -i " + md_file + "  -p T")


def system_input():
    """Deze functie vangt alle variabelen op van de terminal als python hier in ge\
   draaid wordt. Dit gebeurt met sys.arg, deze variabelen worden opgeslagen als een strings en
   worden gereturned.
   :return: si_input_seq : sequentie van de dataset.
   si_protenome_ncbi: het bestand met het proteoom vanuit NCBI.
   """

    si_input_seq = sys.argv[1]
    si_protenome_ncbi = sys.argv[2]
    si_output_folder = sys.argv[3]
    print(si_input_seq, si_protenome_ncbi, si_output_folder)
    return si_input_seq, si_protenome_ncbi, si_output_folder


def main():
    """Dit is de main functie voor het programma. Stap voor stap worden de verschillende functies uitgevoerd in de volgorde zodat de input en ouput steeds klopt.
   Eerst worden de parameters van uit de terminal opgevangen en daarna wordt er een dn gemaakt van het proteoom uit NCBI.
   Wanneer er een db is gemaakt kan de blast worden gedaan met de sequentie verkregen uit de BioServer.

   :return:

   """


input_seq, protenome_ncbi, output_folder = system_input()
print(input_seq, protenome_ncbi, output_folder)
make_db(protenome_ncbi)
print('db done')
best_ncbi_hits = blast_db_ncbi(input_seq, protenome_ncbi)
print('blast done')
gene_dictionary = make_dic_information_gene(best_ncbi_hits, protenome_ncbi)
get_online_info(gene_dictionary, output_folder)
sort_information(output_folder)
print("\ndone\n\nFiles Made: \nresult_gen.txt\ninfo_seq.txt\
          \neiwitcodes.txt\n\nFolders:\n{}".format(output_folder))  # ToDO

main()

