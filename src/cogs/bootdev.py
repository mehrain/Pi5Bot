import discord
import schedule
import time
import threading
from discord.ext import commands
from discord import option
from src.functions.bootdevparse.BDparse import BDParser
from src.functions.bootdevparse.Pokeapi import Pokedex
from src.db.BDDB import BDDB
from datetime import datetime

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
 
    @commands.slash_command(name="archsearch", description="Find an Archmage by Rank, Name, Username, Date, Pokemon")
    @option("search_field", description="Choose a search field", required=True, choices=[
        discord.OptionChoice(name="Rank", value="Rank"),
        discord.OptionChoice(name="Name", value="Name"),
        discord.OptionChoice(name="Username", value="Username"),
        discord.OptionChoice(name="Date", value="Date"),
        discord.OptionChoice(name="Pokemon", value="Pokemon")
    ])
    @option("search_value", description="Value to search for", required=True)
    async def archsearch(self, ctx, search_field: str, search_value: str):
        try:
            # Validate input based on search_field
            if search_field == "Rank":
                try:
                    search_value = int(search_value)
                except ValueError:
                    await ctx.respond("Error: Rank must be an integer.")
                    return
            elif search_field == "Date":
                try:
                    # Accept both M/D/YYYY and D/M/YYYY formats
                    datetime.strptime(search_value, "%m/%d/%Y")
                except ValueError:
                    try:
                        datetime.strptime(search_value, "%d/%m/%Y")
                    except ValueError:
                        await ctx.respond("Error: Invalid date format. Use M/D/YYYY or D/M/YYYY.")
                        return

            # Perform the search
            row = self.bddb.get_entry_by_column_value(search_field, search_value)
            
            if not row:
                await ctx.respond(f"No Archmage found for {search_field}: {search_value}")
                return

            # Unpack row data
            rank, name, username, date, pokemon = row

            # Validate returned data
            if not isinstance(rank, int):
                raise ValueError(f"Invalid Rank format in database: {rank}")
            if not isinstance(name, str):
                raise ValueError(f"Invalid Name format in database: {name}")
            if not isinstance(username, str) or not username.startswith("@"):
                raise ValueError(f"Invalid Username format in database: {username}")
            if not isinstance(date, str):
                raise ValueError(f"Invalid Date format in database: {date}")
            else:
                try:
                    # Try to parse the date in M/D/YYYY format
                    parsed_date = datetime.strptime(date, "%m/%d/%Y")
                    # Convert to YYYY-MM-DD format for consistency
                    date = parsed_date.strftime("%d/%m/%Y")
                except ValueError:
                    raise ValueError(f"Invalid Date format in database: {date}. Expected format: M/D/YYYY")
            if not isinstance(pokemon, str):
                raise ValueError(f"Invalid Pokemon format in database: {pokemon}")

            # Create and send embed
            value = f"Name: {name}\nUsername: {username}\nDate: {date}\nMatching Pokemon: {pokemon}"
            embed = discord.Embed(title="Archmage Found", color=discord.Color.gold())
            embed.add_field(name=f"Archmage rank: {rank}", value=value, inline=False)
            await ctx.respond(embed=embed)
            print("Embed message sent successfully")

        except ValueError as ve:
            error_message = f"Data validation error: {str(ve)}"
            print(error_message)
            await ctx.respond(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(error_message)
            await ctx.respond("An error occurred while processing your request. Please try again later.")

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