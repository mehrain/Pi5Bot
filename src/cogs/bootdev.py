import discord, schedule, time, threading
from discord.ext import commands
import pandas as pd
from src.functions.bootdevparse.Pokematch import Pokematch

class BootDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #print ("BootDev cog initialized")

    @commands.command()
    async def arch10(self, ctx):
        try:
            # Read the Pokemon CSV file
            df = pd.read_csv('BDparsed_with_pokemon.csv')
            print("CSV file read successfully")

            # Get the last 10 rows
            last_10_rows = df.tail(10)
            print("Last 10 rows extracted")

            # Send the last 10 rows as an embed message
            embed = discord.Embed(title="Last 10 Archmages", color=discord.Color.gold())
            for index, row in last_10_rows.iterrows():
                embed.add_field(name=f"Archmage rank: {index+1}", value=row.to_string(index=False), inline=False)
            await ctx.send(embed=embed)
            print("Embed message sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred. That sucks.")
            
    @commands.command()
    async def archsync(self, ctx):
        try:
            # Log the start of the command
            print("pokematch command started")

            # Instantiate the Pokematch class
            pokematch_instance = Pokematch()
            print("Pokematch instance created")

            # Execute the run method
            result = pokematch_instance.run()
            print("Pokematch run method executed")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred. That sucks.")
            
  
  # make the Pokematch run every hour          
    def start_scheduler(self):
        schedule.every().hour.do(self.run_pokematch)
        thread = threading.Thread(target=self.run_scheduler)
        thread.start()
        print("Scheduler started")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_pokematch(self):
        try:
            print("Scheduled Pokematch run started")
            pokematch_instance = Pokematch()
            result = pokematch_instance.run()
            print("Scheduled Pokematch run executed")
        except Exception as e:
            print(f"An error occurred during scheduled run: {e}")

            
                  

def setup(bot):
    boot_dev_instance = BootDev(bot)
    bot.add_cog(boot_dev_instance)
    boot_dev_instance.start_scheduler()
    

