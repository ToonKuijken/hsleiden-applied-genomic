from __future__ import division, print_function
import psycopg2


def main():
    doorgaan = True
    try:
        con_string = "host='localhost' dbname='bpapge' user='user' password='password'"
        con = psycopg2.connect(con_string)
        cur = con.cursor()
    except NameError:
        print("Er kan geen verbinding worden gemaakt met de database.")
        doorgaan = False
    if doorgaan:
        verwijder_inhoud_database(con, cur)
        print("De oude database is verwijderd als het aanwezig was.")
        creer_table_server(con, cur)
        print("De table server_sequentie is aangemaakt.")
        creer_table_seq_gene(con, cur)
        print("De table seq_gene is aangemaakt.")
        creer_table_ncbi_gene(con, cur)
        print("De table ncbi_gene is aangemaakt.")
        creer_table_gene_mrna(con, cur)
        print("De table gene_mrna is aangemaakt.")
        creer_table_ncbi_mrna(con, cur)
        print("De table ncbi_mrna is aangemaakt.")
        creer_table_prot_gen(con, cur)
        print("De table prot_gen is aangemaakt.")
        creer_table_ncbi_protein(con, cur)
        print("De table ncbi_gen is aangemaakt.")
        creer_table_prot_path(con, cur)
        print("De table prot_path is aangemaakt.")
        creer_table_pathway(con, cur)
        print("De table pathway is aangemaakt.")
        add_foreign_keys(con, cur)
        print("De foreign keys zijn toegevoegd.")
        print("De database is aangemaakt.")
    else:
        pass


def verwijder_inhoud_database(con, cur):
    cur.execute("DROP TABLE IF EXISTS Server_sequentie CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Seq_gene CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_gene CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Gene_mrna CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_mrna CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Prot_gen CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Ncbi_protein CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Prot_path CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Pathway CASCADE;")
    con.commit()


def creer_table_server(con, cur):
    sql = "CREATE TABLE Server_Sequentie(" \
          "seq_id serial PRIMARY KEY," \
          "org_seq text);"
    cur.execute(sql)
    con.commit()


def creer_table_seq_gene(con, cur):
    sql = "CREATE TABLE Seq_gene(" \
          "ncbi_g_id varchar(30)," \
          "seq_id int," \
          "PRIMARY KEY (ncbi_g_id, seq_id));"
    cur.execute(sql)
    con.commit()


def creer_table_ncbi_gene(con, cur):
    sql = "CREATE TABLE Ncbi_gene(" \
          "ncbi_g_id varchar(30) PRIMARY KEY," \
          "name text," \
          "length int," \
          "chromosome varchar(2)," \
          "location text," \
          "seq text," \
          "exons int);"
    cur.execute(sql)
    con.commit()


def creer_table_gene_mrna(con, cur):
    sql = "CREATE TABLE Gene_mrna(" \
          "ncbi_m_id varchar(30)," \
          "ncbi_g_id varchar(30)," \
          "PRIMARY KEY (ncbi_m_id, ncbi_g_id));"
    cur.execute(sql)
    con.commit()


def creer_table_ncbi_mrna(con, cur):
    sql = "CREATE TABLE Ncbi_mrna(" \
          "ncbi_m_id varchar(30) PRIMARY KEY," \
          "sequentie text);"
    cur.execute(sql)
    con.commit()


def creer_table_prot_gen(con, cur):
    sql = "CREATE TABLE Prot_gen(" \
          "ncbi_prot_id varchar(30)," \
          "ncbi_gene_id varchar(30)," \
          "PRIMARY KEY (ncbi_prot_id, ncbi_gene_id));"
    cur.execute(sql)
    con.commit()


def creer_table_ncbi_protein(con, cur):
    sql = "CREATE TABLE Ncbi_protein(" \
          "ncbi_id varchar(30) PRIMARY KEY," \
          "name_protein text," \
          "ec_code varchar(10)," \
          "lengte int," \
          "orginele_seq_aa text);"
    cur.execute(sql)
    con.commit()


def creer_table_prot_path(con, cur):
    sql = "CREATE TABLE Prot_path(" \
          "ncbi_id varchar(30)," \
          "pathway_id varchar(30)," \
          "PRIMARY KEY (ncbi_id, pathway_id));"
    cur.execute(sql)
    con.commit()


def creer_table_pathway(con, cur):
    sql = "CREATE TABLE Pathway(" \
          "pathway_id varchar(30) PRIMARY KEY," \
          "name_pathway text," \
          "info_pathway text);"
    cur.execute(sql)
    con.commit()


def add_foreign_keys(con, cur):
    cur.execute("ALTER TABLE Seq_gene ADD FOREIGN KEY (seq_id) REFERENCES Server_Sequentie(seq_id);")
    cur.execute("ALTER TABLE Seq_gene ADD FOREIGN KEY (ncbi_g_id) REFERENCES Ncbi_gene(ncbi_g_id);")
    cur.execute("ALTER TABLE Gene_mrna ADD FOREIGN KEY (ncbi_m_id) REFERENCES Ncbi_mrna(ncbi_m_id);")
    cur.execute("ALTER TABLE Gene_mrna ADD FOREIGN KEY (ncbi_g_id) REFERENCES Ncbi_gene(ncbi_g_id);")
    cur.execute("ALTER TABLE Prot_gen ADD FOREIGN KEY (ncbi_prot_id) REFERENCES Ncbi_protein(ncbi_id);")
    cur.execute("ALTER TABLE Prot_gen ADD FOREIGN KEY (ncbi_gene_id) REFERENCES Ncbi_gene(ncbi_g_id);")
    cur.execute("ALTER TABLE Prot_path ADD FOREIGN KEY (ncbi_id) REFERENCES Ncbi_protein(ncbi_id);")
    cur.execute("ALTER TABLE Prot_path ADD FOREIGN KEY (pathway_id) REFERENCES Pathway(pathway_id);")
    con.commit()


main()
