# Importing Stuff
import discord
from discord.ext import commands 
import random
import datetime
from datetime import datetime


# Setting up the class 
class AuditLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # This event works when someone joins a server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(id = 774260551076937758)

        em = discord.Embed(title = "Member joined", description = """
```nim
Member Name: {}
Account Created at: {}
```""".format(member, member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")), color = 0xFFA500)
        em.set_thumbnail(url = member.avatar_url)
        em.set_footer(icon_url = member.avatar_url, text = datetime.datetime.utcnow())

        await channel.send(embed=em)

        wchannel = discord.utils.get(self.bot.guilds[0].channels, name = "《🌏》main-gate")

        links = [
            "https://cdn.discordapp.com/attachments/772028276021264394/773835767550050304/welcome1.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835771986837504/welcome2.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835776135528469/welcome3.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835782556745728/welcome4.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835789154779136/welcome5.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835793005019166/welcome6.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835797920874506/welcome7.png",
            "https://cdn.discordapp.com/attachments/772028276021264394/773835804606857216/welcome8.png"
        ]

        image = random.choice(links)

        await channel.send(f"Welcome to the server, {member.mention}! We are `{len(member.guild.members)}` now!")
        em = discord.Embed(title = "Welcome To The 🚀Trident Galaxy🚀!", description = f"Thanks for joining this server, {member.mention}! We are now at {len(member.guild.members)} members! Thank you so much for joining, this really means a lot to us! Hope you don't leave us soon and have fun here! GG!", color = 0x00ffff)
        em.set_thumbnail(url = "https://cdn.discordapp.com/avatars/744872616644575243/0c360da08621da21d055d2379106b197.webp?size=1024")
        em.set_image(url = image)

        await wchannel.send(embed=em)

        mbed = discord.Embed(title = "Thanks for joining 🚀Trident Galaxy🚀!", description = "This really means a lot to us! Hope you don't leave us soon and have fun here! GG!", color = 0x00ffff)
        mbed.add_field(name = "Top Things To Do In 🚀Trident Galaxy🚀:", value = """
    1. Read the rules from <#724648011006869504> believe me its gonna be handy!

    2. After reading the rules, verify yourself in <#741203963315224588> to gain access to the rest of the server!

    3. After verifying yourself, take some roles from <#757818961781063701> and <#768169204930445378>

    4. Then you are all set and ready to make your home at <#731485901091504229>

    **Have Fun In This Server! GG**""")

        await member.send(embed=mbed)

    
    # This event works when someone gets removed from a server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(id = 774260551076937758)

        em = discord.Embed(title = "Member removed", description = """
```nim
Member Name: {}
Joined at: {}
```""".format(member, member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC ")), color = 0xFFA500)
        em.set_thumbnail(url = member.avatar_url)
        em.set_footer(icon_url = member.avatar_url, text = datetime.datetime.utcnow())

        await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.bot:
            return
        channel = self.bot.get_channel(id = 774260551076937758)

        em = discord.Embed(title = "Member Updated", description = """
```nim
Member Name: {}
```""".format(after), color = 0xFFA500)


        await channel.send(embed=em)

    
    # This event works when a message is deleted
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        channel = self.bot.get_channel(id = 774260551076937758)

        em = discord.Embed(title = "Message Deleted", description = """
```nim
Message Author: {}
Channel: {}
```""".format(msg.author, msg.channel), color = 0xFFA500, timestamp = msg.created_at)

        await channel.send(embed=em)

    
    # This event works when a message is edited
    @commands.Cog.listener()
    async def on_message_edit(self, old_msg, new_msg):
        if new_msg.author.bot:
            return
        channel = self.bot.get_channel(id = 774260551076937758)

        em = discord.Embed(title = "Message edited", description = """
```nim
Message Author: {}
Channel: {}
```""".format(new_msg.author, new_msg.channel), color = 0xFFA500, timestamp = new_msg.created_at)

        await channel.send(embed=em)


# Setting up the cog
def setup(bot):
    bot.add_cog(AuditLogs(bot))
    
