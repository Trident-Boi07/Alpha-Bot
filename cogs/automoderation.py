# Importing stuff
import discord
from discord.ext import commands
import json


# Making the container class
class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, msg):
        filtered_words = ["a-bit-of-swear-words-here"]
        slang = ["a-bit-of-racial-slurs-here"]

        for word in filtered_words: # If the message contains swear words then they will be warned
            if word in msg.content.lower():
                
                # Making the database
                with open('./data/warnings.json','r') as f:
                    warns = json.load(f)
                if str(msg.guild.id) not in warns:
                    warns[str(msg.guild.id)] = {}
                if str(msg.author.id) not in warns[str(msg.guild.id)]:
                    warns[str(msg.guild.id)][str(msg.author.id)] = {}
                    warns[str(msg.guild.id)][str(msg.author.id)]["warns"] = 1
                    warns[str(msg.guild.id)][str(msg.author.id)]["warnings"] = [f"Swearing (Auto Moderation); at {msg.created_at}"]
                else:
                    warns[str(msg.guild.id)][str(msg.author.id)]["warnings"].append("Swearing")
                with open('./data/warnings.json','w') as f:
                    json.dump(warns , f)
                    await msg.delete()

                    await msg.author.send("You have been auto-warned by me in the **Trident Galaxy** for **SWEARING**")   
                    await msg.channel.send("Watch your language, {} You have been warned this time".format(msg.author.mention))

        for nword in slang: # If the message contains racial slurs then they will be banned
            if nword in msg.content.lower():
                await msg.delete()
                await msg.channel.send('**{}** has been automatically banned for using the "n" word.'.format(msg.author))
                await msg.author.ban(reason = "Used the n word")

        await self.bot.process_commands(msg)


# Adding the cog
def setup(bot):
    bot.add_cog(AutoMod(bot))
