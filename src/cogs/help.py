import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        #print("Help cog initialized")

    @commands.slash_command(name="help", description="Display the bot commands")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Bot Commands",
            description="Hello! I am a bot. I can help you with the following commands:",
            color=discord.Color.red()
        )
        embed.set_footer(text="Created by Mehrain")
        embed.add_field(name="/hello", value="To greet you", inline=False)
        embed.add_field(name="/bye", value="To say goodbye", inline=False)
        embed.add_field(name="/help", value="To display this message", inline=False)
        embed.add_field(name="/archsync", value="Run this to execute a manual DB update or initalization. Otherwise it autoupdates every 15 mins.", inline=False)
        embed.add_field(name="/archrecent [number]", value="Displays the last [number] people that have achieved Archmage.", inline=False)
        embed.add_field(name="/archsearch [Rank/Name/Username/Date/Pokemon] [Value]", value="Searches the database for a specific field, returns the entire row if found.", inline=False)
        await ctx.send(embed=embed)
        #print("Help command executed")

def setup(bot):
    cog = Help(bot)
    bot.add_cog(cog)
    #print("Help cog loaded")
