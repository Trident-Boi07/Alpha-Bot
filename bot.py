# Importing stuff
import discord
from discord.ext import commands
import os
import random
import asyncio


# Specifying the file path of our project folder
os.chdir = ("your-project-file-path")


# Defining the bot variable
bot = commands.Bot(command_prefix = ";",
                   case_insensitive = True,
                   allowed_mentions = discord.AllowedMentions(everyone = False, roles = False, users = True))


# Loading the cogs
for filename in os.listdir('./CustomCogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"CustomCogs.{filename[:-3]}")


# This event lets us know when the bot is ready to be used.
@bot.event
async def on_ready():
    print('<------------------------------------------------>')
    print('AlphaBot is now ready to fulfill his duties!')
    print(f'Using Discord.py Version {discord.__version__}')
    print('<------------------------------------------------>')


# This event catches the messages sent
@bot.event
async def on_message(msg):
    await bot.process_commands(msg)


# A simple function which helps us loop through random custom presences
async def change_presence():
    await bot.wait_until_ready()

    statuses = ["with waves", ";help in 69420+ servers", "with alpha and beta signs", "with Trident", "with my master", ">invite for a cookie", "sub to Trident_Boi07 on YouTube", "Yeet it!", "Yeet all day!", "with my master to dump Trident", "with the mods", "Trident Galaxy is EPIC", "with members to invite people"]

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity = discord.Game(name = status))

        await asyncio.sleep(10)


# Getting the token from the token.0 file for security purposes
f = open('token.0', 'r') 
TOKEN = f.read()


# This finally loops the custom presences of the bot
bot.loop.create_task(change_presence())


# And as the function says, it runs the bot and makes the bot come online
bot.run(TOKEN)
