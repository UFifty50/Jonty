#!/bin/python3

import json
import time
import random
import discord
import datetime
import requests
from cogs import roleplayCog, generalCog
import discord.colour
from discord.ext import commands, timers
from discord.ext.commands.errors import *
from discord.errors import DiscordException
from discord.ext.commands.core import Command
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

token = 'ODA0ODQ2ODUyNzgwNDU4MDA0.YBSSCw.l4i5FcfaKQfPvzDONS93R1ejZ3E'
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

purple = 0xff81ff
darkblue = 0x0000ff
lightblue = 0x0096ff
red = 0xff0000
green = 0x00c800

"""
SUB_COMMAND         1
SUB_COMMAND_GROUP   2
STRING              3
INTEGER             4
BOOLEAN             5
USER                6
CHANNEL             7
ROLE                8
"""

version = "1.1.3"


async def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefix = prefixes[str(message.guild.id)]
        return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, help_command=None,
                   case_insensitive=True, intents=discord.Intents.all())
bot.timer_manager = timers.TimerManager(bot)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print('Logged in as', bot.user)
    print('ID:', bot.user.id)
    await bot.change_presence(activity=discord.Game("Now with slash commands!"))
    # await self.bot.change_presence(activity = discord.Streaming(name = "Now with slash commands!", url = "https://twitch.tv")) # , afk=True


@slash.slash(name="setprefix",
             description="Changes the bots prefix.",
             options=[
                 create_option(
                     name="prefix",
                     description="What you want the bot to respond to",
                     option_type=3,
                     required=True
                 )
             ])
@bot.command(aliases=['changeprefix', 'prefixset'], help="Changes the command prefix.", pass_context=True, hidden=True)
async def setprefix(ctx, prefix):
    if ctx.author.guild_permissions.administrator or (ctx.author.id == 513306355390742538):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        self = await ctx.guild.fetch_member(bot.user.id)
        await ctx.send(f'Successfully changed the prefix to: **``{prefix}``**')
        try:
            await self.edit(nick=f"[{prefix}] Jonty")
        except DiscordException:
            await ctx.send(f"I do not have the permissions to change my nick!")
    else:
        await ctx.send(f"sorry {ctx.author}, you do not have the permissions to do that!")


@bot.command(aliases=["purgelogs", "clearlog", "clearlogs"], help="Purge the message logs.")
@commands.is_owner()
async def purgelog(ctx):
    await ctx.send("Message log purged.")
    f = open(f'{ctx.guild.id}.txt', 'w')
    f.write("")
    f.close()


@slash.slash(name="owl",
             description="Summons an **OWL**",
             options=[]
             )
@bot.command()
async def owl(ctx, user=None):
    r = requests.get(
        "https://api.imgur.com/3/album/kzSdMGw/images?client_id=cd388f95a423223").json()
    em = discord.Embed(title="OWL")
    indexmax = len(r['data']) - 1
    size = random.randrange(0, indexmax, 1)
    em.set_image(url=str(r['data'][size]['link']))

    try:
        await ctx.send(embed=em)
    except:
        await ctx.send(str(r['data'][size]['link']))

    # if ctx.message.author.nick == None:
    #    await ctx.send(f"{ctx.message.author.name} is an owl :owl:")
    # else:
    #    await ctx.send(f"{ctx.message.author.nick} is an owl :owl:")


@bot.command(name="timer")
async def remind(ctx, time: int, x):
    #    if x != None:
    if x == "m":
        print("mins")
        date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now(
        ).day, datetime.datetime.now().hour, datetime.datetime.now().minute + time, datetime.datetime.now().second)
        timers.Timer(bot, "reminder", date, args=(
            ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
        await ctx.send(f"Your {time} minute timer has been started.")

    elif x == "s":
        print("seconds")
        date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now(
        ).day, datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second + time)
        timers.Timer(bot, "reminder", date, args=(
            ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
        await ctx.send(f"Your {time} second timer has been started.")

    elif x == "h":
        print("hours")
        date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now(
        ).day, datetime.datetime.now().hour + time, datetime.datetime.now().minute, datetime.datetime.now().second)
        timers.Timer(bot, "reminder", date, args=(
            ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
        await ctx.send(f"Your {time} hour timer has been started.")
#    else:
        #date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour, datetime.datetime.now().minute + time, datetime.datetime.now().second)
        #timers.Timer(bot, "reminder", date, args = (ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
        # await ctx.send(f"Your {time} minute timer has been started.")
#        print("huh, weird lol")


@bot.event
async def on_reminder(channel_id, author_id, text, x):
    channel = bot.get_channel(channel_id)
    if x != None:
        await channel.send("Your {0}{1} timer is up, <@{2}>!".format(text, x, author_id))
    else:
        await channel.send("Your {0} minute timer is up, <@{1}>!".format(text, author_id))


@slash.slash(name="am",
             description="A command to summon a random anime meme!",
             options=[]
             )
@bot.command(aliases=['anime-meme'], help="A command to summon a random anime meme.")
async def am(ctx):
    r = requests.get(
        "https://api.imgur.com/3/album/5TryDub/images?client_id=cd388f95a423223").json()
    em = discord.Embed(title="Have a meme!")
    indexmax = len(r['data']) - 1
    size = random.randrange(0, indexmax, 1)
    em.set_image(url=str(r['data'][size]['link']))
    try:
        await ctx.send(embed=em)
    except:
        await ctx.send(str(r['data'][size]['link']))


@slash.slash(name="changelog",
             description="Prints out Jonty's latest changelog",
             options=[]
             )
@bot.command()
async def changelog(ctx, arg=None):
    changelog = open("changelog.txt")
    lines = changelog.readlines()
    error = False
    if arg != None:
        await ctx.send("This command takes no arguments")
    else:
        em = discord.Embed(title=f"{version} Changelog", color=green)
        line_number = 0
        for line in lines:
            line_number += 1
            line = line.lstrip("\n")
            try:
                if (line[0] == "#") or (line[0] == "\n"):
                    pass
                elif line[0] == "?":
                    index = lines.index(line)
                    value = lines[index+1]
                    if (value == "") or (value == "\n"):
                        bad_lines = [lines[index], lines[index+1]]
                        raise ValueError
                    c = 1
                    for chars in value:
                        if chars not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,/|()&%":
                            c += 1
                        if c == len(value):
                            bad_lines = [lines[index], lines[index+1]]
                            raise ValueError
                    em.add_field(name=f'{line.lstrip("?")}',
                                 value=f"{value}", inline=False)
            except IndexError:
                pass
            except ValueError:
                error = True
                em = discord.Embed(title="Bad changelog syntax", color=red)
                em.add_field(name=f'lines {line_number} and {line_number+1}',
                             value=f"Bad lines: {bad_lines}", inline=False)
                em.add_field(name="Please report this to the main dev, UFifty50",
                             value="Go to https://UFifty50.mywire.org:80/pogbot/issues to report this issue", inline=False)
                # await ctx.send(f"Bad changelog please fix, lines {line_number} and {line_number + 1}\nBad lines: {bad_lines}")
                await ctx.send(embed=em)
                break
        if error:
            pass
        else:
            await ctx.send(embed=em)


class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            em = discord.Embed(description=page)
            await destination.send(embed=em)


bot.help_command = NewHelpName()

"""
@slash.slash(name="help",
             description="Jonty's help command",
             options=[]
             )
@bot.command()
async def help(ctx, arg1=None, arg2=None):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
    if not arg1:
        em = discord.Embed(title="Jonty help", color=0xff81ff)
        em.add_field(name="**roleplay**",
                     value=f"*Either hug em or kill em!*\n**2 commands**", inline=True)
        em.add_field(
            name="**memes**", value=f"*Yeah, we got memes here!*\n**2 commands**", inline=True)
        em.add_field(name="**general**",
                     value=f"*General stuff like fav colours*\n**7 commands**", inline=True)
#        if ctx.guild.id == 779303893464121344:
#            em.add_field(name="apple", value="***who is the true appler***", inline=True)
#            em.add_field(name="whoeatsbones", value="Who eats bones? wait.... Hyper what are you chewing on?", inline=True)
#            em.add_field(name="getfiftylols, gfl", value="Tells you how many times fifty has said lol in your server", inline=True)
        em.add_field(
            name="**timers**", value="*Timers (Work In Progress)*\n**1 command**", inline=True)
        em.add_field(name="**moderation**",
                     value="*Work In Progress*\n**1 command**", inline=True)
    # if ctx.guild.id == 775835250596249630:
    #    em.add_field(name="getfiftylols, gfl", value="Tells you how many times fifty has said lol in your server", inline=True)
        await ctx.send(embed=em)

    elif arg1 == "roleplay":
        em = discord.Embed(title="roleplay help", color=0xff81ff)
        em.add_field(
            name="hug", value="A command to give people hugs, with possible messages added on.", inline=False)
        em.add_field(
            name="kill", value="Everyone dies at some point, especially the people you ping >:)", inline=False)

        await ctx.send(embed=em)

    elif arg1 == "memes":
        em = discord.Embed(title="meme help", color=0xff81ff)
        em.add_field(name="anime-meme, am",
                     value="A command to summon a random anime meme.", inline=False)
        em.add_field(name="owl", value="OWL", inline=False)

        await ctx.send(embed=em)

    elif arg1 == "general":
        em = discord.Embed(title="general help", color=0xff81ff)
        em.add_field(
            name="hi", value="Says hi to whoever you mention.", inline=False)
        em.add_field(
            name="ping", value="Pong! Returns your ping in ms.", inline=False)
        em.add_field(name="setfavcolour, setfavcolor, sfc",
                     value="Sets your favorite colour.", inline=False)
        em.add_field(name="favcolour, favcolor, sfc",
                     value="Says you your favorite colour, or whoever you ping's favorite colour.", inline=False)
        em.add_field(
            name="boop", value="Boops whoever you mention ;)", inline=False)
        em.add_field(name="changelog",
                     value="Displays Jonty's Changelog", inline=False)
        em.add_field(
            name="bonk", value="Bonks whoever you mention ;)", inline=False)
        await ctx.send(embed=em)

    elif arg1 == "timers":
        em = discord.Embed(title="general help", color=0xff81ff)
        em.add_field(
            name="timer", value="Starts a time for the given amount of time, in s, m or h (seconds s, minutes m or hours h).", inline=False)
        em.add_field(name="Under construction",
                     value="not finished", inline=False)

    elif arg1 == "moderation":
        em = discord.Embed(title="general help", color=0xff81ff)
        em.add_field(name="prefixset",
                     value="Changes the command prefix.", inline=False)

    #    await ctx.send(f"The current prefix is `{prefix}`")
"""

# @bot.command()
# @bot.has_permissions(kick_members=True)
# async def kick(ctx, member: discord.Member, *, reason=none):
#    await member.kick(reason=reason)
#    await ctx.send(f'User {member} has kicked for the reason `{reason}`.')

# @bot.command()
# @bot.has_permissions(kick_members=True)
# async def kick(ctx, member: discord.Member, *, reason=none):
#    await member.kick(reason=reason)
#    await ctx.send(f'User {member} has kicked for the reason `{reason}`.')

# @command.error
# async def command_error(ctx):
#    print(f"{ctx.message.author}'s message: {ctx.message.error} errored!")

commandList = [setprefix.name, owl.name,
               changelog.name, roleplayCog.cmds, generalCog.cmds]

if __name__ == "__main__":
    bot.remove_command("help")
    bot.load_extension('cogs.eventCog')
    bot.load_extension('cogs.roleplayCog')
    bot.load_extension('cogs.helpCog')
    bot.load_extension('cogs.generalCog')
    print("All extensions loaded")
    bot.run(token)
