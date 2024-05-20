import os
import logging
from logging import Logger
import random
import requests
import discord
import discord.colour
from discord import app_commands
from discord.ext import commands

from Utils import Colour, sendEmbed

JontyLogger: Logger = logging.getLogger("Jonty")


class GeneralCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        JontyLogger.info("GeneralCog is ready")

    @app_commands.command(name="sync", description="Syncs the commands")
    async def sync(self, interaction: discord.Interaction):
        fmt = await self.bot.tree.sync(guild=interaction.guild)
        await interaction.response.send_message(f"Synced {len(fmt)} commands")

    @app_commands.command(
        name="ping",
        description="Pong! Returns your ping in ms.",
    )
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(interaction.client.latency * 1000)
        await interaction.response.send_message(f"Pong! Your ping is {bot_latency} ms.")

    # @app_commands.command(name="sfc",
    #            description="Sets your fav colour!",
    #            options=[
    #                 create_option(
    #                     name="colour",
    #                     description="Whats yours?",
    #                     option_type=3,
    #                     required=False
    #                 )
    #            ])
    # async def sfc(self, ctx, *, colour=None):
    #     if colour != None:
    #         favcolour = colour
    #         with open('favcolours.json', 'r') as f:
    #             favcolours = json.load(f)
    #             favcolours[str(ctx.author.id)] = favcolour.rstrip(" ")
    #         with open('favcolours.json', 'w') as f:
    #             json.dump(favcolours, f, indent=4)
    #         if ctx.author.nick == None:
    #             await ctx.send(f"{ctx.author.name}'s favorite colour has been set to `{favcolour.rstrip(' ')}`")
    #         else:
    #             await ctx.send(f"{ctx.author.nick}'s favorite colour has been set to `{favcolour.rstrip(' ')}`")
    #     else:
    #         await ctx.send("you must specify a colour!")

    # @cog_slash(name="fc",
    #            description="Tells you what the pinged person's fav colour is",
    #            options=[
    #                create_option(
    #                    name="user",
    #                    description="Its time to find out :)",
    #                    option_type=6,
    #                    required=False
    #                )
    #            ])
    # async def fc(self, ctx, user: discord.Member = None):
    #     if user:
    #         try:
    #             with open('favcolours.json', 'r') as f:
    #                 favcolours = json.load(f)
    #                 favcolour = favcolours[str(user.id)]
    #             if user.nick == None:
    #                 await ctx.send(f"{user.name}'s favorite colour is `{favcolour}`")
    #             else:
    #                 await ctx.send(f"{user.nick}'s favorite colour is `{favcolour}`")
    #         except Exception:
    #             await ctx.send("This user has not set a favorite colour yet!")
    #     else:
    #         try:
    #             with open('favcolours.json', 'r') as f:
    #                 favcolours = json.load(f)
    #                 favcolour = favcolours[str(ctx.author.id)]
    #             if ctx.author.nick == None:
    #                 await ctx.send(f"{ctx.author.name}'s favorite colour is `{favcolour}`")
    #             else:
    #                 await ctx.send(f"{ctx.author.nick}'s favorite colour is `{favcolour}`")
    #         except Exception:
    #             await ctx.send("You have not set a favorite colour yet!")

    @app_commands.command(name="hi", description="Says hi!")
    @app_commands.describe(user="Who you sain' hi to?")
    async def hi(self, interaction: discord.Interaction, user: discord.Member):
        invokerName = (
            interaction.user.nick if interaction.user.nick else interaction.user.name  # type: ignore
        )
        userName = user.nick if user.nick else user.name

        await interaction.response.send_message(
            f"{invokerName} is saying hi to you, {userName}!"
        )

    @app_commands.command(
        name="anime-meme", description="A command to summon a random anime meme."
    )
    async def animeMeme(self, interaction: discord.Interaction):
        imageListJson = requests.get(
            f"https://api.imgur.com/3/album/5TryDub/images?client_id={os.environ['IMGUR_CLIENT_ID']}"
        ).json()["data"]
        imageLink = random.choice(imageListJson)["link"]

        em = discord.Embed(title="Have a meme!")
        em.set_image(url=imageLink)

        await sendEmbed(interaction, em)

    # @app_commands.command(
    #     name="changelog", description="Prints out Jonty's latest changelog"
    # )
    # async def changelog(self, interaction: discord.Interaction):
    #     changelog = open("changelog.txt")
    #     lines = changelog.readlines()
    #     error = False
    #     em = discord.Embed(title=f"{os.environ['JONTY_VERSION']} Changelog", color=Colour.green) # type: ignore
    #     line_number = 0
    #     for line in lines:
    #         line_number += 1
    #         line = line.lstrip("\n")
    #         try:
    #             if (line[0] == "#") or (line[0] == "\n"):
    #                 pass
    #             elif line[0] == "?":
    #                 index = lines.index(line)
    #                 value = lines[index + 1]
    #                 if (value == "") or (value == "\n"):
    #                     bad_lines = [lines[index], lines[index + 1]]
    #                     raise ValueError
    #                 c = 1
    #                 for chars in value:
    #                     if (
    #                         chars
    #                         not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,/|()&%"
    #                     ):
    #                         c += 1
    #                     if c == len(value):
    #                         bad_lines = [lines[index], lines[index + 1]]
    #                         raise ValueError
    #                 em.add_field(
    #                     name=f'{line.lstrip("?")}', value=f"{value}", inline=False
    #                 )
    #         except IndexError:
    #             pass
    #         except ValueError:
    #             error = True
    #             em = discord.Embed(title="Bad changelog syntax", color=Colour.red) # type: ignore
    #             em.add_field(
    #                 name=f"lines {line_number} and {line_number+1}",
    #                 value=f"Bad lines: {bad_lines}",
    #                 inline=False,
    #             )
    #             em.add_field(
    #                 name="Please report this to the main dev, UFifty50",
    #                 value="Go to https://github.com/UFifty50/Jonty/issues to report this issue",
    #                 inline=False,
    #             )
    #             # await ctx.send(f"Bad changelog please fix, lines {line_number} and {line_number + 1}\nBad lines: {bad_lines}")
    #             await interaction.response.send_message(embed=em)
    #             break
    #     if error:
    #         pass
    #     else:
    #         await interaction.response.send_message(embed=em)

    @app_commands.command(name="owl", description="Summons an **OWL**")
    async def owl(self, interaction: discord.Interaction):
        imageListJson = requests.get(
            f"https://api.imgur.com/3/album/kzSdMGw/images?client_id={os.environ['IMGUR_CLIENT_ID']}"
        ).json()["data"]
        imageLink = random.choice(imageListJson)["link"]

        em = discord.Embed(title="OWL")
        em.set_image(url=imageLink)

        await sendEmbed(interaction, em)


cmds = [
    GeneralCog.owl.name,
    #   GeneralCog.changelog.name,
    GeneralCog.ping.name,
    GeneralCog.hi.name,
    GeneralCog.animeMeme.name,
    GeneralCog.sync.name,
    # generalCog.sfc.name,
    # generalCog.fc.name,
]


async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))
