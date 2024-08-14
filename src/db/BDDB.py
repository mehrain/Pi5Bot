import sqlite3

class BDDB:
    def __init__(self):
        self.filepath = "./src/db/bootdev.db"
        self.create_sqlite_database()
        self.create_table()

    def create_sqlite_database(self):
        """ Create a database connection to an SQLite database """
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
        conn = None
        try:
            conn = sqlite3.connect(self.filepath)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS ArchmageArcanum
                         (Rank INTEGER, Name TEXT, Username TEXT, Date TEXT, Pokemon TEXT,
                         UNIQUE(Rank, Name, Username, Date))''')
            conn.commit()
            print("Table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            if conn:
                conn.close()

    def insert_leaderboard(self, entries):
        conn = None
        try:
            conn = sqlite3.connect(self.filepath)
            c = conn.cursor()
            c.executemany("""
                INSERT OR IGNORE INTO ArchmageArcanum(Rank, Name, Username, Date)
                VALUES (?,?,?,?)
            """, entries)
            conn.commit()
            print(f"Inserted {c.rowcount} new entries.")
        except sqlite3.Error as e:
            print(f"Error inserting leaderboard entries: {e}")
        finally:
            if conn:
                conn.close()

    def get_recent_archmages(self, number: int = 5):
        conn = None
        rows = []
        try:
            conn = sqlite3.connect(self.filepath)
            c = conn.cursor()
            result = c.execute("SELECT Rank, Name, Username, Date, Pokemon FROM ArchmageArcanum ORDER BY Rank DESC LIMIT ?", (number,))
            rows = result.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving recent archmages: {e}")
        finally:
            if conn:
                conn.close()
        return rows

if __name__ == '__main__':
    bddb = BDDB()
    print("Database and table created successfully.")