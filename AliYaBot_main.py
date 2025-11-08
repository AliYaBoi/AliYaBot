Version = "1.1.0"

import discord #discord modules
from discord.ext import commands
from discord import app_commands
import asyncio

import datetime #general python modules
import random
import os #for accesing files in the main folder
from dotenv.main import load_dotenv
import platform
import sys


boot_Time =datetime.datetime.today().replace(microsecond=0)


# Get the absolute path to the directory where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Join the script directory path with the filename
file_path = os.path.join(script_dir, 'address_me.png')

load_dotenv()
bot_Token = os.getenv("bot_Token")
GUILD_ID =discord.Object( os.getenv("DEV_GUILD_ID"))  #debug server



print(commands.bot)
class Client(commands.Bot):
    async def on_ready(self): #on bot bootup
        print(f"Logged in as {self.user}")

        try:
            guild = GUILD_ID
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to server {guild.id}")

        except Exception as e:
            print(f"Synching error: {e}")

    async def on_message_delete(self, message): #repeats deleted messages, hello crazy
        await message.channel.send(f"Deleted message by {message.author}: {message.content}")

    async def on_message(self , message):
        if message.author == self.user:
           return
        # if message.content.startswith("test"):
        #     await message.channel.send("test")

        guess = random.randint(0,150)
        if guess == 1:
            await message.channel.send(file=discord.File(os.path.join(script_dir, 'address_me.png')))
        else:
            print(f"nada: {guess} {message.author}")

intents = discord.Intents.default() 
intents.message_content = True
intents.voice_states = True

client = Client(command_prefix="!", intents = intents)


@client.tree.command(name="stats", description = "Debug Info", guild = GUILD_ID)
async def stats(interaction: discord.Interaction):
    # await interaction.response.send_message(f"Time of boot: {boot_Time} UK time ")
    embed = discord.Embed(title="Stats", color=discord.Colour.random())

    OpSys = platform.system()
    HostDevice =""
    if OpSys == "Linux":
        HostDevice = "Rasberry Pi 3 Model B V1.2 1GB RAM"
    elif OpSys == "Windows":
        HostDevice = "Thinkpad T480 - Intel i5-8350 - 24GB RAM "
    else: 
        HostDevice = "I DONT FUCKING KNOW IM SCARED"

    embed.add_field(name="Version",value=Version,inline=True)
    embed.add_field(name="Ping",value=f"{round(client.latency*1000)}ms",inline=True)

    embed.add_field(name= chr(173),value= chr(173), inline=False)

    embed.add_field(name="Time of Boot",value=boot_Time,inline=True)
    embed.add_field(name="Current Time",value=datetime.datetime.today().replace(microsecond=0),inline=True)

    embed.add_field(name= chr(173),value= chr(173), inline=False)

    embed.add_field(name="Specs",value=HostDevice,inline=True)
    embed.add_field(name="Language",value=f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",inline=True)


    await interaction.response.send_message(embed=embed)


@client.tree.command(name="join", description="Joins your current voice channel", guild = GUILD_ID)
async def join(interaction: discord.Interaction):
    # Check if the user is in a voice channel
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        # Check if the bot is already connected to a voice channel in this guild
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(channel)
            await interaction.response.send_message(f"Moved to your voice channel: **{channel.name}**", ephemeral=True)
        else:
            await channel.connect()
            await interaction.response.send_message(f"Joined voice channel: **{channel.name}**", ephemeral=True)
    else:
        await interaction.response.send_message("You are not in a voice channel. You must be in a voice channel to use this command.", ephemeral=True)




client.run(bot_Token)