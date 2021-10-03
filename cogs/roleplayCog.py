import random
import discord
import requests
from discord.ext import commands
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_commands import create_option


class roleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_slash(name="bonk",
               description="bonks whoever you mention ;)",
               options=[
                   create_option(
                       name="bonk",
                       description="who you gonna bonk bro",
                       option_type=6,
                       required=False
                   )
               ])
    async def bonk(self, ctx, bonk: discord.Member = None):
        if bonk == None:
            await ctx.send("That isnt a member!\nTry pinging an actual person you want to bonk next time")
        else:
            invoker = ctx.author
            if invoker.nick == None:
                invokera = invoker.name
            else:
                invokera = invoker.nick

            if bonk:
                if bonk.nick == None:
                    usera = bonk.name
                else:
                    usera = bonk.nick

                await ctx.send(f"{invokera} bonked {usera}!")
            else:
                await ctx.send(f'Hey {invokera}, bonk!')

    @cog_slash(name="boop",
               description="boop! Better keep dat nose hidden!",
               options=[
                   create_option(
                       name="boop",
                       description="who you gonna boop tho",
                       option_type=6,
                       required=False
                   )
               ])
    async def boop(self, ctx, boop: discord.Member = None):
        if boop == None:
            await ctx.send("You didnt ping anyone, so **im coming for your nose >:)**")
        else:
            invoker = ctx.author
            if invoker.nick == None:
                invokera = invoker.name
            else:
                invokera = invoker.nick

            if boop:
                if boop.nick == None:
                    usera = boop.name
                else:
                    usera = boop.nick

                await ctx.send(f"Boop! {invokera} booped you, {usera}!")
            else:
                await ctx.send(f'Hey {invokera}, boop!')

    @cog_slash(name="hug",
               description="A command to give people hugs, with possible messages added on!",
               options=[
                    create_option(
                        name="user",
                        description="Who you huggin'?",
                        option_type=6,
                        required=False
                    ),
                   create_option(
                        name="message",
                        description="Whats your message?",
                        option_type=3,
                        required=False
                    )
               ])
    async def hug(self, ctx, user: discord.Member, message):
        if user:
            invoker = ctx.author

            """
            message = ""
            for arg in args:
                message = message + arg + " "
            """

            if invoker.nick == None:
                invokera = invoker.name
            else:
                invokera = invoker.nick

            if user.nick == None:
                usera = user.name
            else:
                usera = user.nick

            r = requests.get(
                f"https://api.imgur.com/3/album/sA0jDHt/images?client_id=cd388f95a423223").json()
            em = discord.Embed(
                title=f"Awww, **{invokera}** is hugging **{usera}**!\nHow cute!", colour=0x89cff0, description=message)
            indexmax = len(r['data']) - 1
            size = random.randrange(0, indexmax, 1)
            em.set_image(url=str(r['data'][size]['link']))
            try:
                await ctx.send(embed=em)
            except:
                await ctx.send(str(r['data'][size]['link']))
        else:
            user = ctx.author
            r = requests.get(
                f"https://api.imgur.com/3/album/sA0jDHt/images?client_id=cd388f95a423223").json()
            em = discord.Embed(
                title=f"Your need to mention someone to hug, so\ni'm just gonna hug you instead!", colour=0x89cff0)
            indexmax = len(r['data']) - 1
            size = random.randrange(0, indexmax, 1)
            em.set_image(url=str(r['data'][size]['link']))
            try:
                await ctx.send(embed=em)
            except:
                await ctx.send(str(r['data'][size]['link']))

    @cog_slash(name="pat",
               description="Give other users headpats :)",
               options=[
                    create_option(
                        name="user",
                        description="Who's gettin' dem pats?",
                        option_type=6,
                        required=False
                    )
               ])
    async def pat(self, ctx, xuser: discord.Member):
        xinvoker = ctx.author

        if xinvoker.nick == None:
            invoker = xinvoker.name
        else:
            invoker = xinvoker.nick

        if xuser.nick == None:
            user = xuser.name
        else:
            user = xuser.nick

        em = discord.Embed(title=f"**{invoker}** is giving **{user}** headpats\nHow nice!",
                           colour=0x89cff0, description="*Headpat embeds coming soon!*")
        await ctx.send(embed=em)

    @cog_slash(name="kill",
               description="Murders the victim >:)",
               options=[
                    create_option(
                        name="user",
                        description="**DO IT**",
                        option_type=6,
                        required=False
                    )
               ])
    async def kill(self, ctx, user: discord.Member = None):
        invoker = ctx.author
        try:
            if user:
                if invoker.nick:
                    invokera = invoker.name
                else:
                    invokera = invoker.nick

                if user.nick:
                    usera = user.name
                else:
                    usera = user.nick

                if user == invoker:
                    await ctx.send(f"{usera} is staing alive! *pouts*")
                else:
                    sample = [
                        f"Killed {usera}! {usera} is now dead :(",
                        f"{invokera} kicked {usera} where nobody should be kicked.",
                        f"{usera} died.",
                        f"{usera} got hit by a truck.",
                        f"{usera} died after eating too many pickles.",
                        f"In a suprising turn of events, {usera} stays alive!",
                        f"{invokera} tries to kill {usera}, but {usera} is ready for them and slaps {invoker.nick}'s aorta!",
                        f"{usera} pogged too hard.",
                        f"{usera} got a question wrong in the victorian era, and was forced to wear the dunce hat. They died of embarrassment.",
                        f"{invokera} ran {usera} over with their citroen."
                    ]
                    await ctx.send(random.sample(sample, 1)[0])
            else:
                await ctx.send("You need to specify someone to kill, you devil!")
        except discord.ext.commands.errors.MemberNotFound:
            await ctx.send("That isnt a member, silly!\nTry pinging a real member next time.")


cmds = [roleplayCog.pat.name, roleplayCog.hug.name, roleplayCog.kill.name,
        roleplayCog.boop.name, roleplayCog.bonk.name]


def setup(bot):
    bot.add_cog(roleplayCog(bot))
    print("roleplayCog loaded")
