import discord
import schedule
import time
import threading
from discord.ext import commands
from discord import option
from src.functions.bootdevparse.BDparse import BDParser
from src.functions.bootdevparse.Pokeapi import Pokedex
from src.db.BDDB import BDDB

class BootDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bddb = BDDB()
        
    @commands.slash_command(name='archsync', description='Sync the Archmage data')
    async def archsync(self, ctx):
        await ctx.defer()
        try:
            BDParser().start()
            Pokedex().append_pokemon()
            await ctx.respond("Sync completed successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.respond("An error occurred. That sucks.")
            

    @commands.slash_command(name="archrecent", description="Get the last n Archmages")
    @option("number", description="The number of Archmages to display", required=True, type=int)
    async def archrecent(self, ctx: discord.ApplicationContext, number: int):
        if number <= 0:
            await ctx.respond("Please enter a number greater than 0")
            return
        try:
            rows = self.bddb.get_recent_archmages(number)
            if not rows:
                await ctx.respond("No data found")
                return
            total_characters = sum(len(str(row)) for row in rows)
            if total_characters > 6000:
                await ctx.respond("The total number of characters exceeds the limit of 6000.")
                return
            embed = discord.Embed(title=f"Last {number} Archmages", color=discord.Color.gold())
            for row in rows:
                value = f"Name: {row[1]}\nUsername: {row[2]}\nDate: {row[3]}\nMatching Pokemon: {row[4]}"
                embed.add_field(name=f"Archmage rank: {row[0]}", value=value, inline=False)
            await ctx.respond(embed=embed)
            print("Embed message sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.respond("An error occurred while sending the embed message. That sucks.")

     #todo this is gonna need a lot of error handling   
    @commands.slash_command(name="archsearch", description="Find an Archmage by Rank, Name, Username, Date, Pokemon")
    @option("search_field", description="Choose a search field", required=True, choices=[
        discord.OptionChoice(name="Rank", value="Rank"),
        discord.OptionChoice(name="Name", value="Name"),
        discord.OptionChoice(name="Username", value="Username"),
        discord.OptionChoice(name="Date", value="Date"),
        discord.OptionChoice(name="Pokemon", value="Pokemon")
    ])
    @option("search_value", description="Value to search for", required=True, type=int)
    async def archsearch(self, ctx, search_field: str, search_value: int):
        try:
            row = self.bddb.get_entry_by_column_value(search_field, search_value)
            if not row:
                await ctx.respond("No data found")
                return
            value = f"Name: {row[1]}\nUsername: {row[2]}\nDate: {row[3]}\nMatching Pokemon: {row[4]}"
            embed = discord.Embed(title=f"Archmage found", color=discord.Color.gold())
            embed.add_field(name=f"Archmage rank: {row[0]}", value=value, inline=False)
            await ctx.respond(embed=embed)
            print("Embed message sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.respond("An error occurred while sending the embed message. That sucks.")

    def start_scheduler(self):
        schedule.every(15).minutes.do(self.run_autoupdate)
        thread = threading.Thread(target=self.run_scheduler)
        thread.daemon = True
        thread.start()
        print("Scheduler started")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_autoupdate(self):
        try:
            print("Scheduled BDParser run started")
            BDParser().start()
            Pokedex().append_pokemon()
            print("Scheduled BDParser run executed")
        except Exception as e:
            print(f"An error occurred during scheduled run: {e}")

def setup(bot):
    bddb = BDDB()  # Create the BDDB instance
    cog = BootDev(bot)
    cog.bddb = bddb  # Assign the BDDB instance to the cog
    bot.add_cog(cog)
    cog.start_scheduler()  # Start the scheduler explicitly