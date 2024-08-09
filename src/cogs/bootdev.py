import discord
from discord.ext import commands
import pandas as pd
from src.functions.bootdevparse.Pokematch import Pokematch

class BootDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokematch(self, ctx):
        try:
            # Log the start of the command
            print("pokematch command started")

            # Instantiate the Pokematch class
            pokematch_instance = Pokematch()
            print("Pokematch instance created")

            # Execute the run method
            result = pokematch_instance.run()
            print("Pokematch run method executed")

            # Read the Pokemon CSV file
            df = pd.read_csv('BDparsed_with_pokemon.csv')
            print("CSV file read successfully")

            # Get the last 10 rows
            last_10_rows = df.tail(10)
            print("Last 10 rows extracted")

            # Send the last 10 rows as a message
            await ctx.send(last_10_rows.to_string(index=False))
            print("Message sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(BootDev(bot))