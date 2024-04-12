import discord
import os
import asyncio
import discord.colour
from discord.ext import commands
import dotenv

dotenv.load_dotenv()

token = os.environ["TOKEN"]
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

intents = discord.Intents.default()
bot = commands.Bot("", intents=intents)


@bot.event
async def on_ready():
    if bot.user is None:
        print("Bot failed to log in. Exiting...")
        return

    print("Logged in as", bot.user)
    print("ID:", bot.user.id)

    await bot.tree.sync()
    print("Synced")

    await bot.change_presence(activity=discord.Game("Now with slash commands!"))


# @bot.command(name="timer")
# async def remind(ctx, time: int, x):
#     #    if x != None:
#     if x == "m":
#         print("mins")
#         date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now(
#         ).day, datetime.datetime.now().hour, datetime.datetime.now().minute + time, datetime.datetime.now().second)
#         timers.Timer(bot, "reminder", date, args=(
#             ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
#         await ctx.send(f"Your {time} minute timer has been started.")

#     elif x == "s":
#         print("seconds")
#         date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now(
#         ).day, datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second + time)
#         timers.Timer(bot, "reminder", date, args=(
#             ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
#         await ctx.send(f"Your {time} second timer has been started.")

#     elif x == "h":
#         print("hours")
#         date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now(
#         ).day, datetime.datetime.now().hour + time, datetime.datetime.now().minute, datetime.datetime.now().second)
#         timers.Timer(bot, "reminder", date, args=(
#             ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
#         await ctx.send(f"Your {time} hour timer has been started.")
#    else:
# date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour, datetime.datetime.now().minute + time, datetime.datetime.now().second)
# timers.Timer(bot, "reminder", date, args = (ctx.channel.id, ctx.author.id, f"{time}", f"{x}")).start()
# await ctx.send(f"Your {time} minute timer has been started.")
#        print("huh, weird lol")


# @bot.event
# async def on_reminder(channel_id, author_id, text, x):
#     channel = bot.get_channel(channel_id)
#     if x != None:
#         await channel.send("Your {0}{1} timer is up, <@{2}>!".format(text, x, author_id))
#     else:
#         await channel.send("Your {0} minute timer is up, <@{1}>!".format(text, author_id))


class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            em = discord.Embed(description=page)
            await destination.send(embed=em)


bot.help_command = NewHelpName()


async def load():
    bot.remove_command("help")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
