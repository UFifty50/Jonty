import os
import logging
from logging import Logger
import discord
from discord import app_commands
from discord.ext import commands

from Utils import sendEmbed


JontyLogger: Logger = logging.getLogger("Jonty")

class HelpCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        JontyLogger.info("HelpCog is ready")

    @app_commands.command(name="help", description="Shows all modules of that bot")
    @app_commands.describe(module="Module to get help for")
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, interaction: discord.Interaction, module: str | None = None):
        if not module:
            # starting to build embed
            em = discord.Embed(
                title="Commands and modules",
                color=discord.Color.blue(),
                description="Use `help <module>` to gain more information about that module :smiley:\n",
            )

            cogDescriptions = ""
            for cog in self.bot.cogs:
                cogDescriptions += f"`{cog}` {self.bot.cogs[cog].__doc__}\n"

            em.add_field(name="Modules", value=cogDescriptions, inline=False)

            loneCmdDescriptions = ""
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    loneCmdDescriptions += f"{command.name} - {command.help}\n"

            # adding those commands to embed
            if loneCmdDescriptions:
                em.add_field(
                    name="Not belonging to a module",
                    value=loneCmdDescriptions,
                    inline=False,
                )

            em.add_field(
                name="About",
                value="Jonty was originally created by Ufifty50sh on February 21st, 2021, using discord.py.\n\
                                    Please visit https://github.com/ufifty50/Jonty to submit ideas or bugs.",
            )
            em.set_footer(
                text=f"Jonty is is currently version {os.environ['JONTY_VERSION']}"
            )

        else:
            if module not in self.bot.cogs.keys():
                em = discord.Embed(
                    title="What's that?!",
                    description=f"I've never heard from a module called `{module}` before :scream:",
                    color=discord.Color.orange(),
                )
            else:
                cog = self.bot.cogs[module]
                em = discord.Embed(
                    title=f"{cog} - Commands",
                    description=cog.__doc__,
                    color=discord.Color.green(),
                )

                for command in cog.get_commands():
                    if not command.hidden:
                        em.add_field(
                            name=f"`{command.name}`",
                            value=command.help,
                            inline=False,
                        )

        await sendEmbed(interaction, em)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
