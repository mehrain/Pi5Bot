import discord, schedule, time, threading
from discord.ext import commands
from discord.commands import option
from src.functions.bootdevparse.BDparse import BDParser
from src.functions.bootdevparse.Pokeapi import Pokedex
from src.db.BDDB import BDDB

class BootDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #print ("BootDev cog initialized")

    @discord.slash_command(name="archrecent", description="Get the last n Archmages")
    @option("number", description="The number of Archmages to display", required=True, type=int)
    async def archrecent(self, ctx: discord.ApplicationContext, number: int):

        bddb = BDDB()
        
        if not number:
            await ctx.send("Please enter a number")
            return
        elif number <= 0:
            await ctx.send("Please enter a number greater than 0")
            return
        
        try:
            rows = bddb.get_recent_archmages(number)
            if not rows:
                await ctx.send("No data found")
                return
            
            total_characters = sum(len(str(row)) for row in rows)
            if total_characters > 6000:
                await ctx.send("The total number of characters exceeds the limit of 6000.")
                return

            # Send the last `number` rows as an embed message
            embed = discord.Embed(title=f"Last {number} Archmages", color=discord.Color.gold())
            for index, row in enumerate(rows):
                value = f"Name: {row[1]}\nUsername: {row[2]}\nDate: {row[3]}\nMatching Pokemon: {row[4]}"
                embed.add_field(name=f"Archmage rank: {row[0]}", value=value, inline=False)
            await ctx.send(embed=embed)
            print("Embed message sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred while sending the embed message. That sucks.")
            
    # @commands.command()
    # async def archlookup(self, ctx, what :str, value):
    #     pass
            
    @commands.slash_command(name='archsync', description='Sync the Archmage data')
    async def archsync(self, ctx):
        try:

            BDParser().start()
            Pokedex().append_pokemon()
            await ctx.send("Sync completed successfully")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred. That sucks.")
            
            
  
  # make the Pokematch run every hour          
    def start_scheduler(self):
        schedule.every().hour.do(self.run_autoupdate)
        thread = threading.Thread(target=self.run_scheduler)
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
    boot_dev_instance = BootDev(bot)
    boot_dev_instance.bddb = bddb  # Assign the BDDB instance to the cog
    bot.add_cog(boot_dev_instance)
    boot_dev_instance.start_scheduler()
    
    

