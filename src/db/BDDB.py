import sqlite3

class BDDB:

    def __init__ (self):
        self.filepath = "./src/db/bootdev.db"
        self.create_sqlite_database()
        self.create_table()
        
    
    
    def create_sqlite_database(self):
        """ create a database connection to an SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.filepath)
            print(f"SQLite version: {sqlite3.sqlite_version}")
        except sqlite3.Error as e:
            print(f"Error creating database: {e}")
        finally:
            if conn:
                conn.close()

    def create_table(self):
        conn = sqlite3.connect(self.filepath)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ArchmageArcanum
                    (Rank INT, Name TEXT, Username TEXT, Date TEXT, Score INT, Pokemon TEXT)''')
        conn.commit()
        conn.close()
        
    def insert_leaderboard(self, entries):
        
        conn = sqlite3.connect(self.filepath)
        c = conn.cursor()

        c.executemany("INSERT INTO ArchmageArcanum(Rank, Name, Username, Date) VALUES (?,?,?,?)", entries)
        conn.commit()
        conn.close()

    def get_recent_archmages(self, number: int = 5):
        conn = sqlite3.connect(self.filepath)
        c = conn.cursor()

        # Select the last `number` entries ordered by Rank in descending order
        result = c.execute("SELECT Rank, Name, Username, Date, Pokemon FROM ArchmageArcanum ORDER BY Rank DESC LIMIT ?", (number,))
        rows = result.fetchall()

        conn.close()

        return rows
    

if __name__ == '__main__':
    bddb = BDDB()
    print("Database and table created successfully.")