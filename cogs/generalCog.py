from discord_slash.utils.manage_commands import create_option
from discord_slash.cog_ext import cog_slash
from discord.ext import commands
import discord
import time
import json


class generalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_slash(name="ping",
               description="Pong! Returns your ping in ms.",
               options=[]
               )
    async def ping(self, ctx):
        #   await delete_message(ctx.message)
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  Your ping is `{int(ping)}ms`")
        print(f'{ctx.author.name}\'s current ping is {int(ping)}ms')

    @cog_slash(name="sfc",
               description="Sets your fav colour!",
               options=[
                    create_option(
                        name="colour",
                        description="Whats yours?",
                        option_type=3,
                        required=False
                    )
               ])
    async def sfc(self, ctx, *, colour=None):
        if colour != None:
            favcolour = colour
            with open('favcolours.json', 'r') as f:
                favcolours = json.load(f)
                favcolours[str(ctx.author.id)] = favcolour.rstrip(" ")
            with open('favcolours.json', 'w') as f:
                json.dump(favcolours, f, indent=4)
            if ctx.author.nick == None:
                await ctx.send(f"{ctx.author.name}'s favorite colour has been set to `{favcolour.rstrip(' ')}`")
            else:
                await ctx.send(f"{ctx.author.nick}'s favorite colour has been set to `{favcolour.rstrip(' ')}`")
        else:
            await ctx.send("you must specify a colour!")

    @cog_slash(name="fc",
               description="Tells you what the pinged person's fav colour is",
               options=[
                   create_option(
                       name="user",
                       description="Its time to find out :)",
                       option_type=6,
                       required=False
                   )
               ])
    async def fc(self, ctx, user: discord.Member = None):
        if user:
            try:
                with open('favcolours.json', 'r') as f:
                    favcolours = json.load(f)
                    favcolour = favcolours[str(user.id)]
                if user.nick == None:
                    await ctx.send(f"{user.name}'s favorite colour is `{favcolour}`")
                else:
                    await ctx.send(f"{user.nick}'s favorite colour is `{favcolour}`")
            except Exception:
                await ctx.send("This user has not set a favorite colour yet!")
        else:
            try:
                with open('favcolours.json', 'r') as f:
                    favcolours = json.load(f)
                    favcolour = favcolours[str(ctx.author.id)]
                if ctx.author.nick == None:
                    await ctx.send(f"{ctx.author.name}'s favorite colour is `{favcolour}`")
                else:
                    await ctx.send(f"{ctx.author.nick}'s favorite colour is `{favcolour}`")
            except Exception:
                await ctx.send("You have not set a favorite colour yet!")

    @cog_slash(name="hi",
               description="Says hi!",
               options=[
                    create_option(
                        name="user",
                        description="Who you sain' hi to?",
                        option_type=6,
                        required=False
                    )
               ])
    async def hi(self, ctx, user: discord.Member = None):
        invoker = ctx.author
        if invoker.nick == None:
            invokera = invoker.name
        else:
            invokera = invoker.nick

        if user:
            if user.nick == None:
                usera = user.name
            else:
                usera = user.nick

            await ctx.send(f"{invokera} is saying hi to you, {usera}!")
        else:
            await ctx.send(f'Hi {invokera}!')


cmds = [generalCog.ping.name, generalCog.sfc.name,
        generalCog.fc.name, generalCog.hi.name]


def setup(bot):
    bot.add_cog(generalCog(bot))
    print("generalCog loaded")
