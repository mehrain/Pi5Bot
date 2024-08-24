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
        
        c.execute("SELECT Rank FROM ArchmageArcanum WHERE Pokemon IS NULL")
        rows = c.fetchall()

        for _, row in enumerate(rows):
            rank = row[0]
            pokemon_id = rank
            pokemon_name = self.get(pokemon_id)
            c.execute("UPDATE ArchmageArcanum SET Pokemon = ? WHERE Rank = ?", (pokemon_name, rank))
            print(f"Updated row {rank} with Pokemon {pokemon_name}")
        
        conn.commit()
        conn.close()