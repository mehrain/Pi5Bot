import sqlite3

class BDDB:

    def __init__ (self):
        self.filepath = "./src/db/bootdev.db"
        
    
    
    def create_sqlite_database(self):
        """ create a database connection to an SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.filepath)
            print(sqlite3.sqlite_version)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    
    def create_table(self):
        conn = sqlite3.connect(self.filepath)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ArchmageArcanum
                    (Rank INT, Name TEXT, Username TEXT, Date TEXT)''')
        conn.commit()
        conn.close()
        
    def insert_leaderboard(self, entries):
        
        conn = sqlite3.connect(self.filepath)
        c = conn.cursor()

        c.executemany("INSERT INTO ArchmageArcanum(Rank, Name, Username, Date) VALUES (?,?,?,?)", entries)
        conn.commit()
        conn.close()

    def get_archmages(self):
        conn = sqlite3.connect(self.filepath)
        c = conn.cursor()

        result = c.execute("Select Rank, Name, Username, Date FROM ArchmageArcanum")
        rows = result.fetchall()

        for row in rows:
            print(row)

        conn.close()


if __name__ == '__main__':
    bddb = BDDB()

    bddb.get_archmages()
    # bddb.create_sqlite_database()
    # bddb.create_table()
    # # bddb.insert_leaderboard(
    # #     [
    # #         {'rank': 1, 'name': 'Ashley', 'username': '@AshGriffiths', 'date': '5/27/2023', 'pokemon': 'bulbasaur'},
    # #         {'rank': 2, 'name': 'Matthew', 'username': '@skovranek', 'date': '6/29/2023', 'pokemon': 'ivysaur'},
    # #         {'rank': 3, 'name': 'Theo', 'username': '@katomyomachia', 'date': '6/30/2023', 'pokemon': 'venusaur'},
    # #         {'rank': 4, 'name': 'Doo', 'username': '@doovel', 'date': '9/6/2023', 'pokemon': 'charmander'},
    # #         {'rank': 5, 'name': 'Maciej', 'username': '@icepick', 'date': '10/3/2023', 'pokemon': 'charmeleon'}
    # #     ]
    # # )
