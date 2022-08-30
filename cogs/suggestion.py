import discord
from discord.ext import commands
from datetime import *
import config

suggestionChannelIds = config.suggestionChannelIds

class Suggestions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="suggest", description="Creates a suggestion")
    async def suggest(self, ctx, message: str):
        user = ctx.author
        if ctx.channel.id in suggestionChannelIds and not user.bot:
    
            #The title and description
            suggestionEmbed = discord.Embed(
             fields=[
             discord.EmbedField(name="Предложение:", value=message, inline=False)
             ]
            )
            #Author, timestamp, footer and color
            suggestionEmbed.set_author(name=user.display_name)
            suggestionEmbed.timestamp = datetime.now()
            suggestionEmbed.set_footer(text='\u200b')
            if user.colour.value:
                suggestionEmbed.colour = user.colour
                suggestionEmbed.set_thumbnail(url="https://img.icons8.com/external-flaticons"+
                "-flat-circular-flat-icons/200/external-suggestions-customer-feedback-flaticons-flat-circular-flat-icons.png")

            message = await ctx.respond(embed = suggestionEmbed)
            msg = await message.original_message()
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
        else:
            await ctx.respond("You are not allowed to send this command here!", ephemeral=True)
        


def setup(client):
    client.add_cog(Suggestions(client))