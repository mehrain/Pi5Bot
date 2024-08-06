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
    
    if message.content.startswith('$bye'):
        await message.channel.send('Goodbye!')
        
    if message.content.startswith('$help'):
        await message.channel.send('Hello! I am a bot. I can help you with the following commands: \n $hello - To greet you \n $bye - To say goodbye \n $help - To display this message')
        
#fetching the token 
token = os.getenv('DISCORD_TOKEN')  

client.run(token)