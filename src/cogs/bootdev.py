import discord
from discord.ext import commands
import pandas as pd
from src.functions.bootdevparse.BDparse import BDParser
from src.functions.bootdevparse.Pokematch import Pokematch

class BootDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokematch(self, ctx):
        # Execute the pokematch function
        result = Pokematch()

        # Read the Pokemon CSV file
        df = pd.read_csv('pokemon.csv')

        # Get the last 10 rows
        last_10_rows = df.tail(10)

        # Send the last 10 rows as a message
        await ctx.send(last_10_rows.to_string(index=False))

def setup(bot):
    bot.add_cog(BootDev(bot))