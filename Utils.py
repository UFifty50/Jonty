import logging
import discord
import enum


class Colour(enum.Enum):
    purple = 0xFF81FF
    darkblue = 0x0000FF
    lightblue = 0x0096FF
    red = 0xFF0000
    green = 0x00C800


class MaxLevelFilter(logging.Filter):
    def __init__(self, maxLevel: int):
        self.maxLevel = maxLevel

    def filter(self, record: logging.LogRecord):
        return record.levelno < self.maxLevel


async def sendEmbed(interaction: discord.Interaction, embed: discord.Embed):
    """Handles the sending of embeds

    - tries to send embed in channel
    - tries to send normal if that fails
    - tries to send ephemeral message if that fails

    Args:
        interaction (discord.Interaction): The interaction object
        embed (discord.Embed): The embed to send
    """

    try:
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        try:
            await interaction.response.send_message(
                "Hey, seems like I can't send embeds. Please check my permissions :)"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Hey, seems like I can't send any message in this channel. Please inform the server team about this issue.",
                ephemeral=True,
            )
