# Importing stuff
import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import cooldown, BucketType
import json
import traceback


# Making the class container
class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Database Setup

    async def open_muterole(self, role):
        roles = await self.get_muterole()

        if str(role.id) in roles:
            return False
        else:
            roles[str(role.id)] = "none"

        with open('./data/muterole.json', 'w') as f:
            json.dump(roles, f)
        return True


    async def get_muterole(self):
        with open('./data/muterole.json', 'r') as f:
            roles = json.load(f)

        return roles

    @commands.command(aliases=["purge"])
    @cooldown(1, 3, BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *, amount: int = None):
        if amount == None:
            await ctx.send(f"Please enter an amount of messages to be purged, {ctx.author.mention}")

        elif amount > 99 or amount < 1:
            await ctx.send(f"The amount of messages to be deleted must be between 2 and 100, {ctx.author.mention}")

        else:
            await ctx.channel.purge(limit=amount+1)

            em = discord.Embed(title=f":white_check_mark: | {amount} messages have been successfully deleted!", colour = discord.Colour.blue())

            msg = await ctx.send(embed=em)

            await asyncio.sleep(3)
            await msg.delete()


    @commands.command()
    @commands.has_permissions(kick_members=True)
    @cooldown(1, 3, BucketType.user)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
    
        if reason == None:
            await member.kick(reason="No reason was provided")
            em = discord.Embed(title = f"{member} has been kicked!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** No reason was provided.", color = ctx.author.color, timestamp = ctx.message.created_at)

            await ctx.send(embed=em)

            await member.send(f"You were kicked from **{ctx.guild}** by **{ctx.author}** and **no reason was provided.**")

            return

        elif reason != None:
            await member.kick(reason=reason)
            em = discord.Embed(title = f"{member} has been kicked!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** {reason}", color = ctx.author.color, timestamp = ctx.message.created_at)
    
            await ctx.send(embed=em)

            await member.send(f"You were kicked from **{ctx.guild}** by **{ctx.author}** because **{reason}**")

            return


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 3, BucketType.user)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
    
        if reason == None:
            await member.ban(reason="No reason was provided")
            em = discord.Embed(title = f"{member} has been Banned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** No reason was provided.", color = ctx.author.color, timestamp = ctx.message.created_at)

            await ctx.send(embed=em)

            await member.send(f"You were banned from **{ctx.guild}** by **{ctx.author}** and **no reason was provided.**")

            return

        elif reason != None:
            await member.ban(reason=reason)
            em = discord.Embed(title = f"{member} has been banned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** {reason}", color = ctx.author.color, timestamp = ctx.message.created_at)
    
            await ctx.send(embed=em)

            await member.send(f"You were banned from **{ctx.guild}** by **{ctx.author}** because **{reason}**")

            return

    

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 3, BucketType.user)
    async def unban(self, ctx, member=None, *, reason='No Reason Was Provided'):
        if member == None:
            await ctx.send(f"You can't unban yourself, {ctx.author.mention}\nNext time provide a user.")
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_disc):
                em = discord.Embed(title = f"{member} has been unbanned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** {reason}", color = ctx.author.color, timestamp = ctx.message.created_at)
    
                await ctx.send(embed=em)

                await member.send(f"You were unbanned from **{ctx.guild}** by **{ctx.author}** because **{reason}**")

                return

        await ctx.send(member + ' was not found. Make sure you gave a valid format (For eg. Trident_Boi07#7452)')


    @commands.command()
    @commands.has_guild_permissions(manage_guild = True)
    async def muterole(self, ctx, msg = None, *, role: discord.Role = None):
        await self.open_muterole(ctx.guild)

        with open('./data/muterole.json', 'r') as f:
            roles = json.load(f)

        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        if msg == None:
            await ctx.send(f"Invalid arguments provided! Correct way to use this command is -> `{prefix}muterole <set> <role>` to set a muterole, else type `{prefix}muterole remove` to remove the muterole which had been set up.")

        if msg == "set":
            roles[str(ctx.guild.id)] = role.id
            em = discord.Embed(title = "<:tick:766512731616182293> Muterole Setup Successful!", description = f"The muterole for {ctx.guild.name} has been successfully set up to {role.mention}", color = ctx.author.color)
            await ctx.send(embed=em)

            with open("./data/muterole.json", 'w') as f:
                json.dump(roles, f)

        elif msg == "remove":
            roles[str(ctx.guild.id)] = "none"
            em = discord.Embed(title = "<:tick:766512731616182293> Muterole Removal Successful!", description = f"The muterole for {ctx.guild.name} has been successfully removed!", color = ctx.author.color)
            await ctx.send(embed=em)

            with open("./data/muterole.json", 'w') as f:
                json.dump(roles, f)

        else:
            await ctx.send(f"Invalid arguments provided! Correct way to use this command is -> `{prefix}muterole <set> <role>` to set a muterole, else type `{prefix}muterole remove` to remove the muterole which had been set up.")

    def convert(self, time):
        pos = ["s", "sec", "sec", "m", "min", "mins", "h", "hrs", "hr", "d" "days"]

        time_dict = {"s": 1, "sec": 1, "secs": 1, "m" : 60, "min": 60, "mins": 60, "h": 3600, "hr": 3600, "hrs": 3600, "d": 86400, "days": 86400}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def tempmute(self, ctx, member: discord.Member = None, duration = None, *, reason = None):
        await self.open_muterole(ctx.guild)

        with open('./data/muterole.json', 'r') as f:
            roles = json.load(f)

        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        muterole = ctx.guild.get_role(roles[str(ctx.guild.id)])

        if duration == -1:
            await ctx.send("Invalid duration provided.")

            return

        elif duration == -2:
            await ctx.send("Invalid duration provided.")

            return           
        
        time = self.convert(duration)   

        if member == None or duration == None:
            await ctx.send(f"Invalid arguments provided! The correct method is -> `{prefix}mute <user> <duration> <reason>`") 

        else:    
            await member.add_roles(muterole)

            if roles[str(ctx.guild.id)] == "none":
                await ctx.send(f"The muterole for this server isn't setup. Type `{prefix}muterole set <role>` to set one!")

            else:
                if reason == None:
                    em = discord.Embed(title = f"{member} has been muted!", description = f"The mute may not work perfectly if it isn't setup well\n**Responsible Moderator:** {ctx.author.mention}\n**Time:** {duration}\n**Reason:** No reason was provided", color = ctx.author.color)

                    await ctx.send(embed=em)

                    await member.send(f"You were muted in **{ctx.guild}** by **{ctx.author}** and **no reason was provided**")

                else:
                    em = discord.Embed(timestamp = ctx.message.created_at, title = f"{member} has been muted!", description = f"The mute may not work perfectly if it isn't setup well\n**Responsible Moderator:** {ctx.author.mention}\n**Time:** {duration}\n**Reason:** {reason}", color = ctx.author.color)

                    await ctx.send(embed=em)

                    await member.send(f"You were muted in **{ctx.guild}** by **{ctx.author}** because **{reason}**")

                await asyncio.sleep(time)

                await member.remove_roles(muterole)


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member: discord.Member = None, *, reason = None):
        await self.open_muterole(ctx.guild)

        with open('./data/muterole.json', 'r') as f:
            roles = json.load(f)

        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        muterole = ctx.guild.get_role(roles[str(ctx.guild.id)])

        if member == None:
            await ctx.send(f"Invalid arguments provided! The correct method is -> `{prefix}mute <user> <reason>`") 

        else:    

            if roles[str(ctx.guild.id)] == "none":
                await ctx.send(f"The muterole for this server isn't setup. Type `{prefix}muterole set <role>` to set one!")

            else:
                await member.add_roles(muterole)

                if reason == None:
                    em = discord.Embed(title = f"{member} has been muted!", description = f"The mute may not work perfectly if it isn't setup well\n**Responsible Moderator:** {ctx.author.mention}\n**Time:** Indefinite\n**Reason:** No reason was provided", color = ctx.author.color)

                    await ctx.send(embed=em)

                    await member.send(f"You were muted in **{ctx.guild}** by **{ctx.author}** and **no reason was provided**")

                else:
                    em = discord.Embed(timestamp = ctx.message.created_at, title = f"{member} has been muted!", description = f"The mute may not work perfectly if it isn't setup well\n**Responsible Moderator:** {ctx.author.mention}\n**Time:** Indefinite\n**Reason:** {reason}", color = ctx.author.color)

                    await ctx.send(embed=em)

                    await member.send(f"You were muted in **{ctx.guild}** by **{ctx.author}** because **{reason}**")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, *, member: discord.Member = None):
        await self.open_muterole(ctx.guild)

        with open('./data/muterole.json', 'r') as f:
            roles= json.load(f)

        muterole = roles[str(ctx.guild.id)]

        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        if roles[str(ctx.guild.id)] == "none":
                await ctx.send(f"The muterole for this server isn't setup. Type `{prefix}muterole set <role>` to set one!")

        else:
            for role in member.roles:
                if role.id == muterole:
                    if muterole in member.roles:
                        await ctx.send(f"That user hasn't been muted yet! Type `{prefix}mute <user> <duration> <reason>` to mute a person!")
                    await member.remove_roles(role)
                    await ctx.send(f"**{member.name}** has been successfully unmuted")

                    return

            if muterole not in member.roles:
                await ctx.send(f"That member is not muted!")

    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @cooldown(1, 3, BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        
        # Making the database
        with open('./data/warnings.json','r') as f:
            warns = json.load(f)
        if str(ctx.guild.id) not in warns:
            warns[str(ctx.guild.id)] = {}
        if str(member.id) not in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)] = {}
            warns[str(ctx.guild.id)][str(member.id)]["warns"] = 1
            warns[str(ctx.guild.id)][str(member.id)]["warnings"] = [f"{reason}; by {ctx.author}; at {ctx.message.created_at}"]
        else:
            warns[str(ctx.guild.id)][str(member.id)]["warnings"].append(reason)
        with open('./data/warnings.json','w') as f:
            json.dump(warns , f)
    
        if reason == None:

            em = discord.Embed(title = f"{member} has been warned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** No reason was provided.", color = ctx.author.color, timestamp = ctx.message.created_at)

            await ctx.send(embed=em)

            await member.send(f"You were warned in **{ctx.guild}** by **{ctx.author}** and **no reason was provided.**")

            return

        elif reason != None:

            em = discord.Embed(title = f"{member} has been warned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Reason:** {reason}", color = ctx.author.color, timestamp = ctx.message.created_at)
    
            await ctx.send(embed=em)

            await member.send(f"You were warned in **{ctx.guild}** by **{ctx.author}** because **{reason}**")

            return

    @commands.command()
    async def selfmute(self, ctx, *, duration = None):
        await self.open_muterole(ctx.guild)

        with open('./data/muterole.json', 'r') as f:
            roles = json.load(f)

        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        muterole = ctx.guild.get_role(roles[str(ctx.guild.id)])

        member = ctx.author

        if duration == -1:
            await ctx.send("Invalid duration provided.")

            return

        elif duration == -2:
            await ctx.send("Invalid duration provided.")

            return           
        
        time = self.convert(duration)   

        if duration == None:
            await ctx.send(f"Invalid arguments provided! The correct method is -> `{prefix}mute <user> <duration> <reason>`") 

        else:    
            await member.add_roles(muterole)

            if roles[str(ctx.guild.id)] == "none":
                await ctx.send(f"The muterole for this server isn't setup. Tell an admin to type `{prefix}muterole set <role>` to set one!")

            else:
                await ctx.send(f"Make sure to enjoy your mute, **{member.name}**")

                await asyncio.sleep(time)

                await member.remove_roles(muterole)

                for role in member.roles:
                    if role.id == muterole:
                        if muterole in member.roles:
                            
                            
                            await ctx.send(f"**{member.name}** has been auto unmuted due to the completion of the duration of the mute.")


    @commands.command(aliases= ["giverole"])
    @commands.has_guild_permissions(manage_roles = True)
    async def addrole(self, ctx, member: discord.Member = None, *, role: discord.Role = None):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        if member == None or role == None:
            await ctx.send(f"Enough arguments weren't provided. The correct arguments are -> `{prefix}addrole <user> <role>`")
        else:
            await member.add_roles(role)
            em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at, title = "<:tick:766512731616182293> Role Added Successfully!", description = f"The role {role.mention} was successfully added to {member.mention}")
             
            await ctx.send(embed=em)

    @commands.command()
    @commands.has_guild_permissions(manage_roles = True)
    async def removerole(self, ctx, member: discord.Member = None, *, role: discord.Role = None):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        if member == None or role == None:
            await ctx.send(f"Enough arguments weren't provided. The correct arguments are -> `{prefix}addrole <user> <role>`")
        else:
            await member.remove_roles(role)
            em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at, title = "<:tick:766512731616182293> Role Removed Successfully!", description = f"The role {role.mention} was successfully removed from {member.mention}")
             
            await ctx.send(embed=em)

    @commands.command(aliases= ["cn", "changenick", "nickname"])
    @commands.has_guild_permissions(manage_nicknames = True)
    async def changenickname(self, ctx, member: discord.Member = None, *, nickname = None):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        oldname = member.display_name

        if member == None and nickname == None:
            await ctx.send(f"Not enough arguments provided. Type `{prefix}nickname <user> <new nickname>` to change a user's nickname!")

        else:
            await member.edit(nick = nickname)
            em = discord.Embed(title = "NickName Change", description = 
f"""
```diff
Responsible Moderatior: {ctx.author}
- Old Nickname: {oldname}
+ New Nickname: {nickname}
```""", color = member.color, timestamp =ctx.message.created_at)
            await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member = None, *, reason = "No reason was provided."):
        if member == None:
            await ctx.send(f"You can not ban yourself, {ctx.author.mention}")

        else:
            await member.ban(reason=reason)
            await member.unban(reason = reason)
            em = discord.Embed(title = f"<:tick:766512731616182293> Successfully softbanned {member}", description = f"**Reason: **{reason}\n**Responsible Moderator**: {ctx.author.mention}", timestamp = ctx.message.created_at, color = ctx.author.color)

            await ctx.send(embed=em)

            if reason == None:
                await member.send(f"You were soft banned in **{ctx.guild}** by **{ctx.author}** and **no reason was provided.**")

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def tempban(self, ctx, member: discord.Member = None, duration = None, *, reason = "No reason was provided."):

        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]

        if duration == -1:
            await ctx.send("Invalid duration provided.")

            return

        elif duration == -2:
            await ctx.send("Invalid duration provided.")

            return           
        
        time = self.convert(duration)   

        if member == None or duration == None:
            await ctx.send(f"Invalid arguments provided! The correct method is -> `{prefix}tempban <user> <duration> [reason]`") 

        else:    
            await member.ban(reason = reason)

            if reason == None:
                em = discord.Embed(title = f"{member} has been banned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Time:** {duration}\n**Reason:** No reason was provided", color = ctx.author.color)

                await ctx.send(embed=em)

                await member.send(f"You were banned from **{ctx.guild}** by **{ctx.author}** and **no reason was provided**")

            else:
                em = discord.Embed(timestamp = ctx.message.created_at, title = f"{member} has been banned!", description = f"**Responsible Moderator:** {ctx.author.mention}\n**Duration:** {duration}\n**Reason:** {reason}", color = ctx.author.color)

                await ctx.send(embed=em)

                await member.send(f"You were temporarily banned in **{ctx.guild}** by **{ctx.author}** because **{reason}**")

            await asyncio.sleep(time)

            await member.unban(reason = 'No reason was provided.')

    @commands.command(aliases = ["clearwarn"])
    @commands.has_permissions(manage_guild=True)
    async def removewarn(self,ctx, member: discord.Member, num: int, *, reason='No reason provided.'):
        with open('./data/warnings.json' , 'r') as f:
            warns = json.load(f)

        num -= 1
        warns[str(ctx.guild.id)][str(member.id)]["warns"] -= 1
        warns[str(ctx.guild.id)][str(member.id)]["warnings"].pop(num)
        with open('./data/warnings.json' , 'w') as f:
            json.dump(warns , f)
        em = discord.Embed(timestamp = ctx.message.created_at, color = ctx.author.color, description = f"Warn of {member.mention} has been successfully removed by {ctx.author.mention}")
        await ctx.send(embed=em)

    @commands.command(aliases = ["warnings"])
    @commands.has_permissions(manage_messages=True)
    async def warns(self,ctx , member : discord.Member):
        with open('./data/warnings.json', 'r') as f:
            warns = json.load(f)

        num = 1
        warnings = discord.Embed(title = f"{member}\'s warns", color = ctx.author.color)
        for warn in warns[str(ctx.guild.id)][str(member.id)]["warnings"]:
            warnings.add_field(name = f"Warn {num}" , value = warn)
            num += 1
        await ctx.send(embed = warnings)

    @commands.command(aliases=["ui", "user"])
    @cooldown(1, 5, BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):

        if member == None:
            member = ctx.author

        roles = [role for role in member.roles]
            
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)

        embed.add_field(name="Full name:", value=f"{member.name}")
        embed.add_field(name="Guild name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC "), inline=False)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC "), inline=False)
        embed.add_field(name=f"Roles ({len(roles)})", value = " ".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Top role:", value=member.top_role.mention, inline=False)
        embed.add_field(name="Bot?", value = member.bot)

        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx, message = None):

        em = discord.Embed(
            color = ctx.author.color,
            title = f"{ctx.guild.name} Server Info!",
            timestamp = ctx.message.created_at
        )
        em.set_thumbnail(url = ctx.guild.icon_url)
        em.add_field(name = "Server Created At", value = ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC "), inline =False)
        em.add_field(name = "Owner", value = ctx.guild.owner, inline =False)
        em.add_field(name = f"Guild ID", value = ctx.guild.id, inline = False)
        em.add_field(name="Region", value = ctx.guild.region, inline = False)
        em.add_field(name="Member Count", value = ctx.guild.member_count, inline = False)
        em.add_field(name= "Channel Count", value = f"{len(ctx.guild.channels)}", inline =False)
        em.add_field(name = "Role Count", value = f"{len(ctx.guild.roles)}", inline = False)
        em.add_field(name = "Booster Count", value = ctx.guild.premium_subscription_count, inline = False)
        em.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")

        await ctx.send(embed=em)

    @commands.command(aliases = ["av"])
    @cooldown(1, 5, BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member == None:
            em = discord.Embed(description=f"[**{ctx.author.name}'s Avatar**]({ctx.author.avatar_url})", colour=ctx.author.color, timestamp =ctx.message.created_at)
            em.set_image(url= ctx.author.avatar_url)
            em.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")

            await ctx.send(embed=em)

            return

        else:
            em = discord.Embed(description=f"[**{member.name}'s Avatar**]({member.avatar_url})", colour = member.color, timestamp =ctx.message.created_at)
            em.set_image(url=member.avatar_url)
            em.set_footer(icon_url = member.avatar_url, text = f"Requested by {ctx.author}")

            await ctx.send(embed=em)

            return


# Adding the cog
def setup(bot):
    bot.add_cog(Moderation(bot))
