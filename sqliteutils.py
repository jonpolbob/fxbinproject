import sqlite3

db_loc=None

def init():
    global db_loc
    db_loc = sqlite3.connect('Notes.db')
    #db_ram = sqlite3.connect(':memory:')


def uninit():
    global db_loc
    db_loc.close()
    db_loc = None

def inittables(listetables):
    global db_loc
    cursor = db_loc.cursor()

    # on regarde si la table existe
    lastring = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    # "SELECT table_name FROM information_schema.tables " #WHERE table_schema = 'databasename' AND table_name = "+nomtable
    resu = cursor.execute(lastring)
    toto = resu.fetchall()

    for latable in toto:
        lastring = "DROP TABLE " + latable[0]  # latable est un tuple
        cursor.execute(lastring)

    for table in listetables:
        nomtable = "tabl_"+table

        lastring = "CREATE TABLE "+nomtable+"( time INTEGER PRIMARY KEY,  date TEXT, open REAL, high REAL, low REAL, close REAL);"
        #print(lastring)
        cursor.execute(lastring)
        db_loc.commit()


def savecandle(table,time, date,candle):
    cursor = db_loc.cursor()
    nomtable = "tabl_" + table
    cursor.execute("INSERT INTO "+nomtable+" VALUES (?,?,?,?,?,?);", (time, date, candle[0], candle[1],candle[2],candle[3]) )


#test
init()
inittables(["auiusd","totot"])
savecandle("auiusd",100,"25/02:12:30",[100,110,90,105])

lastring = "SELECT * FROM tabl_auiusd;"
cursor = db_loc.cursor()
resu = cursor.execute(lastring)
toto = resu.fetchall()
print(toto)


