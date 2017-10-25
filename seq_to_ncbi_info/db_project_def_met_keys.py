import psycopg2
import sys
import subprocess


def open_en_split(file):
    """Deze funcite opend het bestand 'pathway_table.txt' en stopt alles van het bestand in een lijst.
       De inhoud van het bestand 'pathway_table.txt' bevat tab's ('\t'), daar wordt er gesplits zodat
       de inhoud gescheiden word.

       :param file: Dit is een txt bestand.
       :return: inhoud: Dit is een lijst met de inhoud die in het bestand 'pathway_table.txt' zit.
    """
    inhoud = []
    with open(file, 'r') as files:
        for i in files.readlines():
            inhoud.append(i.split('\t'))
    return inhoud


def clean_make_lists(data):
    """Deze funcite maakt een nieuwe lijst van de gereturnde lijst 'inhoud_bestand'. Dit word gedaan
       door middel van een for loop en de enters ('\n') te verwijderen. De lijst word vervolgens
       als variabele opgeslagen en gereturnd.

       :param data: Dit is de variable 'inhoud_bestand' die word doorgeven als de varaiable naam 'data'.
       :return: new_list: Dit is een lijst met de inhoud die in het bestand 'pathway_table.txt' zit.
    """
    new_list = []
    for lijnen in data:
        lijnen.remove('\n')
        for i in lijnen[1:len(lijnen)]:
            listt = i.split(' ')
            if listt[0][0:3] == "oaa":
                new_list.append([lijnen[0], listt[0], ''.join(i + ' ' for i in listt[1: len(listt)])])
            else:
                new_list.append([lijnen[0], listt[1], ''.join(i + ' ' for i in listt[2: len(listt)])])
    return new_list


def write_to_file(clean_path):
    """Deze funcite maakt gebruik van subprocess om de inhoud van het bestand 'clean_pathways.txt' te
       soteren zodat er alleen maar unieke waardes overblijven. Alle dubbele waardes worden er dus
       uitgehaald. Deze aanpasingen in het bestand 'clean_pathways.txt' worden bewaard in het bestand
       en de oude inhoud wordt overschreven.

       :param clean_path: Dit is een lijst met de inhoud die in het bestand 'pathway_table.txt' zit.
    """
    with open('clean_pathways.txt', 'w+') as file:
        for lines in clean_path:
            for i in lines:
                file.write(i)
                file.write('\t')
            file.write('\n')
    subprocess.call('cat clean_pathways.txt |sort | uniq>clean_pathway.txt; rm clean_pathways.txt', shell=True)


def make_patways_files():
    """Deze fucntie roept drie andere fucnties aan om de informatie van het bestand "pathway_table.txt"
       te filteren. Na dat de informatie uit "pathway_table.txt" is gehaald word er lijst gemaakt, deze
       lijst word nog gefilteerd en vervolgens als een bestand weg geschereven.
    """
    inhoud_bestand = open_en_split('pathway_table.txt')
    clean_path = clean_make_lists(inhoud_bestand)
    write_to_file(clean_path)


# einde van de funties

# begin db setting

def Setup():
    """Deze funcite zorgt er voor dat er ingelogt kan worden om conectie te maken met de database
       en dat er querry's uit gevoerd kunnen worden via de terminal.
       
       :return: con: Logit in op postgrespsql.
       :return: cur: Zorgt er voor dat de query uit gevoerd word.
    """
    con = None
    con = psycopg2.connect("host='localhost' dbname='project_perode_1' user='postgres_user' password='password'")
    cur = con.cursor()
    return con, cur


def clean_up_db(con, cur):
    """Deze fucntie maakt de bestaande tabellen leeg en verbreekt de connectie tussen de tabellen
       als ze die hebben. Als de tabellen niet bestaan treed er geen fout melding op en gaat het
       programma verder met runnen.

       :param con: Logit in op postgrespsql.
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    
    cur.execute("DROP TABLE IF EXISTS Sequentie_info CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Pathways CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Mrna CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_gene CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Seq_ncbi_combinatie CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Protien CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Protein CASCADE;")


def Tabel_info_seq(con, cur):
    """Het maken van de tabel Sequentie_info. In deze tabel is Seq_id de PRIMARY KEY die refereerd naar tabel
       Alles en het atribut Seq_id. Deze tabel zal bestaan uit drie kolomen: Seq_id, Orginale_seq en
       Lengte. De lengte is een INT en de andere twee een VARCHAR.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    
    cur.execute("""CREATE TABLE Sequentie_info(
        Seq_id VARCHAR(7) PRIMARY KEY REFERENCES Seq_ncbi_combinatie (Seq_id),
        Orginale_seq VARCHAR(8000),
        Lengte INT)""")


def Tabel_Pathways(con, cur):
    """Het maken van de tabel Pathways.In deze tabel is ID de PRIMARY KEY. Deze tabel zal uit vier
       kolomen bestaan: ID als een SERIAL en Id_Pathway, Naam_Pathway, Info als VARCHAR. ID is als
       SERIal een goeie PRIMARY KEY, omdat het steeds een nieuwe en unieke waarde toevoegt.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    
    cur.execute("""CREATE TABLE Pathways(
        ID SERIAL PRIMARY KEY,
        Id_pathway VARCHAR(50) ,
        Naam_Pathway VARCHAR(50),
        Info VARCHAR(500))""")


def Tabel_Mrna(con, cur):
    """Het maken van de tabel Mrna. In deze tabel is ncbi_id de PRIMARY KEY. Hier zullen
       drie kolomen worden gemaakt: ncbi_id en Seq als VARCHAR en Lengte als INT.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    
    cur.execute("""CREATE TABLE Mrna(
        ncbi_id VARCHAR(500) PRIMARY KEY,
        Lengte INT,
        Seq VARCHAR(8000))""")


def Tabel_Ncbi_gene(con, cur):
    """Het maken van de tabel Ncbi_gene. In deze tabel is NCBI_id_name_gene de PRIMARY KEY. Hier zullen
       acht kolomen worden gemaakt: Ncbi_id als VARCHAR, Naam als VARCHAR, Lengte als Int,
       Chromosom als Int, Locatie als VARCHAR, Seq als VARCHAR, Exonen als INT en tot slot Ncbi_protien_id
       als VARCHAR.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    
    cur.execute("""CREATE TABLE Ncbi_gene(
        Ncbi_id VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR (150),
        Lengte INT,
        Chromosom INT,
        Locatie VARCHAR(400),
        Seq VARCHAR(4000),
        Exonen INT,
        Ncbi_protein_id VARCHAR(150))""")


def Tabel_Alles(con, cur):
    """Het maken van de tabel Seq_ncbi_combinatie. In deze tabel is Seq_id de PRIMARY KEY. Hier zullen
       vier kolomen worden gemaakt: Seq_id, Ncbi_p_id, Ncbi_g_id en Ncbi_mr_id allemaal als
       VARCHAR.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """

    cur.execute("""CREATE TABLE Seq_ncbi_combinatie(
        Seq_id VARCHAR(7) PRIMARY KEY,
        Ncbi_g_id VARCHAR(150),   
        Ncbi_p_id VARCHAR(150),     
        Ncbi_mr_id VARCHAR(150))""")


def Tabel_Protein(con, cur):
    """Het maken van de tabel Protein.In deze tabel is NCBI_naam_id_Protien de PRIMARY KEY. Hier zullen
       zes kolomen worden gemaakt: NCBI_naam_id_Protien als VARCHAR, Naam_Protien als VARCHAR, EC_code
       als VARCHAR, Lengte_Protien als INT, Orginale_seq_aa als VARCHAR en Pathway als VARCHAR.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    cur.execute("""CREATE TABLE Protein(  
        ID_Protein SERIAL,
        Ncbi_id VARCHAR(150) PRIMARY KEY,
        Naam_Protein VARCHAR(150),
        EC_code VARCHAR(40),
        Lengte_Protein INT,
        Orginale_seq_aa VARCHAR(4000),
        Pathway VARCHAR(50))""")


def Keys(con, cur):
    """Deze fucntie voegt de FOREIGN KEY'S toe na dat de tabelen met de PRIMARY KEY zijn gemaakt.
       Hier worden de meeste FOREIGN KEY'S gemaakt van de atributen die in de tabel Alles zitten.
       Deze FOREIGN KEY'S verbinden de tabellen met elkaar.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uitgevoerd word.
    """
    cur.execute("ALTER TABLE Seq_ncbi_combinatie ADD FOREIGN KEY(Ncbi_g_id) REFERENCES Protein(Ncbi_id)")
    cur.execute("ALTER TABLE Seq_ncbi_combinatie ADD FOREIGN KEY(ncbi_p_id) REFERENCES Ncbi_gene(ncbi_id)")    
    cur.execute("ALTER TABLE Seq_ncbi_combinatie ADD FOREIGN KEY(Ncbi_mr_id) REFERENCES Mrna (ncbi_id)")
    cur.execute("ALTER TABLE Protein ADD FOREIGN KEY(ID_Protein) REFERENCES Pathways(ID)")
    cur.execute("ALTER TABLE Ncbi_gene ADD FOREIGN KEY(Ncbi_protein_id) REFERENCES Protein(Ncbi_id)")


def Pathwyay_table(con, cur):
    """Deze functie leest de het bestand "clean_pathway.txt". Uit dit bestand word er dankzij een
       forloop de inhoud gelezen en in de juiste kolomen gestopt. De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab word de informatie in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand "clean_pathway.txt" in kolom is
       ingedeeld.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    org_table_sql = """
        INSERT INTO Pathways (Id_Pathway,Naam_Pathway,Info) VALUES (%s,%s,%s)"""

    f = open("clean_pathway.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(org_table_sql, data)
    con.commit()


def alles_table(con, cur):
    """Deze functie leest de het bestand "alles_table_clean.txt". Uit dit bestand word er dankzij een
       forloop de inhoud gelezen en in de juiste kolomen gestopt. De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab word de informatie in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand "alles_table_clean.txt" in kolom is
       ingedeeld.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    Alles_table_sql = """
    INSERT INTO Seq_ncbi_combinatie (Seq_id,Ncbi_P_id,Ncbi_G_id,Ncbi_MR_id) VALUES (%s,%s,%s,%s)"""
    f = open("alles_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(Alles_table_sql, data)
    con.commit()


def protien_table(con, cur):
    """Deze functie leest de het bestand "eiwit_table_clean.txt". Uit dit bestand word er dankzij een
       forloop de inhoud gelezen en in de juiste kolomen gestopt. De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab word de informatie in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand "eiwit_table_clean.txt" in kolom is
       ingedeeld.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    protien_table_sql = """
    INSERT INTO Protein (Ncbi_id, Naam_Protein, EC_code, Lengte_Protein, Orginale_seq_aa,Pathway)
    VALUES (%s,%s,%s,%s,%s,%s)"""
    f = open("eiwit_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        data.append('oaa' +data[0])

        cur.execute(protien_table_sql, data)
    con.commit()


def Ncbi_gene_table(con, cur):
    """Deze functie leest de het bestand "ncbi_table_clean.txt". Uit dit bestand word er dankzij een
       forloop de inhoud gelezen en in de juiste kolomen gestopt. De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab word de informatie in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand "ncbi_table_clean.txt" in kolom is
       ingedeeld.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    ncbi_gene_table = """
    INSERT INTO Ncbi_gene VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    f = open("ncbi_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data.pop(3)
        data = [None if x == 'NONE' or x=='Unknown' else x for x in data]

        cur.execute(ncbi_gene_table, tuple(data))
    con.commit()


def Mrna_table(con, cur):
    """Deze functie leest de het bestand "mrna_table_clean.txt". Uit dit bestand word er dankzij een
       forloop de inhoud gelezen en in de juiste kolomen gestopt. De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab word de informatie in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand "mrna_table_clean.txt" in kolom is
       ingedeeld.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    Mrna_table = """
    INSERT INTO Mrna VALUES (%s,%s,%s)"""
    f = open("mrna_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(Mrna_table, data)
    con.commit()


def Info_seq_table(con, cur):
    """Deze functie leest de het bestand "org_table_clean.txt". Uit dit bestand word er dankzij een
       forloop de inhoud gelezen en in de juiste kolomen gestopt. De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab word de informatie in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand "org_table_clean.txt" in kolom is
       ingedeeld.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    org_info_sql = """
    INSERT INTO Sequentie_info VALUES (%s,%s,%s)"""
    f = open("org_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else str(x) for x in data]

        cur.execute(org_info_sql, tuple(data))
    con.commit()

def info_alles(con, cur):
    """Deze functie maakt het bestand 'alles_table_clean.txt'. Dit word gedaan door informatie uit
       het bestand 'info_seq.txt' te halen, doormiddel van een for loop. De informatie wordt in
       vier rijen gescheiden doormiddel van tab's ('\t'). Door tab's toe te voegen is het makkelijker
       om de informatie in de database te zetten.
       
       :param con: Logit in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd word.
    """
    with open('info_seq.txt', 'r') as file:
        a = file.readlines()
        with open('alles_table_clean.txt', 'w') as outfile:
            for i in a:
                outfile.write(
                    i.split(' ')[0].split('/')[1] + '\t' + i.split(' ')[len(i.split(' ')) - 2] + '\t' + i.split(' ')[
                        2] + '\t' + i.split(' ')[len(i.split(' ')) - 1])


def main():
    """Dit is de main fucntie voor het programma. Stap voor stap worden de
       verschillende functies uitgevoerd in deze volgorde waardoor er geen
       error's optreden en de KEY's gebonden zijn aan de juiste identifier.
       Pas na dat alle tabellen gemaat zijn word de informatie pas toe gevoegd.
       Als het progrma klaar is, zouden alle tabellen gevuld moeten zijn en is
       de database klaar voor gebruik.
    """
    make_patways_files()
    con, cur = Setup()  # TODO make een var of zo.
    print("connected")
    clean_up_db(con, cur)
    con.commit()

    # maken van tabels
    Tabel_Alles(con, cur)
    Tabel_info_seq(con, cur)
    Tabel_Protein(con, cur)
    Tabel_Pathways(con, cur)
    Tabel_Mrna(con, cur)
    Tabel_Ncbi_gene(con, cur)


    con.commit()
    print("Tabellen zijn gemaakt.")
    info_alles(con, cur)
    Pathwyay_table(con, cur)
    protien_table(con, cur)
    alles_table(con, cur)
    Ncbi_gene_table(con,cur)
    Mrna_table(con, cur)
    Info_seq_table(con,cur) #TypeError: argument 1 must be a string or unicode object
    print("Tabellen zijn gevuld.")
    Keys(con, cur) #FOREIGN Keys's werken nog niet moet nog naar gekeken worden.
    print('Alle KEYs zijn gevormd.''\n''Database is klaar voor gebruik!')
    # hier is het eind
    con.commit()
    con.close()


main()

