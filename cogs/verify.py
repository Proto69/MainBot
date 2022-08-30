import discord
from discord.ext import commands
from discord.ui import View
import config

joinRoleId = config.joinRoleId

class VerifyMessageView(View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(label="Verify!", style = discord.ButtonStyle.blurple, custom_id="verifyButton")
    async def buttonVerify(self, button: discord.ui.Button, interaction: discord.Interaction):
      user = interaction.user
      role = interaction.guild.get_role(joinRoleId)
      await user.add_roles(role)
      await interaction.response.send_message(f"You are now verified!", ephemeral=True)

class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="verify", description="Verify a message")
    async def verify(self, ctx):
        channel = ctx.channel
        view = VerifyMessageView()
        embed = discord.Embed(
          title="Verify Here",
          description="Gain access to all channels in the server by clicking the button below!",
          colour=discord.Color.green()
        )
        await ctx.channel.send(embed = embed, view=view)


def setup(client):
    client.add_cog(Verify(client))