import discord
from discord.ext import commands
from discord.ui import View, Button
import config

joinRoleId = config.joinRoleId

class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="verify", description="Verify a message")
    async def verify(self, ctx):
        button = Button(label="Verify!", style = discord.ButtonStyle.blurple, custom_id="verifyButton")
        embed = discord.Embed(
          title="Verify Here",
          description="Gain access to all channels in the server by clicking the button below!",
          colour=discord.Color.green()
        )
        await ctx.channel.send(embed = embed, view=View(button))

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.custom_id == "verifyButton":
            user = interaction.user
            role = interaction.guild.get_role(joinRoleId)
            await user.add_roles(role)
            await interaction.response.send_message(f"You are now verified!", ephemeral=True)


def setup(client):
    client.add_cog(Verify(client))