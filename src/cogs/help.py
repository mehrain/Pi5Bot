import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Bot Commands", description="Hello! I am a bot. I can help you with the following commands:")
        embed.add_field(name="$hello", value="To greet you", inline=False)
        embed.add_field(name="$bye", value="To say goodbye", inline=False)
        embed.add_field(name="$help", value="To display this message", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
