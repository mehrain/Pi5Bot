from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

# Load the environment variables
load_dotenv()
disc_token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

# define bot instance and set command prefix
bot = commands.Bot(intents=intents)

# @bot.event
# async def on_connect():
#     try:
#         if bot.auto_sync_commands:
#             await bot.sync_commands()
#     except Exception as e:
#         print(f"Failed to sync commands: {e}")
#     print(f'Connected to Discord as {bot.user}')

@bot.event
async def on_ready():
    try:
        if bot.auto_sync_commands:
            await bot.sync_commands()
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f'Bot is ready to go! My name is {bot.user}')

    
# Global error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use a valid command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command is on cooldown. Try again after {error.retry_after:.2f} seconds.")
    else:
        await ctx.send("An error occurred while processing the command.")
        print(f"Error in global error handler: {error}")

# add list of cogs to load
cogs_list = [
    'help',
    'responses',
    'bootdev'
]

for cog in cogs_list:
    try:
        bot.load_extension(f'src.cogs.{cog}')
        print(f'Loaded {cog} cog successfully.')
    except Exception as e:
        print(f'Failed to load {cog} cog: {e}')

bot.run(disc_token)