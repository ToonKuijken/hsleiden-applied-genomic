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
        Orginale_seq VARCHAR(99999),
        Lengte INT)""")

def Tabel_Pathways(con,cur):
    '''Het maken van de tabel Pathways'''
    cur.execute("""CREATE TABLE Pathways(
        ID SERIAL PRIMARY KEY, 
        Id_Pathway VARCHAR(500) ,
        Naam_Pathway VARCHAR(500),        
        Info VARCHAR(500))""")

def Tabel_Mrna(con,cur):
    '''Het maken van de tabel Mrna'''
    cur.execute("""CREATE TABLE Mrna(
        NCBI_id_name VARCHAR(500) PRIMARY KEY,
        Lengte INT,
        Seq VARCHAR(99999))""")

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
        Lengte_Protien INT,
        Pathway VARCHAR(99999),
        Orginale_seq_AA VARCHAR(500))""")  

def Keys(con,cur):
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_P_id) REFERENCES Protien(NCBI_naam_id_Protien)")
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_G_id) REFERENCES Ncbi_gene(Ncbi_id_name_gene)")
    cur.execute("ALTER TABLE Alles ADD FOREIGN KEY(Ncbi_MR_id) REFERENCES Mrna (NCBI_id_name)")
    cur.execute("ALTER TABLE Protien ADD FOREIGN KEY(Pathway) REFERENCES Pathways(Naam_Pathway)")
    cur.execute("ALTER TABLE Ncbi_gene ADD FOREIGN KEY(Protien) REFERENCES Protien(NCBI_naam_id_Protien)")




def Pathwyay_table(con,cur):
        org_table_sql = """
        INSERT INTO Pathways (Id_Pathway,Naam_Pathway,Info) VALUES (%s,%s,%s)"""
        
        f = open("clean_pathway.txt", "r")
        for line in f.readlines():
        	data = line.strip().split('\t')
        	data = [None if x=='\\N' else x for x in data]
        	cur.execute(org_table_sql, data)
        con.commit()


def alles_table(con,cur):
    Alles_table_sql = """
    INSERT INTO Alles (Seq_id_Alles,Ncbi_P_id,Ncbi_G_id,Ncbi_MR_id) VALUES (%s,%s,%s,%s)"""
    f = open("alles_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x=='\\N' else x for x in data]
        cur.execute(Alles_table_sql, data)
    con.commit()

def protien_table(con,cur):
    protien_table_sql = """
    INSERT INTO Protien VALUES (%s,%s,%s,%s,%s)"""
    f = open("eiwit_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x=='\\N' else x for x in data]
        cur.execute(protien_table_sql, data)
    con.commit()

def Ncbi_gene_table(con,cur):
    Ncbi_gene_table = """
    INSERT INTO Ncbi_gene VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    f = open("ncbi_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x=='\\N' else x for x in data]
        cur.execute(Ncbi_gene_table, data)
    con.commit()

def Mrna_table(con,cur):
    Mrna_table = """
    INSERT INTO Mrna VALUES (%s,%s,%s)"""
    f = open("mrna_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x=='\\N' else x for x in data]
        cur.execute(Mrna_table, data)
    con.commit() 

def Info_seq_table(con,cur):
    Mrna_table = """
    INSERT INTO Info_seq VALUES (%s,%s,%s)"""
    f = open("org_table_clean.txt", "r")
    for line in f.readlines():
        data = line.strip().split('\t')
        data = [None if x=='\\N' else x for x in data]
        cur.execute(Info_seq_table, data)
    con.commit() 


def info_alles(con,cur):
    with open('org_table_clean.txt', 'r') as a, open('ncbi_table_clean.txt', 'r') as b, open('mrna_table_clean.txt','r') as c, open('eiwit_table_clean.txt','r') as d:
        #print(a.readlines())


        lezen=a.readlines()
        #print(lezen)
        alles=''
        regel=''
        index=[]
        for elke_regel in lezen:
             alles+=elke_regel
        #print(alles)
        for elk in alles:
            if elk is '\t' or elk is ' ' or elk is '\n' or elk is '':
                index.append(regel)
                regel=''
            else:
                regel+=elk
                #print(elk)
        #print(index)
        #print(len(index))
        teller=0
        org_table=[]
        
        for each in index:
            if each.find('seq') is 0:
                org_table.append(each)
        print(org_table)
        print(len(org_table))

        

        lezen=b.readlines()
        #print(lezen)
        alles=''
        regel=''
        index=[]
        for elke_regel in lezen:
             alles+=elke_regel
        #print(alles)
        for elk in alles:
            if elk is '\t' or elk is ' ' or elk is '\n' or elk is '':
                index.append(regel)
                regel=''
            else:
                regel+=elk
                #print(elk)
        #print(index)
        #print(len(index))
        teller=0
        NCBI_table=[]
        
        for each in index:
            if each.find('X') is 0:
                NCBI_table.append(each)
        print(NCBI_table)
        print(len(NCBI_table))

        lezen=c.readlines()
        #print(lezen)
        alles=''
        regel=''
        index=[]
        for elke_regel in lezen:
             alles+=elke_regel
        #print(alles)
        for elk in alles:
            if elk is '\t' or elk is ' ' or elk is '\n' or elk is '':
                index.append(regel)
                regel=''
            else:
                regel+=elk
                #print(elk)
        #print(index)
        #print(len(index))
        teller=0
        mrna_table=[]
        
        for each in index:
            if each.find('X') is 0:
                mrna_table.append(each)
        print(mrna_table)
        print(len(mrna_table))

        lezen=d.readlines()
        #print(lezen)
        alles=''
        regel=''
        index=[]
        for elke_regel in lezen:
             alles+=elke_regel
        #print(alles)
        for elk in alles:
            if elk is '\t' or elk is ' ' or elk is '\n' or elk is '':
                index.append(regel)
                regel=''
            else:
                regel+=elk
                #print(elk)
        #print(index)
        #print(len(index))
        teller=0
        eiwit_table=[]
        
        for each in index:
            if each.find('EC') is 0:
                eiwit_table.append(each)
        print(eiwit_table)
        print(len(eiwit_table))


        alles_table=''
        
        for waarde in range(len(org_table)):
            a=org_table[waarde]
            alles_table+=a
            alles_table+='\t'
            if waarde < 23:
                b=NCBI_table[waarde]
                alles_table+=b
                alles_table+='\t'
                c=mrna_table[waarde]
                alles_table+=c
                alles_table+='\t'
                d=eiwit_table[waarde]
                alles_table+=d
                alles_table+='\t'
            if waarde >22:    
                if len(NCBI_table) < waarde:
                    alles_table+= 'none''\t'
                elif len(NCBI_table) > waarde:
                    b=NCBI_table[waarde]
                    alles_table+=b
                    alles_table+='\t'
                alles_table+= 'none''\t'*2

                
        print(alles_table)
        with open('alles_table_clean.txt', 'w') as outfile:
            outfile.write(alles_table) 

    

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
    con.commit()
    print("Tabellen en Key's zijn gemaakt.")
    info_alles(con,cur)
    Pathwyay_table(con,cur)
    #alles_table(con,cur) #TypeError: not all arguments converted during string formatting
    protien_table(con,cur)
    #Ncbi_gene_table(con,cur) #TypeError: not all arguments converted during string formatting
    Mrna_table(con,cur)
    #Info_seq_table(con,cur) #TypeError: argument 1 must be a string or unicode object
    #hier is het eind
    con.commit()
    con.close()

main()
