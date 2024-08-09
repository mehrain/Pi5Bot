from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

# Load the environment variables
load_dotenv()
disc_token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

#define bot instance and set command prefix
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#add list of cogs to load
cogs_list = [
    'help',
    'responses',
    'bootdev'
]

for cog in cogs_list:
    bot.load_extension(f'src.cogs.{cog}')

bot.run(disc_token)