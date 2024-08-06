from dotenv import load_dotenv
import os
import discord

# Load the environment variables
load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    if message.content.startswith('$whoisacunt'):
        await message.channel.send('Vinny is a fucking frog cunt obviously, who else do you think?')
#fetching the token 
token = os.getenv('DISCORD_TOKEN')  

client.run(token)