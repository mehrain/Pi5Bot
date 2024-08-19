import pypokedex, sqlite3, csv
from src.db.BDDB import BDDB

class Pokedex:
    def __init__(self):
        self.db = BDDB()

    # Grab the pokemon with the Archmage index
    def get(self, pokemon_id):
        print(f"Getting pokemon with Archmage index: {pokemon_id}")
        pokemon = pypokedex.get(dex=pokemon_id)
        print(f"Pokemon name: {pokemon.name}")
        return pokemon.name
    
    def append_pokemon(self):
        conn = sqlite3.connect(self.db.filepath)
        c = conn.cursor()
        
        c.execute("SELECT rowid, * FROM ArchmageArcanum WHERE Pokemon IS NULL")
        rows = c.fetchall()
        
        # # Write rows to a CSV file
        # with open('pokemon.csv', 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(['ID', 'Name'])  # Write header row
        #     for row in rows:
        #         writer.writerow(row)
        
        for index, row in enumerate(rows):
            pokemon_id = index + 1  # Assuming you want to assign Pokémon sequentially
            pokemon_name = self.get(pokemon_id)
            c.execute("UPDATE ArchmageArcanum SET Pokemon = ? WHERE rowid = ?", (pokemon_name, row[0]))
            print(f"Updated row {row[0]} with Pokemon {pokemon_name}")
        
        conn.commit()
        conn.close()