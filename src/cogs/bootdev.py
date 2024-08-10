import discord, schedule, time, threading
from discord.ext import commands
import pandas as pd
from src.functions.bootdevparse.Pokematch import Pokematch

class BootDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.df = None
        #print ("BootDev cog initialized")

    @commands.command()
    async def archrecent(self, ctx, number: int):
        
        try:
            # Read the Pokemon CSV file
            df = pd.read_csv('BDparsed_with_pokemon.csv')
            print("CSV file read successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred while building dataframe. That sucks.")
            return
        
        if not number:
            await ctx.send("Please enter a number")
            return
        elif number <= 0:
            await ctx.send("Please enter a number greater than 0")
            return
        elif number > len(df):
            await ctx.send("Number exceeds the length of the CSV file")
            return
        
        try:
            # Get the last 10 rows
            last_x_rows = df.tail(number)
            print(f"Last {number} rows extracted")
            
            total_characters = last_x_rows.astype(str).sum(axis=1).str.len().sum()
            if total_characters > 6000:
                await ctx.send("The total number of characters exceeds the limit of 6000.")
                return

            # Send the last 10 rows as an embed message
            embed = discord.Embed(title=f"Last {number} Archmages", color=discord.Color.gold())
            for index, row in last_x_rows.iterrows():
                embed.add_field(name=f"Archmage rank: {index+1}", value=row.to_string(index=False), inline=False)
            await ctx.send(embed=embed)
            print("Embed message sent successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send("An error occurred while sending the embed message. That sucks.")
            
    # @commands.command()
    # async def archlookup(self, ctx, what :str, value):
    #     pass
            
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
            
            # Send a nice embed message to indicate successful completion of Pokematch run
            embed = discord.Embed(title="Pokematch Run Completed", color=discord.Color.green())
            embed.add_field(name="Status", value="Pokematch run completed successfully", inline=False)
            await ctx.send(embed=embed)
            
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
    
    

