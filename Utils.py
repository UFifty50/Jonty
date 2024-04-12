import discord
import enum


class Colour(enum.Enum):
    purple = 0xFF81FF
    darkblue = 0x0000FF
    lightblue = 0x0096FF
    red = 0xFF0000
    green = 0x00C800

async def sendEmbed(interaction: discord.Interaction, embed: discord.Embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information about missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
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
                f"Hey, seems like I can't send any message in {interaction.channel.name} on {interaction.guild.name}\n" # type: ignore
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
                ephemeral=True,
            )
