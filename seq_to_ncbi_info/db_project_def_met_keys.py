import psycopg2
import sys
import subprocess


def open_and_split(file):
    """Deze functie opent het bestand 'pathway_table.txt' en stopt
    alles van het bestand in een lijst.
       De inhoud van het bestand 'pathway_table.txt' bevat tab's ('\t')
       , vervolgens wordt daarop gesplits zodat
       de inhoud gescheiden wordt.
       :param file: Dit is een txt bestand.
       :return: inhoud: Dit is een lijst met de inhoud die in het
        bestand 'pathway_table.txt' zit.
    """
    inhoud = []
    with open(file, 'r') as files:
        for i in files.readlines():
            inhoud.append(i.split('\t'))
    return inhoud


def clean_make_lists(data):
    """Deze functie maakt een nieuwe lijst van de gereturnde lijst
     'inhoud_bestand'. Dit wordt gedaan
           door middel van een for loop en door de enters ('\n')
           te verwijderen. De lijst wordt vervolgens
           als variabele opgeslagen en gereturnd.
           :param data: Dit is de variable 'inhoud_bestand' die wordt
           doorgeven als de variable name 'data'.
           :return: new_list: Dit is een lijst met de inhoud die in het
            bestand 'pathway_table.txt' zit.
        """
    new_list = []
    for lijnen in data:
        lijnen.remove('\n')
        for i in lijnen[1:len(lijnen)]:
            listt = i.split(' ')
            if listt[0][0:3] == "oaa":
                new_list.append([lijnen[0], listt[0], ''.join(
                    i + ' ' for i in listt[1: len(listt)])])
            else:
                new_list.append([lijnen[0], listt[1], ''.join(
                    i + ' ' for i in listt[2: len(listt)])])
    return new_list


def write_to_file(clean_path):
    """Deze functie maakt gebruik van subprocess om de inhoud van het
     bestand 'clean_pathways.txt' te
          sorteren zodat er alleen maar unieke waardes overblijven.
           Alle dubbele waardes worden er dus
          uitgehaald. Deze aanpassingen in het bestand
           'clean_pathways.txt' worden bewaard in het bestand
          en de oude inhoud wordt overschreven.
          :param clean_path: Dit is een lijst met de inhoud die in het
           bestand 'pathway_table.txt' zit.
       """
    with open('clean_pathways.txt', 'w+') as file:
        for lines in clean_path:
            for i in lines:
                file.write(i)
                file.write('\t')
            file.write('\n')
    subprocess.call(
        'cat clean_pathways.txt |sort |'
        ' uniq>clean_pathway.txt; rm clean_pathways.txt',
        shell=True)


def make_patways_files():
    """Deze functie roept drie andere functies aan om de informatie
    van het bestand "pathway_table.txt"
       te filteren. Nadat de informatie uit "pathway_table.txt" is
       gehaald wordt er een lijst gemaakt, deze
       lijst wordt nog gefilteerd en vervolgens als een bestand
       weggeschereven.
    """
    inhoud_bestand = open_and_split('pathway_table.txt')
    clean_path = clean_make_lists(inhoud_bestand)
    write_to_file(clean_path)


def Setup(host, db, user, password):
    """Deze functie zorgt ervoor dat er ingelogt kan worden om
    conectie te maken met de database
        en dat er querry's uitgevoerd kunnen worden via de terminal.
        :return: con: Logt in op postgrespsql.
        :return: cur: Zorgt ervoor dat de query uitgevoerd wordt.
     """
    con = None
    con = psycopg2.connect(
        "host='{}' dbname='{}' user='{}' password='{}'".format(host, db, user,
                                                               password))
    cur = con.cursor()
    return con, cur


def clean_up_db(con, cur):
    """Deze functie maakt de bestaande tabellen leeg en verbreekt
    de connectie tussen de tabellen
       wanneer ze ee connectie hebben. Als de tabellen niet bestaan
        treed er geen fout melding op en gaat het
       programma verder met runnen.
       :param con: Logt in op postgrespsql.
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """

    cur.execute("DROP TABLE IF EXISTS sequence_info CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Pathways CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Mrna CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_gene CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Seq_ncbi_combination CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Protein CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_Protein CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_Mrna CASCADE;")


def Table_info_seq(con, cur):
    """Het maken van de tabel sequence_info. In deze tabel is Seq_id
     de PRIMARY KEY die refereerd naar tabel
           Alles en het atribut Seq_id. Deze tabel zal bestaan uit drie
            kolomen: Seq_id, Orginale_seq en
           Length. De lengte is een INT en de andere twee een VARCHAR.
           :param con: Logt in op postgrespsql
           :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
        """

    cur.execute("""CREATE TABLE sequence_info(
        Seq_id VARCHAR(7) PRIMARY KEY REFERENCES Seq_ncbi_combination (Seq_id),
        Org_seq VARCHAR(8000),
        Length INT)""")


def Table_Pathways(con, cur):
    """Het maken van de tabel Pathways. In deze tabel is ID de PRIMARY
    KEY. Deze tabel zal uit vier
       kolomen bestaan: ID als een SERIAL en Id_Pathway, name_Pathway,
       Info als VARCHAR. ID is als
       SERIAl een goede PRIMARY KEY, omdat het steeds een nieuwe en
       unieke waarde toevoegt.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """

    cur.execute("""CREATE TABLE Pathways(
        id SERIAL PRIMARY KEY,
        Id_pathway VARCHAR(50) ,
        Name_Pathway VARCHAR(50),
        Info_pathway VARCHAR(500))""")


def Table_Mrna(con, cur):
    """Het maken van de tabel Ncbi_Mrna. In deze tabel is ncbi_id de
     PRIMARY KEY. Hier zullen
       drie kolomen worden gemaakt: ncbi_id en Seq als VARCHAR en
        Length als INT.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """

    cur.execute("""CREATE TABLE Ncbi_Mrna(
        ncbi_id VARCHAR(500) PRIMARY KEY,
        Length INT,
        Seq VARCHAR(8000))""")


def Table_Ncbi_gene(con, cur):
    """Het maken van de tabel Ncbi_gene. In deze tabel is
    NCBI_id_name_gene de PRIMARY KEY. Hier zullen
       acht kolomen worden gemaakt: Ncbi_id als VARCHAR, name als
        VARCHAR, Length als INT,
       Chromosoom als INT, Locatie als VARCHAR, Seq als VARCHAR,
       Exonen als INT en tot slot Ncbi_protien_id
       als VARCHAR.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """

    cur.execute("""CREATE TABLE Ncbi_gene(
        Ncbi_id VARCHAR(150) PRIMARY KEY,
        Name VARCHAR (150),
        Length INT,
        Chromosome INT,
        Location VARCHAR(400),
        Seq VARCHAR(4000),
        Exons INT,
        Ncbi_protein_id VARCHAR(150))""")


def Table__all(con, cur):
    """Het maken van de tabel Seq_ncbi_combination. In deze tabel
     is Seq_id de PRIMARY KEY. Hier zullen
       vier kolomen worden gemaakt: Seq_id, Ncbi_p_id, Ncbi_g_id
        en Ncbi_mr_id allemaal als
       VARCHAR.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """

    cur.execute("""CREATE TABLE Seq_ncbi_combination(
        Seq_id VARCHAR(7) PRIMARY KEY,
        Ncbi_g_id VARCHAR(150),
        Ncbi_p_id VARCHAR(150),
        Ncbi_mr_id VARCHAR(150))""")


def Table_Protein(con, cur):
    """Het maken van de tabel Ncbi_Protein. In deze tabel is
    NCBI_name_id_Protein de PRIMARY KEY. Hier zullen
        zes kolomen worden gemaakt: NCBI_name_id_Protein als VARCHAR,
        name_Protein als VARCHAR, EC_code
        als VARCHAR, Length_Protein als INT, Orginale_seq_aa als
        VARCHAR en Pathway als VARCHAR.
        :param con: Logt in op postgrespsql
        :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
     """
    cur.execute("""CREATE TABLE Ncbi_Protein(
        Ncbi_id VARCHAR(150) PRIMARY KEY,
        ID_Protein SERIAL,
        Name_Protein VARCHAR(150),
        EC_code VARCHAR(40),
        Length INT,
        originele_seq_aa VARCHAR(4000),
        Pathway VARCHAR(50))""")


def Keys(con, cur):
    """Deze functie voegt de FOREIGN KEY'S toe na dat de tabelen
    met de PRIMARY KEY zijn gemaakt.
       Hier worden de meeste FOREIGN KEY'S gemaakt van de atributen
       die in de tabel Alles zitten.
       Deze FOREIGN KEY'S verbinden de tabellen met elkaar.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """
    cur.execute(
        "ALTER TABLE Seq_ncbi_combination ADD FOREIGN KEY(Ncbi_g_id)"
        " REFERENCES Ncbi_gene(ncbi_id)")
    cur.execute(
        "ALTER TABLE Seq_ncbi_combination ADD FOREIGN KEY(ncbi_p_id) "
        "REFERENCES  Ncbi_Protein(Ncbi_id)")
    cur.execute(
        "ALTER TABLE Seq_ncbi_combination ADD FOREIGN KEY(Ncbi_mr_id)"
        " REFERENCES Ncbi_Mrna (ncbi_id)")
    cur.execute(
        "ALTER TABLE Ncbi_Protein ADD FOREIGN KEY(ID_Protein)"
        " REFERENCES Pathways(ID)")
    cur.execute(
        "ALTER TABLE Ncbi_gene ADD FOREIGN KEY(Ncbi_protein_id)"
        " REFERENCES Ncbi_Protein(Ncbi_id)")
    cur.execute(
        "ALTER TABLE sequence_info ADD FOREIGN KEY(Seq_id)"
        " REFERENCES Seq_ncbi_combination(Seq_id)")


def Pathwyay_table(con, cur):
    """Deze functie leest de het bestand "clean_pathway.txt". Uit dit
     bestand wordt er dankzij een
       for loop de inhoud gelezen en in de juiste kolomen gestopt.
       De manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's
        ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab wordt de informatie
       in een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand
       "clean_pathway.txt" in kolom is
       ingedeeld.

       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """
    org_table_sql = """
        INSERT INTO Pathways (Id_Pathway,name_Pathway,Info_Pathway) VALUES (%s,%s,%s)"""

    f = open("clean_pathway.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(org_table_sql, data)
    con.commit()


def all_table(con, cur):
    """Deze functie leest de het bestand "alles_table_clean.txt". Uit dit
     bestand wordt er dankzij een
       for loop de inhoud gelezen en in de juiste kolomen gestopt. De
       manier waarop de inhoud in de
       juiste kolom terecht komt is door gebruik te maken van tab's
        ('\t'). In het bestand staat de
       inhoud gescheiden in tab's, na elke tab wordt de informatie in
        een andere kolom gezet. Dit
       proces herhaald zich tot dat alle inhoud uit het bestand
        "alles_table_clean.txt" in kolom is
       ingedeeld.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt er voor dat de query uit gevoerd wordt.
    """
    Alles_table_sql = """
    INSERT INTO Seq_ncbi_combination (Seq_id,Ncbi_P_id,Ncbi_G_id,
    Ncbi_MR_id) VALUES (%s,%s,%s,%s)"""
    f = open("alles_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(Alles_table_sql, data)
    con.commit()


def protein_table(con, cur):
    """Deze functie leest de het bestand "eiwit_table_clean.txt".
    Uit dit bestand wordt er dankzij een
        for loop de inhoud gelezen en in de juiste kolomen gestopt.
        De manier waarop de inhoud in de
        juiste kolom terecht komt is door gebruik te maken van tab's
         ('\t'). In het bestand staat de
        inhoud gescheiden in tab's, na elke tab wordt de informatie
        in een andere kolom gezet. Dit
        proces herhaald zich tot dat alle inhoud uit het bestand
        "eiwit_table_clean.txt" in kolom is
        ingedeeld.
        :param con: Logt in op postgrespsql
        :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
     """
    protien_table_sql = """
    INSERT INTO Ncbi_Protein (Ncbi_id, Name_Protein, EC_code,
     Length, Original_seq_aa,Pathway)
    VALUES (%s,%s,%s,%s,%s,%s)"""
    f = open("eiwit_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        data.append('oaa' + data[0])

        cur.execute(protien_table_sql, data)
    con.commit()


def Ncbi_gene_table(con, cur):
    """Deze functie leest de het bestand "ncbi_table_clean.txt".
    Uit dit bestand wordt er dankzij een
        for loop de inhoud gelezen en in de juiste kolomen gestopt.
         De manier waarop de inhoud in de
        juiste kolom terecht komt is door gebruik te maken van tab's
         ('\t'). In het bestand staat de
        inhoud gescheiden in tab's, na elke tab wordt de informatie
        in een andere kolom gezet. Dit
        proces herhaald zich tot dat alle inhoud uit het bestand
        "ncbi_table_clean.txt" in kolom is
        ingedeeld.
        :param con: Logt in op postgrespsql
        :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
     """
    ncbi_gene_table = """
    INSERT INTO Ncbi_gene VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    f = open("ncbi_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data.pop(3)
        data = [None if x == 'NONE' or x == 'Unknown' else x for x in data]

        cur.execute(ncbi_gene_table, tuple(data))
    con.commit()


def Mrna_table(con, cur):
    """Deze functie leest de het bestand "mrna_table_clean.txt". Uit
    dit bestand wordt er dankzij een
        for loop de inhoud gelezen en in de juiste kolomen gestopt.
        De manier waarop de inhoud in de
        juiste kolom terecht komt is door gebruik te maken van tab's
         ('\t'). In het bestand staat de
        inhoud gescheiden in tab's, na elke tab wordt de informatie
        in een andere kolom gezet. Dit
        proces herhaald zich tot dat alle inhoud uit het bestand "
        mrna_table_clean.txt" in kolom is
        ingedeeld.

        :param con: Logt in op postgrespsql
        :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
     """
    Mrna_table = """
    INSERT INTO Ncbi_Mrna VALUES (%s,%s,%s)"""
    f = open("mrna_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(Mrna_table, data)
    con.commit()


def Info_seq_table(con, cur):
    """Deze functie leest de het bestand "org_table_clean.txt". Uit
    dit bestand wordt er dankzij een
        for loop de inhoud gelezen en in de juiste kolomen gestopt.
        De manier waarop de inhoud in de
        juiste kolom terecht komt is door gebruik te maken van tab's
         ('\t'). In het bestand staat de
        inhoud gescheiden in tab's, na elke tab wordt de informatie
        in een andere kolom gezet. Dit
        proces herhaald zich tot dat alle inhoud uit het bestand
        "org_table_clean.txt" in kolom is
        ingedeeld.
        :param con: Logt in op postgrespsql
        :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
     """
    org_info_sql = """
    INSERT INTO sequence_info VALUES (%s,%s,%s)"""
    f = open("org_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else str(x) for x in data]
        cur.execute(org_info_sql, tuple(data))
    con.commit()


def info_all(con, cur):
    """Deze functie maakt het bestand 'alles_table_clean.txt'.
     Dit wordt gedaan door informatie uit
       het bestand 'info_seq.txt' te halen, doormiddel van een for
       loop. De informatie wordt in
       vier rijen gescheiden doormiddel van tab's ('\t'). Door tab's
        toe te voegen is het makkelijker
       om de informatie in de database te zetten.
       :param con: Logt in op postgrespsql
       :param cur: Zorgt ervoor dat de query uitgevoerd wordt.
    """
    with open('info_seq.txt', 'r') as file:
        a = file.readlines()
        with open('alles_table_clean.txt', 'w') as outfile:
            for i in a:
                outfile.write(
                    i.split(' ')[0].split('/')[1] + '\t' + i.split(' ')[
                        2] + '\t' + i.split(' ')[len(i.split(' ')) - 2] + '\t' +
                    i.split(' ')[len(i.split(' ')) - 1])


def get_parameters():
    """Deze functie zorgt voor de parameters die op worden gegeven.
       Hiermee kan de database worden gekozen, het wachtwoord van de
        gebuiker en de user."""
    host = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    return host, db, user, password


def main():
    """Dit is de main functie voor het programma. Stap voor stap worden
     de verschillende functies uitgevoerd in de goede volgorde waardoor
     er geen
        error's optreden en de KEY's gebonden zijn aan de juiste
        identifier.
        Pas nadat alle tabellen gemaakt zijn wordt de informatie
        pas toegevoegd.
        Als het programma klaar is, zouden alle tabellen gevuld
         moeten zijn en is
        de database klaar voor gebruik.
     """
    make_patways_files()
    try:
        host, db, user, password = get_parameters()
    except IndexError:
        print('no db values')
        host = 'localhost'
        db = 'project'
        user = 'user'
        password = 'password'
        print('using defaults')

    con, cur = Setup(host, db, user, password)
    print("connected")
    clean_up_db(con, cur)
    con.commit()

    # Maken van tabellen
    Table__all(con, cur)
    Table_info_seq(con, cur)
    Table_Protein(con, cur)
    Table_Pathways(con, cur)
    Table_Mrna(con, cur)
    Table_Ncbi_gene(con, cur)

    con.commit()
    print("Tabellen zijn gemaakt.")
    info_all(con, cur)
    Pathwyay_table(con, cur)
    protein_table(con, cur)
    all_table(con, cur)
    Ncbi_gene_table(con, cur)
    Mrna_table(con, cur)
    Info_seq_table(con, cur)
    print("Tabellen zijn gevuld.")
    Keys(con, cur)
    print('Alle KEYs zijn gevormd.''\n''Database is klaar voor gebruik!')
    # Hier is het eind
    con.commit()
    con.close()


main()
