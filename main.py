import os
import atexit
import logging
import logging.config
from logging import Handler, Logger
from logging.handlers import QueueHandler

import discord
from discord.ext import commands
import discord.colour

import yaml
import asyncio

from Utils import MaxLevelFilter  # for logging

import dotenv

dotenv.load_dotenv()


JontyLogger: Logger = logging.getLogger("Jonty")

intents = discord.Intents.default()
bot = commands.Bot(".", intents=intents)


def setupLogging():
    loggingConfig: dict

    with open("loggingConfig.yml", "r") as f:
        loggingConfig = yaml.safe_load(f)

    logging.config.dictConfig(loggingConfig)

    queueHandler: Handler | None = logging.getHandlerByName("QueueHandler")
    if isinstance(queueHandler, QueueHandler):
        JontyLogger.debug("QueueHandler found")
        queueHandler.listener.start()  # type: ignore
        atexit.register(queueHandler.listener.stop)  # type: ignore

    JontyLogger.info("Logging setup complete")


async def load():
    bot.remove_command("help")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    if bot.user is None:
        JontyLogger.critical("Bot failed to log in. Exiting...")
        return

    JontyLogger.info(f"Logged in as {bot.user}")
    JontyLogger.debug(f"ID: {bot.user.id}")

    await bot.tree.sync()
    JontyLogger.debug("Synced commands")

    await bot.change_presence(activity=discord.Game("Now with slash commands!"))
    JontyLogger.info("Bot is ready")


async def main():
    setupLogging()
    async with bot:
        await load()
        await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
