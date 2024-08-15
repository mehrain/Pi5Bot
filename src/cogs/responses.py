from discord.ext import commands
import discord

# Move on_message event to a cog
class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="hello", description="Say hello to the bot")
    async def hello(self, ctx):
        embed = discord.Embed(title='Hello!', description='This is quite a useless command.')
        await ctx.send(embed=embed)

    @commands.slash_command(name="bye", description="Say goodbye to the bot") #todo make shutdown command
    async def bye(self, ctx):
        embed = discord.Embed(title='Goodbye!', description='See you later!')
        await ctx.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title='Command Not Found',
                description=f"The command `{ctx.invoked_with}` was not found.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Responses(bot))