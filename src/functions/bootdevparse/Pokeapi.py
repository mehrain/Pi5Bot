import pypokedex

class Pokedex:
    def __init__(self):
        pass
# Grab the pokemon with the Archmage index
    def get(self, pokemon_id):
        print(f"Getting pokemon with Archmage index: {pokemon_id}")
        pokemon = pypokedex.get(dex=pokemon_id)
        print(f"Pokemon name: {pokemon.name}")
        return pokemon
    
# Pokedex().get(150)