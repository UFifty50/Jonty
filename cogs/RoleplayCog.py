import os
import logging
from logging import Logger
import random
import requests
import discord
from discord.ext import commands
from discord import app_commands

from Utils import sendEmbed


JontyLogger: Logger = logging.getLogger("Jonty")

class RoleplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        JontyLogger.info("RoleplayCog is ready")

    @app_commands.command(name="bonk", description="bonks whoever you mention ;)")
    @app_commands.describe(bonk="who you gonna bonk bro")
    async def bonk(self, interaction: discord.Interaction, bonk: discord.Member):
        invokerName = (
            interaction.user.nick if interaction.user.nick else interaction.user.name  # type: ignore
        )
        victim = bonk.nick if bonk.nick else bonk.name

        await interaction.response.send_message(f"{invokerName} bonked {victim}!")

    @app_commands.command(name="boop", description="boop! Better keep dat nose hidden!")
    @app_commands.describe(boop="who you gonna boop tho")
    async def boop(self, interaction: discord.Interaction, boop: discord.Member):
        invokerName = (
            interaction.user.nick if interaction.user.nick else interaction.user.name  # type: ignore
        )
        victim = boop.nick if boop.nick else boop.name

        await interaction.response.send_message(
            f"Boop! {invokerName} booped you, {victim}!"
        )

    @app_commands.command(
        name="hug",
        description="A command to give people hugs, with possible messages added on!",
    )
    @app_commands.describe(user="Who you huggin'?")
    @app_commands.describe(message="Whats your message?")
    async def hug(
        self,
        interaction: discord.Interaction,
        user: discord.Member | None = None,
        message: str | None = None,
    ):
        invokerName = (
            interaction.user.nick if interaction.user.nick else interaction.user.name  # type: ignore
        )
        imageListJson = requests.get(
            f"https://api.imgur.com/3/album/sA0jDHt/images?client_id={os.environ['IMGUR_CLIENT_ID']}"
        ).json()["data"]
        imageLink = random.choice(imageListJson)["link"]

        if user:
            userName = user.nick if user.nick else user.name

            em = discord.Embed(
                title=f"Awww, **{invokerName}** is hugging **{userName}**!\nHow cute!",
                colour=0x89CFF0,
                description=message,
            )
            em.set_image(url=imageLink)

        else:
            em = discord.Embed(
                title="Your need to mention someone to hug, so\ni'm just gonna hug you instead!",
                colour=0x89CFF0,
            )
            em.set_image(url=imageLink)

        await sendEmbed(interaction, em)

    @app_commands.command(name="pat", description="Give other users headpats :)")
    @app_commands.describe(user="Who's gettin' dem pats?")
    async def pat(self, interaction: discord.Interaction, user: discord.Member):
        invokerName = (
            interaction.user.nick if interaction.user.nick else interaction.user.name  # type: ignore
        )
        userName = user.nick if user.nick else user.name

        em = discord.Embed(
            title=f"**{invokerName}** is giving **{userName}** headpats\nHow nice!",
            colour=0x89CFF0,
            description="*Headpat embeds coming soon!*",
        )

        await sendEmbed(interaction, em)

    @app_commands.command(name="kill", description="Murders the victim >:)")
    @app_commands.describe(user="**DO IT**")
    async def kill(self, interaction: discord.Interaction, user: discord.Member):
        invokerName = (
            interaction.user.nick if interaction.user.nick else interaction.user.name  # type: ignore
        )
        victimName = user.nick if user.nick else user.name

        if invokerName == victimName:
            await interaction.response.send_message(
                f"{invokerName} is staying alive! *pouts*"
            )
        else:
            sample = [
                f"Killed {victimName}! {victimName} is now dead :(",
                f"{invokerName} kicked {victimName} where nobody should be kicked.",
                f"{victimName} died.",
                f"{victimName} got hit by a truck.",
                f"{victimName} died after eating too many pickles.",
                f"In a surprising turn of events, {victimName} stays alive!",
                f"{invokerName} tries to kill {victimName}, but {victimName} is ready for them and slaps {invokerName}'s aorta!",
                f"{victimName} pogged too hard.",
                f"{victimName} got a question wrong in the victorian era, and was forced to wear the dunce hat. They died of embarrassment.",
                f"{invokerName} ran {victimName} over with their citroen.",
            ]
            await interaction.response.send_message(random.choice(sample))


cmds = [
    RoleplayCog.pat.name,
    RoleplayCog.hug.name,
    RoleplayCog.kill.name,
    RoleplayCog.boop.name,
    RoleplayCog.bonk.name,
]


async def setup(bot):
    await bot.add_cog(RoleplayCog(bot))
