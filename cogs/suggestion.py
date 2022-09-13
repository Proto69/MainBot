import discord
from discord.ext import commands
from datetime import *
import myConfig

suggestionChannelIds = myConfig.suggestionChannelIds


async def findingEmojis(message: discord.Message):
    emojiUp = "✅"
    emojiDown = "❌"
    for emoji in message.guild.emojis:
        if emoji.id in myConfig.emojisUp:
            emojiUp = emoji
        elif emoji.id in myConfig.emojisDown:
            emojiDown = emoji
    
    await message.add_reaction(emojiUp)
    await message.add_reaction(emojiDown)

class Suggestions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        user = message.author
        if not user.bot:
            if message.channel.id in suggestionChannelIds:
    
                #The title and description
                suggestionEmbed = discord.Embed(
                fields=[
                discord.EmbedField(name="Предложение:", value=message.content, inline=False)
                ]
                )
                #Author, timestamp, footer and color
                suggestionEmbed.set_author(name=user.display_name)
                suggestionEmbed.timestamp = datetime.now()
                if user.colour.value:
                    suggestionEmbed.colour = user.colour
                suggestionEmbed.set_thumbnail(url="https://img.icons8.com/external-flaticons"+
                "-flat-circular-flat-icons/200/external-suggestions-customer-feedback-flaticons-flat-circular-flat-icons.png")

                await message.delete()
                msg = await message.channel.send(embed = suggestionEmbed)
                await findingEmojis(msg)
                

def setup(client):
    client.add_cog(Suggestions(client))