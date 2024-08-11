import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        #print("Help cog initialized")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Bot Commands",
            description="Hello! I am a bot. I can help you with the following commands:",
            color=discord.Color.red()
        )
        embed.set_footer(text="Created by Mehrain")
        embed.add_field(name="$hello", value="To greet you", inline=False)
        embed.add_field(name="$bye", value="To say goodbye", inline=False)
        embed.add_field(name="$help", value="To display this message", inline=False)
        embed.add_field(name="$archrecent [number]", value="Displays the last [number] people that have achieved Archmage.", inline=False)
        await ctx.send(embed=embed)
        #print("Help command executed")

def setup(bot):
    bot.add_cog(Help(bot))
    #print("Help cog loaded")
