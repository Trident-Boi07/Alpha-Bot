import discord
from discord.ext import commands
import os
import random
import asyncio

os.chdir = ("C:\\Users\\parth\\OneDrive\\Desktop\\Trident Bot")

bot = commands.Bot(command_prefix = ";", case_insensitive = True)

for filename in os.listdir('./CustomCogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"CustomCogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print('<------------------------------>')
    print('The Alpha version of Trident is ready')
    print(f'Using Discord.py Version {discord.__version__}')
    print('<------------------------------>')

@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

async def change_presence():
    await bot.wait_until_ready()

    statuses = ["with waves", ";help in 69420+ servers", "with alpha and beta signs", "with Trident", "with my master", ">invite for a cookie", "sub to Trident_Boi07 on YouTube", "Yeet it!", "Yeet all day!", "with my master to dump Trident", "with the mods", "Trident Galaxy is EPIC", "with members to invite people"]

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity = discord.Game(name = status))

        await asyncio.sleep(10)


f = open('token.0', 'r') 
TOKEN = f.read()

bot.loop.create_task(change_presence())
bot.run(TOKEN)
