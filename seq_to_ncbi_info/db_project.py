import psycopg2
import sys

# funcites voor de pathways tabel
"""script voor mike ze tabellen"""
import subprocess


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
        for i in lijnen[1:len(lijnen)]:
            listt = i.split(' ')
            if listt[0][0:3] == "oaa":
                new_list.append([lijnen[0], listt[0], ''.join(i + ' ' for i in listt[1: len(listt)])])
            else:
                new_list.append([lijnen[0], listt[1], ''.join(i + ' ' for i in listt[2: len(listt)])])
    return new_list


def write_to_file(clean_path):
    with open('clean_pathways.txt', 'w+') as file:
        for lines in clean_path:
            for i in lines:
                file.write(i)
                file.write('\t')
            file.write('\n')
    subprocess.call('cat clean_pathways.txt |sort | uniq>clean_pathway.txt; rm clean_pathways.txt', shell=True)


def make_patways_files():
    inhoud_bestand = open_en_split('pathway_table.txt')
    clean_path = clean_make_lists(inhoud_bestand)
    write_to_file(clean_path)


# einde van de funties

# begin db setting

def Setup():
    con = None
    ''' Zorg er voor dat je dbname, user en password aanpast naar jou gegevens en de python shell op fullscheern zet'''
    con = psycopg2.connect("host='localhost' dbname='project' user='root' password='password'")
    cur = con.cursor()
    return con, cur


def clean_up_db(con, cur):
    cur.execute("DROP TABLE IF EXISTS Info_seq CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Pathways CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Mrna CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_gene CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Alles CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Protien CASCADE;")


def Tabel_info_seq(con, cur):
    '''Het maken van de tabel Info_seq'''
    cur.execute("""CREATE TABLE Info_seq(
        Seq_id VARCHAR(150) PRIMARY KEY REFERENCES Alles (Seq_id),
        Orginale_seq VARCHAR(5000),
        Lengte INT)""")


def Tabel_Pathways(con, cur):
    '''Het maken van de tabel Pathways'''
    cur.execute("""CREATE TABLE Pathways(
        ID SERIAL PRIMARY KEY,
        Id_Pathway VARCHAR(500) ,
        Naam_Pathway VARCHAR(500),
        Info VARCHAR(500))""")


def Tabel_Mrna(con, cur):
    '''Het maken van de tabel Mrna'''
    cur.execute("""CREATE TABLE Mrna(
        Id_mrna VARCHAR(500) PRIMARY KEY,
        Lengte INT,
        Seq VARCHAR(8000))""")


def Tabel_Ncbi_gene(con, cur):
    '''Het maken van de tabel Ncbi_gene'''
    cur.execute("""CREATE TABLE Ncbi_gene(
        Id_gen VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR (150),
        Lengte INT,
        chromosom INT,
        Locatie VARCHAR(400),
        Seq VARCHAR(4000),
        exonen int,
        Protien VARCHAR(150))""")


def Tabel_Alles(con, cur):
    ### tabel ***Alles*** (heeft nog geen echte naam) ###
    '''Het maken van de tabel Alles'''
    cur.execute("""CREATE TABLE Alles(
        Seq_id VARCHAR(150) PRIMARY KEY,
        Ncbi_P_id VARCHAR(150),
        Ncbi_G_id VARCHAR(150),
        Ncbi_MR_id VARCHAR(150))""")


def Tabel_Protien(con, cur):
    '''Het maken van de tabel Protien'''
    cur.execute("""CREATE TABLE Protien(
        Id_protien VARCHAR(150) PRIMARY KEY,
        Name_Protien VARCHAR(150),
        EC_code VARCHAR(30),
        Lengte_Protien INT,
        Orginale_seq_AA VARCHAR(4000),
        Pathway VARCHAR(50))""")


def Keys(con, cur):
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_P_id) REFERENCES Protien(Id_protien)")
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_G_id) REFERENCES Ncbi_gene(Id_gen)")
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_MR_id) REFERENCES Mrna (Id_mrna)")
    cur.execute("ALTER TABLE Protien ADD FOREIGN KEY(Pathway) REFERENCES Pathways(Naam_Pathway)")
    cur.execute("ALTER TABLE Ncbi_gene ADD FOREIGN KEY(Protien) REFERENCES Protien(Id_protien)")


def Pathwyay_table(con, cur):
    org_table_sql = """
        INSERT INTO Pathways (Id_Pathway,Naam_Pathway,Info) VALUES (%s,%s,%s)"""

    f = open("clean_pathway.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(org_table_sql, data)
    con.commit()


def alles_table(con, cur):
    Alles_table_sql = """
    INSERT INTO Alles (Seq_id,Ncbi_P_id,Ncbi_G_id,Ncbi_MR_id) VALUES (%s,%s,%s,%s)"""
    f = open("alles_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(Alles_table_sql, data)
    con.commit()


def protien_table(con, cur):
    protien_table_sql = """
    INSERT INTO Protien VALUES (%s,%s,%s,%s,%s,%s)"""
    f = open("eiwit_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        print(data)
        data.append('oaa' +data[0])


        cur.execute(protien_table_sql, data)
    con.commit()


def Ncbi_gene_table(con, cur):
    Ncbi_gene_table = """
    INSERT INTO Ncbi_gene VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    f = open("ncbi_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data.pop(3)
        data = [None if x == 'NONE' or x=='Unknown' else x for x in data]

        cur.execute(Ncbi_gene_table, tuple(data))
    con.commit()


def Mrna_table(con, cur):
    Mrna_table = """
    INSERT INTO Mrna VALUES (%s,%s,%s)"""
    f = open("mrna_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else x for x in data]
        cur.execute(Mrna_table, data)
    con.commit()


def Info_seq_table(con, cur):
    org_info_sql = """
    INSERT INTO Info_seq VALUES (%s,%s,%s)"""
    f = open("org_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x == 'NONE' else str(x) for x in data]
        cur.execute(org_info_sql, tuple(data))
    con.commit()


def info_alles(con, cur):
    with open('info_seq.txt', 'r') as file:
        a = file.readlines()
        with open('alles_table_clean.txt', 'w') as outfile:
            for i in a:
                outfile.write(
                    i.split(' ')[0].split('/')[1] + '\t' + i.split(' ')[len(i.split(' ')) - 2] + '\t' + i.split(' ')[
                        2] + '\t' + i.split(' ')[len(i.split(' ')) - 1])


def main():
    make_patways_files()
    con, cur = Setup()  # TODO make een var of zo.
    print("connected")
    clean_up_db(con, cur)
    con.commit()

    # maken van tabels
    Tabel_Alles(con, cur)
    Tabel_info_seq(con, cur)
    Tabel_Protien(con, cur)
    Tabel_Pathways(con, cur)
    Tabel_Mrna(con, cur)
    Tabel_Ncbi_gene(con, cur)

    con.commit()
    print("Tabellen en Key's zijn gemaakt.")
    info_alles(con, cur)
    Pathwyay_table(con, cur)

    alles_table(con, cur)
    protien_table(con, cur)
    Ncbi_gene_table(con,cur)
    Mrna_table(con, cur)
    Info_seq_table(con,cur) #TypeError: argument 1 must be a string or unicode object
    # hier is het eind
    con.commit()
    con.close()


main()

