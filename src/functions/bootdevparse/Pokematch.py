import os
import csv
from BDparse import BDParser
from Pokeapi import Pokedex

class Pokematch:
    def __init__(self):
        self.pokedex = Pokedex()
        self.input_file = os.path.join(os.getcwd(), 'BDparsed.csv')
        self.output_file = os.path.join(os.getcwd(), 'BDparsed_with_pokemon.csv')

    def process_csv(self):
        with open(self.input_file, mode='r', newline='') as infile, open(self.output_file, mode='w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Read the header
            header = next(reader)
            header.append('Pokemon')
            writer.writerow(header)

            # Process each row
            for row in reader:
                rank = int(row[0])
                pokemon = self.pokedex.get(rank).name
                row.append(f"Pokemon based on rank: {pokemon}")
                writer.writerow(row)

        print(f"Updated CSV file with Pokémon saved to {self.output_file}")

    def run(self):
        BDParser.start()
        self.process_csv()


if __name__ == "__main__":
    pokematch = Pokematch()
    pokematch.run()
