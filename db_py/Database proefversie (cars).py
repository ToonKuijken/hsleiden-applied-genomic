import sqlite3
import sys

#############################################################################################
#####   Het aan maken van een database en het benoemen van de gevenens                 ######
#####   De db hoeft maar één keer gemaakt te worden, door try and except word          ######
#####   er geken of de database al bestaat. Bestaat de databes all dan komt er error.  ######
#####   de error word niet door geven dus het programma kan gewoon door werken         ######
#############################################################################################

test = sqlite3.connect('cars.db')
try:
    with test:        
        cur = test.cursor()    
        cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
        cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
        cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
        cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
        cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
        cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
        cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")
except:
    pass

#############################################################################################
#####   Het overzichtelijk printen van de gemaakte database.                            #####
#####   Later kan het ook in een tabel gezet worden, maar dat                           #####
#####   leren we pas in de vierde week.                                                 #####
#############################################################################################

test = sqlite3.connect('cars.db')            
with test:    
    cur = test.cursor()    
    cur.execute('SELECT * FROM Cars')    
    col_names = [cn[0] for cn in cur.description]    
    rows = cur.fetchall()    
    print ("%s %-10s %s" % (col_names[0], col_names[1], col_names[2]))
    for row in rows:    
        print ("%2s %-10s %s" % row)  

