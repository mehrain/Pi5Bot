import pypokedex
from src.db.BDDB import BDDB

class Pokedex:
    def __init__(self):
        self.db = BDDB()
# Grab the pokemon with the Archmage index
    def get(self, pokemon_id):
        print(f"Getting pokemon with Archmage index: {pokemon_id}")
        pokemon = pypokedex.get(dex=pokemon_id)
        print(f"Pokemon name: {pokemon.name}")
        return pokemon
    
    