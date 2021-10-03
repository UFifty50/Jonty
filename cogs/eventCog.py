import discord
import json
import datetime
from discord.ext import commands


class eventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('fiftylolcount.json', 'r') as e:
            lols = json.load(e)
            lols[str(guild.id)] = 0
        with open('fiftylolcount.json', 'w') as e:
            json.dump(lols, e, indent=4)

        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes[str(guild.id)] = '.'
            prefix = prefixes[str(guild.id)]
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        self = await guild.fetch_member(self.bot.user.id)
        await self.edit(nick=f"[{prefix}] Jonty")

    @commands.Cog.listener()
    async def on_message(self, message):
        print(str(datetime.datetime.now()) +
              ': Message from {0.author}: {0.content}'.format(message))
        f = open(f'msglogs/{message.guild.id}.msgs', 'a')
        f.write(str(datetime.datetime.now()) +
                ': Message from {0.author}: {0.content}\n'.format(message))
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        f = open(f'msglogs/{message.guild.id}.msgs', 'a')
        f.write(str(datetime.datetime.now()) +
                ': {0.author} has deleted the message: {0.content}'.format(message))
        print(str(datetime.datetime.now()) +
              ': {0.author} has deleted the message: {0.content}'.format(message))

    @commands.Cog.listener()
    async def on_message_edit(self, message, newMsg):
        f = open(f'msglogs/{message.guild.id}.msgs', 'a')
        f.write(str(datetime.datetime.now()) +
                f': {message.author} has edited the message: {message.content} to: {newMsg.content}')
        print(str(datetime.datetime.now()) +
              f': {message.author} has edited the message: {message.content} to: {newMsg.content}')


def setup(bot):
    bot.add_cog(eventCog(bot))
    print("eventCog loaded")
