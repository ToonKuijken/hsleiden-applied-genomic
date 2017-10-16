import psycopg2
import sys


def Setup():  
    con = None
    ''' Zorg er voor dat je dbname, user en password aanpast naar jou gegevens en de python shell op fullscheern zet'''
    con = psycopg2.connect("host='localhost' dbname='project_perode_1' user='postgres_user' password='password'") 
    cur = con.cursor()
    return con, cur

def breken(con,cur):
    cur.execute("DROP TABLE IF EXISTS Info_seq CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Pathways CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Mrna CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_gene CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Alles CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Protien CASCADE;")

def Tabel_info_seq(con,cur):
    '''Het maken van de tabel Info_seq'''
    cur.execute("""CREATE TABLE Info_seq(
        Seq_id VARCHAR(150) PRIMARY KEY REFERENCES Alles (Seq_id_Alles),
        Lengte INT,
        Orginale_seq VARCHAR(500))""")

def Tabel_Pathways(con,cur):
    '''Het maken van de tabel Pathways'''
    cur.execute("""CREATE TABLE Pathways(
        Naam_Pathway VARCHAR(150) PRIMARY KEY,
        Info VARCHAR(150))""")

def Tabel_Mrna(con,cur):
    '''Het maken van de tabel Mrna'''
    cur.execute("""CREATE TABLE Mrna(
        NCBI_id_name VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR(150),
        Lengte INT,
        Seq VARCHAR(99999),
        Andere_dingen VARCHAR(99999))""")

def Tabel_Ncbi_gene(con,cur):
    '''Het maken van de tabel Ncbi_gene'''
    cur.execute("""CREATE TABLE Ncbi_gene(
        Ncbi_id_name_gene VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR (150),
        Lengte INT,
        Locatie VARCHAR(99999),
        Seq VARCHAR(99999),
        Splicing VARCHAR(99999),
        Protien VARCHAR(99999))""")


def Tabel_Alles(con,cur):
    ### tabel ***Alles*** (heeft nog geen echte naam) ###
    '''Het maken van de tabel Alles'''
    cur.execute("""CREATE TABLE Alles(
        Seq_id_Alles VARCHAR(150) PRIMARY KEY,
        Ncbi_P_id VARCHAR(150),
        Ncbi_G_id VARCHAR(150),
        Ncbi_MR_id VARCHAR(99999))""")

def Tabel_Protien(con,cur):
    '''Het maken van de tabel Protien'''
    cur.execute("""CREATE TABLE Protien(
        NCBI_naam_id_Protien VARCHAR(150) PRIMARY KEY,
        Naam_Protien VARCHAR(150),
        EC_code VARCHAR(30),
        Pathway VARCHAR(99999),
        Lengte_Protien INT,
        Orginale_seq_AA VARCHAR(500))""")  

def Keys(con,cur):
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_P_id) REFERENCES Protien(NCBI_naam_id_Protien)")
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_G_id) REFERENCES Ncbi_gene(Ncbi_id_name_gene)")
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_MR_id) REFERENCES Mrna (NCBI_id_name)")
    cur.execute("ALTER TABLE Protien ADD FOREIGN KEY(Pathway) REFERENCES Pathways(Naam_Pathway)")
    cur.execute("ALTER TABLE Ncbi_gene ADD FOREIGN KEY(Protien) REFERENCES Protien(NCBI_naam_id_Protien)")

def main():
    con,cur=Setup()
    print("connectit")
    breken(con,cur)
    con.commit()
    Tabel_Alles(con,cur)
    Tabel_info_seq(con,cur)
    Tabel_Protien(con,cur)
    Tabel_Pathways(con,cur)
    Tabel_Mrna(con,cur)
    Tabel_Ncbi_gene(con,cur)
    print("Tabellen en Key's zijn gemaakt.")
    #hier is het eind
    con.commit()
    con.close()

main()
