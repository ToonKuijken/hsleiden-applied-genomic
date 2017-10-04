import psycopg2
import sys
 
 
con = None
	
try:
    ''' Zorg er voor dat je dbname, user en password aanpast naar jou gegevens en de python shell op fullscheern zet'''
    con = psycopg2.connect("host='localhost' dbname='project_perode_1' user='postgres_user' password='password'") 
    cur = con.cursor()
    
    ### tabel info_seq ###
    '''Het maken van de tabel Info_seq'''
    cur.execute("DROP TABLE IF EXISTS Info_seq;")
    cur.execute("""CREATE TABLE Info_seq(
        seq_Id VARCHAR(150) PRIMARY KEY,
        Lengte INT,
        Orginale_seq VARCHAR(500))""")
    
    '''voegt iets toe aan de databse'''
    cur.execute("""INSERT INTO Info_seq VALUES(
        'Sed_id test',
        499,
        'Orginale_seq test')""")
        
    '''Het uitpriten van de database in python shell'''
    cur.execute("SELECT * FROM Info_seq;")
    con.commit()
    test=cur.fetchall()
    print('inhoud van Info_seq tabel:')
    for z in test:
        print('{:<20},{:<20},{:<20}'.format(z[0], z[1], z[2]))
    print('\n')
    ############

    ### tabel Protien ###
    ### forienkey moet nog toegewezen worden ###
    '''Het maken van de tabel Protien'''
    cur.execute("DROP TABLE IF EXISTS Protien;")
    cur.execute("""CREATE TABLE Protien(
        NCBI_naam_id VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR(150),
        EC_code VARCHAR(30),
        Patway VARCHAR(99999),
        Lengte INT,
        Orginale_seq_AA VARCHAR(500))""")

    '''voegt iets toe aan de databse'''
    cur.execute("""INSERT INTO Protien VALUES(
        'NCBI TEST',
        'NAAM TEST',
        'EC CODE TEST',
        'PATWAY TEST',
        500,
        'ladlkfadlal')""")

    '''Het uitpriten van de database in python shell'''
    cur.execute("SELECT * FROM Protien;")
    con.commit()
    test=cur.fetchall()
    print('inhoud van Protien tabel:')
    for z in test:
        print('{:<20},{:<20},{:<20},{:<20},{:<20},{:<20}'.format(z[0], z[1], z[2], z[3], z[4], z[5]))
    print('\n')
    ############

    ### tabel Patways ###
    '''Het maken van de tabel Patways'''
    cur.execute("DROP TABLE IF EXISTS Patways;")
    cur.execute("""CREATE TABLE Patways(
        Naam VARCHAR(150) PRIMARY KEY,
        Info VARCHAR(150),
        Moleculen VARCHAR(150),
        Link VARCHAR(99999),
        Patway VARCHAR(99999),
        Foto VARCHAR(50))""")

    '''voegt iets toe aan de databse'''
    cur.execute("""INSERT INTO Patways VALUES(
        'Naam TEST',
        'Info TEST',
        'Moleculen TEST',
        'Link TEST',
        'Patway Test',
        'Foto nog onbekend hoe')""")

    '''Het uitpriten van de database in python shell'''
    cur.execute("SELECT * FROM Patways;")
    con.commit()
    test=cur.fetchall()
    print('inhoud van Patways tabel:')
    for z in test:
        print('{:<20},{:<20},{:<20},{:<20},{:<20},{:<20}'.format(z[0], z[1], z[2], z[3], z[4], z[5]))
    print('\n')  
    ############

    ### tabel Mrna ###
    '''Het maken van de tabel Mrna'''
    cur.execute("DROP TABLE IF EXISTS Mrna;")
    cur.execute("""CREATE TABLE Mrna(
        Ncbi_id_name VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR(150),
        Lengte INT,
        Seq VARCHAR(99999),
        Andere_dingen VARCHAR(99999))""")

    '''voegt iets toe aan de databse'''
    cur.execute("""INSERT INTO Mrna VALUES(
        'Ncbi_id_name test',
        'Naam test',
        1246,
        'Seq test',
        'Anderere dingen test')""")

    '''Het uitpriten van de database in python shell'''
    cur.execute("SELECT * FROM Mrna;")
    con.commit()
    test=cur.fetchall()
    print('inhoud van Mrna tabel:')
    for z in test:
        print('{:<20},{:<20},{:<20},{:<20},{:<20}'.format(z[0], z[1], z[2], z[3], z[4]))
    print('\n')
    ############

    ### tabel Ncbi_gene
    '''Het maken van de tabel Ncbi_gene'''
    cur.execute("DROP TABLE IF EXISTS Ncbi_gene;")
    cur.execute("""CREATE TABLE Ncbi_gene(
        Ncbi_id_name VARCHAR(150) PRIMARY KEY,
        Naam VARCHAR(150),
        Lengte INT,
        Locatie VARCHAR(99999),
        Seq VARCHAR(99999),
        Splicing VARCHAR(99999),
        Protien VARCHAR(99999))""")

    '''voegt iets toe aan de databse'''
    cur.execute("""INSERT INTO Ncbi_gene VALUES(
        'Ncbi_id_name test',
        'Naam test',
        1246,
        'Locatie test',
        'Seq test',
        'Splicing test',
        'Protien test')""")

    '''Het uitpriten van de database in python shell'''
    cur.execute("SELECT * FROM Ncbi_gene;")
    con.commit()
    test=cur.fetchall()
    print('inhoud van Ncbi_gene tabel:')
    for z in test:
        print('{:<20},{:<20},{:<20},{:<20},{:<20},{:<20},{:<20}'.format(z[0], z[1], z[2], z[3], z[4], z[5],z[6]))
    print('\n')  
    ############

    ### tabel ***Alles*** (heeft nog geen echte naam) ###
    '''Het maken van de tabel Alles'''
    cur.execute("DROP TABLE IF EXISTS Alles;")
    cur.execute("""CREATE TABLE Alles(
        Seq_id VARCHAR(150) PRIMARY KEY,
        Ncbi_P_id VARCHAR(150),
        Ncbi_G_id VARCHAR(150),
        Ncbi_MR_id VARCHAR(99999))""")

    '''voegt iets toe aan de databse'''
    cur.execute("""INSERT INTO Alles VALUES(
        'Seq_id test',
        'Ncbi_P_id test',
        'Ncbi_G_id test',
        'Ncbi_MR_id test')""")

    '''Het uitpriten van de database in python shell'''
    cur.execute("SELECT * FROM Alles;")
    con.commit()
    test=cur.fetchall()
    print('inhoud van Alles tabel:')
    for z in test:
        print('{:<20},{:<20},{:<20},{:<20}'.format(z[0], z[1], z[2], z[3]))
    print('\n')  
    ############

    '''Print de error die in psql optreed als er iets verkeerds ging'''
except psycopg2.DatabaseError as e:
    if con:
        con.rollback()
 
    print ('Error %s' % e)    
    sys.exit(1)
 
finally:   
    if con:
        con.close()
        print('Tabellen zijn gemaakt, verder geen problemen gevonden.')



